"""Чтение/запись JSONL, CSV и хешей. Форматы совместимы с d3-judge-pipeline."""
import csv
import hashlib
import json
import os
from pathlib import Path

# Порядок колонок итогового CSV по гайдлайну.
FIELDS = ["command", "description", "util", "severity", "category", "risk", "source", "seed", "class"]


def digest(value) -> str:
    if not isinstance(value, bytes):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True).encode()
    return hashlib.sha256(value).hexdigest()


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{n}: битый JSON ({exc.msg})") from None
    return rows


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    os.replace(tmp, path)


def append_jsonl(path, row):
    """Дописать одну строку и сразу сбросить на диск: обрыв сессии не теряет готовое."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def read_jsonl_tolerant(path):
    """Как read_jsonl, но отбрасывает недописанную последнюю строку после обрыва."""
    path = Path(path)
    if not path.exists():
        return []
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    if lines and not lines[-1].endswith(b"\n"):
        path.with_suffix(".interrupted-tail").write_bytes(lines.pop())
        path.write_bytes(b"".join(lines))
    return [json.loads(x) for x in lines if x.strip()]


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def read_commands(path):
    """Команды из CSV (колонка command) или JSONL (поле command) — для проверки пересечений."""
    path = Path(path)
    if path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as f:
            return [r["command"] for r in csv.DictReader(f) if r.get("command")]
    return [r["command"] for r in read_jsonl(path) if r.get("command")]


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)  # csv сам экранирует кавычки удвоением
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in FIELDS})
