"""Шаг 6: экспорт. validated.jsonl -> dataset.csv (9 колонок гайдлайна) + provenance.jsonl.

В CSV нет места для seed_id, модели и т.п. — эта связь лежит в provenance.jsonl по порядку строк
и по record_id. Разметка из генерации — предложение для проверки человеком, не gold.
"""
import json

from .config import run_dir
from .generate import load_taxonomy
from .io import read_jsonl, write_csv, write_jsonl


def run(cfg, log=print):
    out = run_dir(cfg)
    taxonomy = load_taxonomy(cfg)
    seeds = {s["seed_id"]: s for s in read_jsonl(cfg["seeds_path"])}
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    rows, prov = [], []
    for c in read_jsonl(out / "validated.jsonl"):
        cat = c["risk"].split(".")[0]
        seed_val = seeds[c["seed_id"]]["prompt"] if cfg["export"]["seed_column"] == "prompt" else c["seed_id"]
        rows.append({
            "command": c["command"],
            "description": c["description"],
            "util": c["util"],
            "severity": c["severity"],
            "category": taxonomy.get(cat, cat),
            "risk": taxonomy.get(c["risk"], c["risk"]),
            "source": "synthetic",
            "seed": seed_val,
            "class": c["class"],
        })
        prov.append({
            "row": len(rows), "record_id": c["record_id"], "seed_id": c["seed_id"],
            "family_id": c["family_id"], "sample_idx": c["sample_idx"], "cand_idx": c["cand_idx"],
            "split": cfg["split"], "run_name": cfg["run_name"], "backend": manifest["backend"],
            "prompt_version": cfg["prompt"]["version"], "fixes": c.get("fixes", []),
            "warnings": c.get("warnings", []), "human_reviewed": False,
        })
    unnamed = sorted({r["risk"] for r in rows if r["risk"] not in taxonomy.values()})
    if unnamed:
        log(f"ВНИМАНИЕ: нет названий в taxonomy для {unnamed} — в CSV записан только id")
    write_csv(out / "dataset.csv", rows)
    write_jsonl(out / "provenance.jsonl", prov)
    log(f"export: {len(rows)} строк -> {out / 'dataset.csv'}")
    return rows
