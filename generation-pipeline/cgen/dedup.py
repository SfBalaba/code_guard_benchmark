"""Шаг 4: дедупликация. candidates.jsonl -> deduped.jsonl + rejected_dedup.jsonl.

Точные дубликаты после нормализации пробелов: внутри запуска и против внешних файлов
(dedup.against — например, test CSV, чтобы его команды не попали в train).
Близкие дубликаты по эмбеддингам здесь не ищутся — для них оставлен отдельный шаг.
"""
import re

from .config import run_dir
from .io import read_commands, read_jsonl, write_jsonl

WS_RE = re.compile(r"\s+")


def normalize(cmd: str) -> str:
    return WS_RE.sub(" ", cmd.strip())


def run(cfg, log=print):
    out = run_dir(cfg)
    cands = read_jsonl(out / "candidates.jsonl")
    external = {}
    for path in cfg["dedup"]["against"]:
        for c in read_commands(path):
            external.setdefault(normalize(c), path)
    kept, rejected, seen = [], [], {}
    for c in cands:
        key = normalize(c["command"])
        if key in external:
            rejected.append({**c, "stage": "dedup", "reason": "overlaps_external", "overlap_with": external[key]})
        elif key in seen:
            rejected.append({**c, "stage": "dedup", "reason": "duplicate_in_run", "duplicate_of": seen[key]})
        else:
            seen[key] = c["record_id"]
            kept.append(c)
    write_jsonl(out / "deduped.jsonl", kept)
    write_jsonl(out / "rejected_dedup.jsonl", rejected)
    log(f"dedup: оставлено {len(kept)}, отброшено {len(rejected)} (внешних файлов: {len(cfg['dedup']['against'])})")
    return kept, rejected
