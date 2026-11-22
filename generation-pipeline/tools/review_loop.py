"""Одна итерация цикла «сгенерировать → посмотреть → поправить сиды» на локальных моделях.

    python3 tools/review_loop.py --iter 1 --seeds seeds/train/all.jsonl --per-risk 2
    python3 tools/review_loop.py --iter 2 --seeds seeds/train_edit/all.jsonl --ids-from 1 --extra 1

Для каждой модели из train v0 (configs/train_v0_<model>.json): поднимает llama-server на 127.0.0.1
с GGUF из --models-dir, гоняет весь cgen (generate → … → report) по выборке seed, гасит сервер.
Итог в runs/review/iter<N>/: seeds.jsonl (выборка), <model>/ (обычный прогон cgen),
summary.md (метрики по моделям и подкатегориям) и review.md (каждая пара — для ручного ревью).

Выборка: --per-risk seed на подкатегорию (random_state = --random-state), либо те же seed_id, что
в итерации --ids-from, плюс --extra новых на подкатегорию — чтобы сиды не подгонялись под одну выборку.
Команды из ответов модели не исполняются (cgen проверяет только bash -n).
"""
import argparse
import collections
import copy
import hashlib
import json
import random
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cgen import clean, dedup, export, generate, neardup, report, validate  # noqa: E402
from cgen.config import load_config  # noqa: E402
from cgen.io import read_jsonl  # noqa: E402

# Старая утверждённая тройка + кандидаты покрупнее (21.11); --models выбирает подмножество
MODELS_OLD = ["qwen25coder7b", "gemma3_12b", "llama31_8b"]
MODELS_NEW = ["qwen38_27b", "gemma4_26b_a4b", "devstral24b"]
MODELS = MODELS_OLD + MODELS_NEW
PORT = 8080


def sha256_file(path, cache):
    key = f"{path}:{path.stat().st_size}:{path.stat().st_mtime_ns}"
    if key not in cache:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 24), b""):
                h.update(chunk)
        cache[key] = h.hexdigest()
    return cache[key]


def pick_seeds(all_seeds, args, out):
    by_risk = collections.defaultdict(list)
    for s in all_seeds:
        by_risk[s["risk"]].append(s)
    rnd = random.Random(args.random_state)
    chosen = []
    if args.ids_from:
        prev = {s["seed_id"] for s in read_jsonl(ROOT / f"runs/review/iter{args.ids_from}/seeds.jsonl")}
        chosen = [s for s in all_seeds if s["seed_id"] in prev]
        for risk, ss in sorted(by_risk.items()):
            rest = [s for s in ss if s["seed_id"] not in prev and s["seed_id"] not in used_before(args.iter)]
            chosen += rnd.sample(rest, min(args.extra, len(rest)))
    else:
        used = used_before(args.iter) if args.fresh else set()
        for risk, ss in sorted(by_risk.items()):
            pool = [s for s in ss if s["seed_id"] not in used]
            if args.fresh and len(pool) < args.per_risk:
                print(f"предупреждение: {risk} — свежих сидов {len(pool)} < per-risk {args.per_risk}", file=sys.stderr)
            chosen += rnd.sample(pool, min(args.per_risk, len(pool)))
    out.write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in chosen), encoding="utf-8")
    return chosen


def used_before(it):
    ids = set()
    for k in range(1, it):
        p = ROOT / f"runs/review/iter{k}/seeds.jsonl"
        if p.exists():
            ids |= {s["seed_id"] for s in read_jsonl(p)}
    return ids


def wait_health(timeout=300):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=5) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(2)
    return False


