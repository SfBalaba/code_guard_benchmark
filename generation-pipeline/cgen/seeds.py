"""Шаг 1: загрузка и проверка seed.

Seed здесь — промпт-инструкция генератору (не команда и не random seed).
Формат JSONL совместим с d3-judge-pipeline:
  seed_id, split, risk, family_id, prompt, mechanism, source_kind, status,
  [few_shot], [source_commands], ... (остальные поля читаются, но не проверяются)
"""
import re

from .io import read_jsonl

REQUIRED = ["seed_id", "split", "risk", "family_id", "prompt"]
RISK_RE = re.compile(r"^CAT-\d+\.\d+$")


class SeedError(ValueError):
    pass


def load_seeds(cfg):
    seeds = read_jsonl(cfg["seeds_path"])
    if not seeds:
        raise SeedError(f"нет seed в {cfg['seeds_path']}")
    errors, ids = [], set()
    allowed = set(cfg["seeds"]["allowed_statuses"])
    for i, s in enumerate(seeds, 1):
        sid = s.get("seed_id", f"<строка {i}>")
        missing = [k for k in REQUIRED if not isinstance(s.get(k), str) or not s[k].strip()]
        if missing:
            errors.append(f"{sid}: нет полей {missing}")
            continue
        if sid in ids:
            errors.append(f"{sid}: повторяющийся seed_id")
        ids.add(sid)
        if s["split"] != cfg["split"]:
            errors.append(f"{sid}: split={s['split']}, а запуск для {cfg['split']} — test и train не смешиваем")
        if not RISK_RE.match(s["risk"]):
            errors.append(f"{sid}: risk должен выглядеть как CAT-N.M, получено {s['risk']!r}")
        if s.get("source_commands") or s.get("few_shot"):
            errors.append(f"{sid}: в seed есть реальные команды/few-shot — запрещено")
        if s.get("source_kind", "abstract_synthetic_spec") != "abstract_synthetic_spec":
            errors.append(f"{sid}: source_kind={s['source_kind']!r}, ожидается abstract_synthetic_spec")
        if allowed and s.get("status") not in allowed:
            errors.append(f"{sid}: status={s.get('status')!r} не в seeds.allowed_statuses {sorted(allowed)}")
    if errors:
        raise SeedError("Seed не прошли проверку:\n  - " + "\n  - ".join(errors))
    return seeds
