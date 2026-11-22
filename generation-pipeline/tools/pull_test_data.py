"""Выгрузка всех test- и real-команд из веток репозитория данных — для dedup.against (антиутечка).

    python3 tools/pull_test_data.py --repo .. --out data/test

Берёт из каждой ветки origin/feat/* файлы с командами, которые НЕ должны попасть в train:
  - */commands.csv (test всех подкатегорий, включая старые версии в history/ и followup/),
  - commands_test.csv (CAT-4),
  - CAT-7.x/inputs/commands.jsonl,
  - D2-local*/commands.jsonl (реальные локальные логи — по правилу 1 только для test).
Не берёт commands_train.csv, sources.csv, CLASS_CHANGELOG, provenance, разметку.

Одинаковые файлы в разных ветках (один blob) сохраняются один раз. Пишет <out>/<ветка>/<путь>
и <out>/MANIFEST.json (ветка, путь, blob, число команд). Папка data/ в .gitignore — в git не попадает.
Сначала сделай `git fetch origin`, чтобы взять свежие ветки.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cgen.io import read_commands  # noqa: E402

INCLUDE = re.compile(
    r"(^|/)commands\.csv$|(^|/)commands_test\.csv$|^CAT-7\.\d+/inputs/commands\.jsonl$|^D2-local[^/]*/commands\.jsonl$"
)


def git(repo, *args, binary=False):
    out = subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout
    return out if binary else out.decode("utf-8")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo", required=True, help="локальный клон code_guard_benchmark")
    p.add_argument("--out", required=True, help="куда сложить файлы (например data/test)")
    a = p.parse_args(argv)
    repo, out = Path(a.repo), Path(a.out)

    branches = [b.strip() for b in git(repo, "branch", "-r", "--format=%(refname:short)").splitlines()
                if b.strip().startswith("origin/feat/") and "generation-pipeline" not in b]
    seen, manifest = {}, []
    for br in sorted(branches):
        for line in git(repo, "ls-tree", "-r", br).splitlines():
            meta, path = line.split("\t", 1)
            blob = meta.split()[2]
            if not INCLUDE.search(path) or "generation-pipeline/" in path:
                continue
            if blob in seen:
                continue
            dest = out / br.removeprefix("origin/") / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(git(repo, "cat-file", "blob", blob, binary=True))
            n = len(read_commands(dest))
            seen[blob] = str(dest)
            manifest.append({"branch": br, "path": path, "blob": blob, "commands": n,
                             "file": str(dest.relative_to(out))})
            if n == 0:
                print(f"ВНИМАНИЕ: {br}:{path} — 0 команд (нет колонки/поля command?)", file=sys.stderr)
    commit_of = {br: git(repo, "rev-parse", br).strip() for br in branches}
    (out / "MANIFEST.json").write_text(json.dumps(
        {"branches": commit_of, "files": manifest}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    total = sum(m["commands"] for m in manifest)
    print(f"{len(manifest)} файлов, {total} команд (с повторами между версиями) → {out}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