def run_model(model, seeds_path, it_dir, models_dir, log_file, hashes):
    base = json.loads((ROOT / f"configs/train_v0_{model}.json").read_text(encoding="utf-8"))
    gguf = Path(models_dir).expanduser() / base["backend"]["model"].split("/")[-1].split("@")[0]
    if not gguf.exists():
        raise FileNotFoundError(f"нет файла модели {gguf}")
    cfg_raw = copy.deepcopy(base)
    cfg_raw.update(run_name=model, output_dir=str(it_dir), seeds_path=str(seeds_path))
    cfg_raw["sampling"]["samples_per_seed"] = 1
    cfg_raw["dedup"]["against"] = [str(ROOT / "data/test")]
    cfg_raw["taxonomy_path"] = str(ROOT / "taxonomy.json")
    cfg_raw["prompt"]["template"] = str(ROOT / "prompts/generation_v2.md")
    cfg_path = it_dir / f"{model}.config.json"
    cfg_path.write_text(json.dumps(cfg_raw, ensure_ascii=False, indent=2), encoding="utf-8")
    cfg = load_config(cfg_path)

    srv = subprocess.Popen(
        ["llama-server", "-m", str(gguf), "--jinja", "-c", "8192", "-ngl", "99",
         "--host", "127.0.0.1", "--port", str(PORT)],
        stdout=log_file, stderr=subprocess.STDOUT)
    try:
        if not wait_health():
            raise RuntimeError(f"{model}: llama-server не поднялся, см. {log_file.name}")
        t0 = time.time()
        generate.run(cfg, log=lambda *a: None)
        for step in (clean.run, dedup.run, neardup.run, validate.run, export.run, report.run):
            step(cfg, log=lambda *a: None)
        wall = time.time() - t0
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=30)
        except subprocess.TimeoutExpired:
            srv.kill()
    return {"gguf": gguf.name, "gguf_sha256": sha256_file(gguf, hashes), "wall_s": round(wall, 1)}


