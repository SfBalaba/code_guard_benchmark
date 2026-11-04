"""Шаг 2: генерация. Сырые ответы модели -> raw.jsonl (по строке на вызов).

manifest.json фиксирует всё, что нужно для воспроизведения: конфиг, хеши шаблона и seed,
версию кода. --resume продолжает прерванный запуск, если эти хеши не изменились.
"""
import json
import time
from pathlib import Path

from . import __version__
from .backends import make_backend
from .config import run_dir
from .io import append_jsonl, digest, read_jsonl_tolerant, write_json
from .prompt import build_messages, load_template
from .seeds import load_seeds


def load_taxonomy(cfg):
    p = cfg.get("taxonomy_path")
    return json.loads(Path(p).read_text(encoding="utf-8")) if p else {}


def _fingerprint(cfg, template, seeds):
    gen_cfg = {k: cfg[k] for k in ("split", "prompt", "backend", "sampling", "labels")}
    gen_cfg["backend"] = {k: v for k, v in gen_cfg["backend"].items() if k != "api_key_env"}
    return digest({"cfg": gen_cfg, "template": template["raw"], "seeds": seeds, "code": __version__})


def call_seed(base_seed, seed_id, sample_idx):
    """Свой числовой seed на каждый вызов: воспроизводимо и без одинаковых ответов на разных seed."""
    return int(digest([base_seed, seed_id, sample_idx])[:8], 16)


def run(cfg, resume=False, limit=None, dry_run=False, log=print):
    out = run_dir(cfg)
    seeds = load_seeds(cfg)
    template = load_template(cfg["prompt"]["template"])
    taxonomy = load_taxonomy(cfg)
    fp = _fingerprint(cfg, template, seeds)

    manifest_path = out / "manifest.json"
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not resume:
            raise ValueError(f"{out} уже существует: добавь --resume или смени run_name")
        if old["fingerprint"] != fp:
            raise ValueError("конфиг, шаблон или seed изменились после начала запуска — --resume невозможен, смени run_name")
    else:
        out.mkdir(parents=True, exist_ok=True)
        backend_desc = {k: v for k, v in cfg["backend"].items() if k != "api_key_env"}
        write_json(manifest_path, {
            "run_name": cfg["run_name"],
            "code_version": __version__,
            "fingerprint": fp,
            "split": cfg["split"],
            "backend": backend_desc,
            "sampling": cfg["sampling"],
            "prompt_version": cfg["prompt"]["version"],
            "template_sha": digest(template["raw"]),
            "seeds_sha": digest(seeds),
            "n_seeds": len(seeds),
            "config_path": cfg["_config_path"],
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "gold": False,
        })

    raw_path = out / "raw.jsonl"
    done = {(r["seed_id"], r["sample_idx"]) for r in read_jsonl_tolerant(raw_path) if r["status"] == "ok"}
    backend = None if dry_run else make_backend(cfg)
    n_calls = 0
    for s in seeds:
        messages = build_messages(template, s, cfg, taxonomy)
        for k in range(cfg["sampling"]["samples_per_seed"]):
            if (s["seed_id"], k) in done:
                continue
            if limit is not None and n_calls >= limit:
                log(f"достигнут --limit {limit}")
                return raw_path
            cs = call_seed(cfg["sampling"]["seed"], s["seed_id"], k)
            rec = {"seed_id": s["seed_id"], "sample_idx": k, "call_seed": cs, "risk": s["risk"],
                   "family_id": s["family_id"], "prompt_sha": digest(messages)}
            t0 = time.monotonic()
            if dry_run:
                rec.update(status="dry_run", messages=messages)
            else:
                try:
                    raw, usage = backend.complete(messages, cs)
                    rec.update(status="ok", raw=raw, usage=usage)
                except Exception as exc:  # сбой одного вызова не роняет весь запуск
                    rec.update(status="failed", error=f"{type(exc).__name__}: {exc}")
            rec["latency_s"] = round(time.monotonic() - t0, 3)
            append_jsonl(raw_path, rec)
            n_calls += 1
            log(f"[{rec['status']}] {s['seed_id']} #{k}")
    return raw_path
