"""Шаг 6: экспорт. validated.jsonl -> dataset.csv (9 колонок гайдлайна) + provenance.jsonl.

В CSV нет места для seed_id, модели и т.п. — эта связь лежит в provenance.jsonl по порядку строк
и по record_id. Разметка из генерации — предложение для проверки человеком, не gold.
"""
import json

from .config import run_dir
from .generate import load_taxonomy
from .io import digest, read_jsonl, read_jsonl_tolerant, write_csv, write_jsonl
from .prompt import build_messages, load_template


def run(cfg, log=print):
    out = run_dir(cfg)
    taxonomy = load_taxonomy(cfg)
    seeds = {s["seed_id"]: s for s in read_jsonl(cfg["seeds_path"])}
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    rows, prov = [], []
    mode = cfg["export"]["seed_column"]
    template = load_template(cfg["prompt"]["template"]) if mode == "full_request" else None
    sent = {(r["seed_id"], r["sample_idx"]): r.get("prompt_sha") for r in read_jsonl_tolerant(out / "raw.jsonl")}

    def seed_value(c):
        if mode == "seed_id":
            return c["seed_id"]
        if mode == "prompt":
            return seeds[c["seed_id"]]["prompt"]
        # Полный фактический запрос: пересобираем и сверяем с sha того, что реально ушло в модель.
        msgs = build_messages(template, seeds[c["seed_id"]], cfg, taxonomy)
        if digest(msgs) != sent.get((c["seed_id"], c["sample_idx"])):
            raise ValueError(f"{c['seed_id']}#{c['sample_idx']}: сиды/шаблон изменились после generate — "
                             "колонка seed не совпала бы с фактическим запросом; перезапусти генерацию")
        return "\n\n".join(f"[{m['role']}]\n{m['content']}" for m in msgs)

    for c in read_jsonl(out / "validated.jsonl"):
        cat = c["risk"].split(".")[0]
        seed_val = seed_value(c)
        rows.append({
            "command": c["command"],
            "description": c["description"],
            "util": c["util"],
            "severity": c["severity"],
            # голые коды, как в test-CSV (решение 21.11); названия из taxonomy — только для промптов
            "category": cat,
            "risk": c["risk"],
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
            **({"model": c["model"]} if c.get("model") else {}),
            **({"pair_id": c["pair_id"], "role": c["role"], "review": c.get("review")} if c.get("pair_id") else {}),
        })
    write_csv(out / "dataset.csv", rows)
    write_jsonl(out / "provenance.jsonl", prov)
    log(f"export: {len(rows)} строк -> {out / 'dataset.csv'}")
    return rows
