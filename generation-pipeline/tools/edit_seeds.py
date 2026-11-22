"""Применить правку сидов (seeds/edits/<id>.json) к сконвертированным оригиналам.

    python3 tools/edit_seeds.py --base seeds/train/all.jsonl --edit seeds/edits/vp1.json --out seeds/train_vp1

Оригиналы не меняются. В каждую изменённую запись пишется version "<старая>-<edit_id>" и блок edit:
id, sha256 исходного prompt, список применённых правок с причинами. <out>/CHANGELOG.md — diff по каждому сиду.
Замена, которая не нашла свой old в целевом сиде, — ошибка (а не молчаливый пропуск).
"""
import argparse
import difflib
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cgen.io import read_jsonl  # noqa: E402


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", required=True)
    p.add_argument("--edit", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args(argv)
    seeds = read_jsonl(a.base)
    ed = json.loads(Path(a.edit).read_text(encoding="utf-8"))
    out, log, errors = [], [f"# Правка сидов {ed['edit_id']} ({ed['date']})", "", ed["principle"], ""], []
    for s in seeds:
        text, applied = s["prompt"], []
        for r in ed["replace"]:
            target = (r.get("seed_id") == s["seed_id"]) or (s["risk"] in r.get("risk", []))
            if not target:
                continue
            if text.count(r["old"]) != 1:
                errors.append(f"{s['seed_id']}: «{r['old'][:50]}…» найдено {text.count(r['old'])} раз, ожидалось 1")
                continue
            text = text.replace(r["old"], r["new"])
            applied.append({"kind": "replace", "why": r["why"]})
        tail = ed["append"].get(s["risk"])
        if tail:
            text = text.rstrip("\n") + "\n\n" + "\n".join(tail) + "\n"
            applied.append({"kind": "append_checklist", "why": "повтор ограничений сида в конце промпта"})
        if applied:
            new = {**s, "prompt": text, "version": f"{s.get('version', '?')}-{ed['edit_id']}",
                   "edit": {"id": ed["edit_id"], "base_prompt_sha256": hashlib.sha256(s["prompt"].encode()).hexdigest(),
                            "changes": applied}}
            diff = difflib.unified_diff(s["prompt"].splitlines(), text.splitlines(), lineterm="", n=0)
            log += [f"## {s['seed_id']}", "```diff", *list(diff)[2:], "```", ""]
            out.append(new)
        else:
            out.append(s)
    if errors:
        print("ошибка:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 2
    d = Path(a.out)
    d.mkdir(parents=True, exist_ok=True)
    (d / "all.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out), encoding="utf-8")
    (d / "CHANGELOG.md").write_text("\n".join(log) + "\n", encoding="utf-8")
    n = sum(1 for x in out if "edit" in x)
    print(f"изменено {n} из {len(out)} seed → {d}/all.jsonl, diff в {d}/CHANGELOG.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
