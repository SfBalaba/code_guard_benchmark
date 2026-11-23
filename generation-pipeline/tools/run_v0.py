"""Полный прогон train v0: три модели по очереди -> объединение -> общий конвейер.

    python3 tools/run_v0.py              # с нуля или продолжить прерванный (идемпотентно)
    python3 tools/run_v0.py --models qwen38_27b   # только одна модель (отладка)

Каждая модель: поднять llama-server, `cgen generate --resume` (только генерация) в runs/train_v0_<m>/.
Затем сырьё всех моделей сливается в runs/v0/raw.jsonl (sample_idx помечается моделью, чтобы pair_id не
пересекались), и ОДИН раз прогоняются clean -> dedup -> neardup -> validate -> export -> report. Так near-dup
и лимиты рецептов применяются МЕЖДУ моделями, а не только внутри каждой, а дедуп против test — ко всему сразу.

Итог: runs/v0/dataset.csv (9 колонок), provenance.jsonl (модель/seed/версия на строку), report.md.
Резюмируемо: повторный запуск продолжает генерацию каждой модели и пересобирает слияние.

Другой набор конфигов (та же тройка моделей, свои сиды и контракт меток) — --prefix:
    python3 tools/run_v0.py --prefix train_cat4     # configs/train_cat4_<m>.json -> runs/train_cat4_<m>/, слияние в runs/cat4/
Имя слияния = prefix без «train_» (train_v0 -> v0, как раньше). --limit N — не больше N вызовов на модель (смоук).
"""
import argparse
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cgen import clean, dedup, export, generate, neardup, report, validate  # noqa: E402
from cgen.config import load_config, run_dir  # noqa: E402
from cgen.io import append_jsonl, digest, read_jsonl_tolerant, write_json  # noqa: E402

MODELS = ["qwen38_27b", "gemma4_26b_a4b", "devstral24b"]
TAG = {"qwen38_27b": "q", "gemma4_26b_a4b": "g", "devstral24b": "d"}
PORT = 8080


def wait_health(timeout=400):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=5) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(3)
    return False


def generate_model(m, models_dir, log_file, log, prefix="train_v0", limit=None):
    cfg = load_config(ROOT / f"configs/{prefix}_{m}.json")
    gguf = Path(models_dir).expanduser() / cfg["backend"]["model"].split("/")[-1].split("@")[0]
    if not gguf.exists():
        raise FileNotFoundError(f"нет модели {gguf}")
    srv = subprocess.Popen(
        ["llama-server", "-m", str(gguf), "--jinja", "-c", "8192", "-ngl", "99",
         "--host", "127.0.0.1", "--port", str(PORT)], stdout=log_file, stderr=subprocess.STDOUT)
    try:
        if not wait_health():
            raise RuntimeError(f"{m}: llama-server не поднялся, см. {log_file.name}")
        log(f"[{time.strftime('%H:%M:%S')}] {m}: генерация (resume)…")
        generate.run(cfg, resume=True, limit=limit, log=lambda *a: None)
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=30)
        except subprocess.TimeoutExpired:
            srv.kill()
    return cfg


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--models", default=",".join(MODELS))
    p.add_argument("--models-dir", default="~/models/codeguard")
    p.add_argument("--skip-generate", action="store_true", help="только пересобрать слияние из готовых raw")
    p.add_argument("--prefix", default="train_v0", help="конфиги configs/<prefix>_<model>.json")
    p.add_argument("--limit", type=int, help="не больше N новых вызовов на модель (смоук)")
    a = p.parse_args(argv)
    models = a.models.split(",")
    log = print
    name = a.prefix.removeprefix("train_")   # train_v0 -> v0 (пути v0 не меняются)

    cfgs = {}
    with open(ROOT / f"runs/{name}_llama-server.log", "a") as lf:
        for m in models:
            if a.skip_generate:
                cfgs[m] = load_config(ROOT / f"configs/{a.prefix}_{m}.json")
                continue
            cfgs[m] = generate_model(m, a.models_dir, lf, log, a.prefix, a.limit)
            raws = read_jsonl_tolerant(run_dir(cfgs[m]) / "raw.jsonl")
            ok = sum(r["status"] == "ok" for r in raws)
            log(f"[{time.strftime('%H:%M:%S')}] {m}: raw {len(raws)}, ok {ok}")

    # --- merge raw of all models into runs/v0 ---
    v0 = ROOT / "runs" / name
    v0.mkdir(parents=True, exist_ok=True)
    merged = v0 / "raw.jsonl"
    merged.unlink(missing_ok=True)
    backends = {}
    for m in models:
        man = json.loads((run_dir(cfgs[m]) / "manifest.json").read_text(encoding="utf-8"))
        backends[m] = man.get("backend")
        for r in read_jsonl_tolerant(run_dir(cfgs[m]) / "raw.jsonl"):
            r["model"] = m
            r["sample_idx"] = f"{TAG.get(m, m)}{r['sample_idx']}"   # уникальные pair_id между моделями
            append_jsonl(merged, r)

    # merged config = базовый (qwen) с общими seeds/labels/neardup/dedup, run_name=v0
    base = json.loads((ROOT / f"configs/{a.prefix}_{models[0]}.json").read_text(encoding="utf-8"))
    base.update(run_name=name, output_dir="../runs")
    # пишем в configs/, чтобы относительные пути (seeds, data/test, template) резолвились как у обычных конфигов
    mcfg_path = ROOT / "configs" / f"_{name}_merged.config.json"
    mcfg_path.write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
    mcfg = load_config(mcfg_path)
    write_json(v0 / "manifest.json", {
        "backend": backends, "models": models, "seeds_sha": digest(sorted(TAG)),
        "note": f"{name} merged across models; near-dup & recipe caps applied across the merged set",
        "merged_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "gold": False})

    for step in (clean.run, dedup.run, neardup.run, validate.run, export.run, report.run):
        step(mcfg, log=log)
    log(f"\n{name} готов: {v0/'dataset.csv'}  (provenance.jsonl, report.md рядом)")
    log("НЕ gold и НЕ human-reviewed; дальше — judge Дарины + ручное ревью. Модели (24-27B) согласованы командой 22.11.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
