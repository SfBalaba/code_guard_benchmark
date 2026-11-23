"""Конвертер TRAIN-сидов коллег (.txt, один файл = полный промпт на пару risky/safe) в JSONL для cgen.

Читает файлы прямо из git-ветки репозитория данных (без checkout), поэтому в каждую запись
попадает происхождение: ветка, коммит, путь и sha256 исходного текста.

    python3 tools/convert_txt_seeds.py --repo .. --ref origin/feat/data_Cat-6.5 \
        --risk CAT-1.4 CAT-5.1 CAT-5.2 CAT-5.3 CAT-5.4 --out seeds/train

Пишет <out>/<risk>.jsonl на подкатегорию и <out>/all.jsonl со всеми вместе.

Сиды CAT-4 (a.kirillov) — файлы .md в ОДНОЙ общей папке на все подкатегории (CAT-4/seeds/CAT-4.1-TRAIN-S01.md …):

    python3 tools/convert_txt_seeds.py --repo .. --ref 2efa9ea --ref-name feat/data_CAT-4 --folder CAT-4/seeds \
        --risk CAT-4.1 CAT-4.2 CAT-4.3 CAT-4.4 CAT-4.5 --expect-per-risk 20 --combined CAT-4.jsonl --out seeds/train

--folder — общая папка вместо <risk>/seeds; --combined — имя общего файла вместо all.jsonl
(all.jsonl — база build_en_seeds.py для v0, его нельзя переписывать сидами других категорий).

Защита от утечки test → train: файл берётся только если в имени есть TRAIN, а в тексте файла
и README папки нет пометок TEST-only («never TRAIN», «Только TEST» …). Иначе — ошибка, ничего не пишется.
Текст промпта переносится как есть (только нормализуются концы строк), чтобы в seed был полный фактический промпт.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TEST_MARKERS = [
    re.compile(p, re.I) for p in (
        r"never\s+TRAIN", r"belong\s+to\s+TEST", r"Только\s+TEST", r"TEST\s+seed",
        r"Не\s+использовать\s+в\s+train",
    )
]
NAME_RE = re.compile(r"^(CAT-\d+\.\d+)-TRAIN-S(\d+)\.(?:txt|md)$")
SEED_EXT = (".txt", ".md")
VERSION_RE = re.compile(r"\bv(\d+(?:\.\d+)*)\b")


def git_bytes(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def git(repo, *args):
    return git_bytes(repo, *args).decode("utf-8")


# Объявленный в тексте сида код риска: «risk=CAT-1.4 …», «Риск CAT-5.1 …» или «risk CAT-6.1 …» (сиды CAT-6.1).
DECLARED_RISK_RE = re.compile(r"(?:\brisk=|\brisk\s+|^Риск\s+)(CAT-\d+\.\d+)", re.M)


def mechanism_of(text, seed_id):
    """Короткая метка рецепта: заголовок после «—» в первой строке или строка «Сценарий:»."""
    first = text.splitlines()[0].lstrip("# ").strip()
    if "—" in first:
        return first.split("—", 1)[1].strip()
    m = re.search(r"^(?:Сценарий|Сценарное задание):\s*(.+)$", text, re.M)
    if m:
        return m.group(1).strip().rstrip(".")
    raise ValueError(f"{seed_id}: не нашёл заголовок/сценарий для mechanism")


def convert_risk(repo, ref, commit, risk, author, folder=None, ref_name=None):
    """folder=None — своя папка <risk>/seeds; иначе общая папка, из которой берутся только файлы <risk>-TRAIN-*."""
    shared = folder is not None
    folder = folder or f"{risk}/seeds"
    names = git(repo, "ls-tree", "--name-only", f"{ref}:{folder}").splitlines()
    if "README.md" not in names:
        raise ValueError(f"{folder}: нет README.md — не понять, TRAIN это или TEST")
    readme = git(repo, "show", f"{ref}:{folder}/README.md")
    if not re.search(r"\bTRAIN\b", readme, re.I):
        raise ValueError(f"{folder}/README.md не помечает сиды как TRAIN")
    if any(p.search(readme) for p in TEST_MARKERS):
        raise ValueError(f"{folder}/README.md помечен как TEST — эти сиды в train брать нельзя")
    vm = VERSION_RE.search(readme)
    version = vm.group(1) if vm else "unversioned"

    # Всё, кроме README.md, обязано быть TRAIN-сидом с правильным именем — иначе ошибка, а не пропуск.
    others = [n for n in names if n != "README.md"]
    for name in others:
        if not name.endswith(SEED_EXT) or not NAME_RE.match(name):
            raise ValueError(f"{folder}/{name}: имя не вида CAT-N.M-TRAIN-SNN.(txt|md) — не TRAIN-сид?")
    txts = sorted(n for n in others if NAME_RE.match(n).group(1) == risk or not shared)
    if not txts:
        raise ValueError(f"{folder}: нет сидов {risk}")
    out = []
    for name in txts:
        m = NAME_RE.match(name)
        if m.group(1) != risk:
            raise ValueError(f"{folder}/{name}: код в имени {m.group(1)} ≠ папке {risk}")
        raw = git_bytes(repo, "show", f"{ref}:{folder}/{name}")
        text = raw.decode("utf-8").replace("\r\n", "\n").strip() + "\n"
        seed_id = Path(name).stem
        if any(p.search(text) for p in TEST_MARKERS):
            raise ValueError(f"{seed_id}: в тексте пометка TEST-only")
        if seed_id not in text.splitlines()[0]:
            raise ValueError(f"{seed_id}: первая строка файла не содержит его ID")
        declared = set(DECLARED_RISK_RE.findall(text))
        if declared != {risk}:
            raise ValueError(f"{seed_id}: в тексте объявлен risk {sorted(declared) or 'не найден'}, ожидается {risk}")
        out.append({
            "seed_id": seed_id,
            "split": "train",
            "risk": risk,
            "family_id": f"{risk}/S{m.group(2)}",
            "prompt": text,
            "mechanism": mechanism_of(text, seed_id),
            "source_kind": "abstract_synthetic_spec",
            "status": "approved_for_generation",
            "model_family_blocklist": [],
            "ancestors": [],
            "version": version,
            "author": author,
            "origin": {
                "repo": "SfBalaba/code_guard_benchmark",
                "ref": ref_name or ref.removeprefix("origin/"),
                "commit": commit,
                "path": f"{folder}/{name}",
                "sha256": hashlib.sha256(raw).hexdigest(),  # байты blob, как `git show | sha256sum`
            },
        })
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo", required=True, help="локальный клон code_guard_benchmark")
    p.add_argument("--ref", required=True, help="ветка/коммит с папками CAT-N.M/seeds")
    p.add_argument("--risk", nargs="+", required=True, help="подкатегории, например CAT-1.4 CAT-5.1")
    p.add_argument("--out", required=True, help="папка для JSONL")
    p.add_argument("--folder", help="общая папка сидов для всех --risk (по умолчанию <risk>/seeds)")
    p.add_argument("--ref-name", help="имя ветки для origin.ref, если --ref — коммит")
    p.add_argument("--combined", default="all.jsonl", help="имя общего файла (по умолчанию all.jsonl)")
    p.add_argument("--expect-per-risk", type=int, help="ошибка, если сидов на подкатегорию не столько")
    a = p.parse_args(argv)

    repo = Path(a.repo)
    commit = git(repo, "rev-parse", a.ref).strip()
    try:
        groups = {}
        for risk in a.risk:
            author = git(repo, "log", "-1", "--format=%an", a.ref, "--", a.folder or f"{risk}/seeds").strip() or "unknown"
            groups[risk] = convert_risk(repo, a.ref, commit, risk, author, a.folder, a.ref_name)
            if a.expect_per_risk is not None and len(groups[risk]) != a.expect_per_risk:
                raise ValueError(f"{risk}: {len(groups[risk])} сидов, ожидалось {a.expect_per_risk}")
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"ошибка: {getattr(exc, 'stderr', '') or exc}", file=sys.stderr)
        return 2

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    every = []
    for risk, rows in groups.items():
        (out / f"{risk}.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        every += rows
        print(f"{risk}: {len(rows)} seed")
    (out / a.combined).write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in every), encoding="utf-8")
    print(f"всего {len(every)} seed → {out}/{a.combined} (commit {commit[:7]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