def summarize(it_dir, models, meta):
    lines = [f"# Ревью-итерация {it_dir.name}", ""]
    review = [f"# Пары для ревью — {it_dir.name}", ""]
    seeds = {s["seed_id"]: s for s in read_jsonl(it_dir / "seeds.jsonl")}
    lines += ["| модель | вызовов | ok JSON | отказов | пар прошло | % пар | ср. сек/вызов | ток/с |",
              "|---|---|---|---|---|---|---|---|"]
    per_risk = collections.defaultdict(lambda: collections.Counter())
    reasons_all = collections.Counter()
    for m in models:
        d = it_dir / m
        raw = read_jsonl(d / "raw.jsonl")
        rej = read_jsonl(d / "rejected_clean.jsonl") + read_jsonl(d / "rejected_dedup.jsonl") + \
            read_jsonl(d / "rejected_validate.jsonl")
        kept = read_jsonl(d / "validated.jsonl")
        pairs = {c["pair_id"] for c in kept if c.get("pair_id")}
        refused = sum(r["reason"] == "model_refused" for r in rej)
        bad_json = sum(r["reason"] in ("invalid_json", "no_json_object", "no_candidates_list") for r in rej)
        lat = [r.get("latency_s", 0) for r in raw if r["status"] == "ok"]
        toks = sum((r.get("usage") or {}).get("completion_tokens", 0) for r in raw)
        tps = toks / sum(lat) if lat and sum(lat) else 0
        n = len(raw)
        lines.append(f"| {m} | {n} | {n - bad_json - sum(r['status'] != 'ok' for r in raw)} | {refused} | "
                     f"{len(pairs)} | {100 * len(pairs) / max(n, 1):.0f}% | {sum(lat) / max(len(lat), 1):.0f} | {tps:.0f} |")
        for r in raw:
            per_risk[r["risk"]]["calls"] += 1
        for p in pairs:
            per_risk[seeds[p.split("#")[0]]["risk"]]["pairs"] += 1
        for r in rej:
            reasons_all[f"{m}: {r['reason'].split(':')[0] if r['reason'].startswith('pair_rejected') else r['reason']}"] += 1

        # review sheet
        by_pair = collections.defaultdict(dict)
        for c in kept:
            if c.get("pair_id"):
                by_pair[c["pair_id"]][c["role"]] = c
        rej_by_seed = collections.defaultdict(list)
        for r in rej:
            rej_by_seed[(r["seed_id"], r.get("sample_idx"))].append(r)
        for r in raw:
            key = (r["seed_id"], r["sample_idx"])
            pid = f"{r['seed_id']}#{r['sample_idx']}"
            review.append(f"## {m} · {r['seed_id']} · {seeds[r['seed_id']]['mechanism']}")
            if pid in by_pair and len(by_pair[pid]) == 2:
                for role in ("risky", "safe"):
                    c = by_pair[pid][role]
                    review.append(f"**{role}** → `{c['class']}/{c['severity']}` · util `{c['util']}` · "
                                  f"{c['description']}\n```bash\n{c['command']}\n```")
                rv = by_pair[pid]["risky"].get("review")
                if rv:
                    review.append("<details><summary>review модели</summary>\n\n```json\n" +
                                  json.dumps(rv, ensure_ascii=False, indent=1)[:3000] + "\n```\n</details>")
            else:
                why = "; ".join(sorted({x["reason"] for x in rej_by_seed.get(key, [])})) or r["status"]
                review.append(f"**отброшено:** `{why}`")
                for x in rej_by_seed.get(key, []):
                    if x.get("model_reason"):
                        review.append(f"> причина модели: {x['model_reason']}")
                    if x.get("details"):
                        review.append(f"> детали: {x['details']}")
                raw_txt = (r.get("raw") or r.get("error") or "")[:1500]
                review.append("```\n" + raw_txt + "\n```")
            review.append("")
    lines += ["", "| подкатегория | вызовов | пар прошло | % |", "|---|---|---|---|"]
    for risk, c in sorted(per_risk.items()):
        lines.append(f"| {risk} | {c['calls']} | {c['pairs']} | {100 * c['pairs'] / max(c['calls'], 1):.0f}% |")
    lines += ["", "## Причины отсева", ""] + [f"- {v} × {k}" for k, v in reasons_all.most_common()]
    lines += ["", "## Модели", ""] + [f"- {m}: `{v['gguf']}` sha256 `{v['gguf_sha256']}`, {v['wall_s']} c"
                                      for m, v in meta.items()]
    (it_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (it_dir / "review.md").write_text("\n".join(review) + "\n", encoding="utf-8")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--iter", type=int, required=True)
    p.add_argument("--seeds", required=True, help="JSONL с seed (оригинал или правленая версия)")
    p.add_argument("--per-risk", type=int, default=2)
    p.add_argument("--ids-from", type=int, help="взять те же seed_id, что в итерации N")
    p.add_argument("--extra", type=int, default=0, help="плюс столько новых seed на подкатегорию")
    p.add_argument("--fresh", action="store_true", help="брать только сиды, не использованные в прошлых итерациях")
    p.add_argument("--random-state", type=int, default=20261121)
    p.add_argument("--models", default=",".join(MODELS))
    p.add_argument("--models-dir", default="~/models/codeguard")
    p.add_argument("--add", action="store_true", help="добавить модели в существующую итерацию (те же seed)")
    a = p.parse_args(argv)

    it_dir = ROOT / f"runs/review/iter{a.iter}"
    models = a.models.split(",")
    meta_path = it_dir / "meta.json"
    if it_dir.exists() and not a.add:
        print(f"ошибка: {it_dir} уже есть — новая итерация = новый номер (или --add)", file=sys.stderr)
        return 2
    if a.add:
        if not it_dir.exists():
            print(f"ошибка: --add, а {it_dir} нет", file=sys.stderr)
            return 2
        old = json.loads(meta_path.read_text())
        if old["seeds"] != a.seeds:
            print(f"ошибка: итерация шла на {old['seeds']}, а передано {a.seeds}", file=sys.stderr)
            return 2
        clash = [m for m in models if (it_dir / m).exists()]
        if clash:
            print(f"ошибка: модели уже прогнаны в этой итерации: {clash}", file=sys.stderr)
            return 2
        chosen = read_jsonl(it_dir / "seeds.jsonl")
    else:
        it_dir.mkdir(parents=True)
        chosen = pick_seeds(read_jsonl(ROOT / a.seeds), a, it_dir / "seeds.jsonl")
        old = {"seeds": a.seeds, "models": {}}
    print(f"seed в выборке: {len(chosen)} ({', '.join(s['seed_id'] for s in chosen)})")
    hashes_path = Path(a.models_dir).expanduser() / ".sha256_cache.json"
    hashes = json.loads(hashes_path.read_text()) if hashes_path.exists() else {}
    meta = dict(old["models"])
    with open(it_dir / "llama-server.log", "a") as log_file:
        for m in models:
            print(f"[{time.strftime('%H:%M:%S')}] {m} …", flush=True)
            meta[m] = run_model(m, it_dir / "seeds.jsonl", it_dir, a.models_dir, log_file, hashes)
            hashes_path.write_text(json.dumps(hashes))
            print(f"[{time.strftime('%H:%M:%S')}] {m} готово за {meta[m]['wall_s']} c", flush=True)
            meta_path.write_text(json.dumps({"seeds": a.seeds, "models": meta}, ensure_ascii=False, indent=1))
    print(summarize(it_dir, list(meta), meta))
    return 0


if __name__ == "__main__":
    sys.exit(main())
