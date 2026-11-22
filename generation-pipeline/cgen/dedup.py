"""Шаг 4: дедупликация. candidates.jsonl -> deduped.jsonl + rejected_dedup.jsonl.

Точные дубликаты после нормализации пробелов: внутри запуска и против внешних файлов
(dedup.against — например, test CSV, чтобы его команды не попали в train).
Близкие дубликаты по эмбеддингам здесь не ищутся — для них оставлен отдельный шаг.
"""
import re
from pathlib import Path

from .config import run_dir
from .io import read_commands, read_jsonl, write_jsonl

WS_RE = re.compile(r"\s+")


def normalize(cmd: str) -> str:
    """Схлопнуть пробелы и убрать строки-комментарии: сиды требуют заголовки # TASK/# FS,
    и test-команда с таким заголовком не должна проходить exact-dedup."""
    body = "\n".join(line for line in cmd.splitlines() if not line.lstrip().startswith("#"))
    return WS_RE.sub(" ", body.strip())


def against_files(cfg):
    """dedup.against: файлы или папки (из папки берутся все *.csv и *.jsonl рекурсивно, кроме MANIFEST)."""
    files = []
    for p in cfg["dedup"]["against"]:
        p = Path(p)
        if p.is_dir():
            files += sorted(x for x in p.rglob("*") if x.suffix in (".csv", ".jsonl") and x.is_file())
        elif p.is_file():
            files.append(p)
        else:
            raise FileNotFoundError(f"dedup.against: нет такого файла или папки {p}")
    return files


def run(cfg, log=print):
    out = run_dir(cfg)
    cands = read_jsonl(out / "candidates.jsonl")
    external = {}
    files = against_files(cfg)
    for path in files:
        for c in read_commands(path):
            external.setdefault(normalize(c), str(path))
    if cfg["dedup"]["against"] and not external:
        raise ValueError(f"dedup.against задан, но команд в нём 0: {cfg['dedup']['against']}")
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
    log(f"dedup: оставлено {len(kept)}, отброшено {len(rejected)} (внешних файлов: {len(files)}, команд: {len(external)})")
    return kept, rejected
