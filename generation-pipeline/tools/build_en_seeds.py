"""Собрать английские сиды из каркаса (cores/) и заполненных полей (parts/ для CAT-1.4, worksheet/ для CAT-5.x).

    python3 tools/build_en_seeds.py --out seeds/en

Берёт метаданные (split, family_id, origin, mechanism) из seeds/train/all.jsonl, подставляет английские
поля в шаблон и пишет <out>/all.jsonl в том же JSONL-формате, что ждёт cgen. version -> "<старая>-en1".
Падает, если хоть одно английское поле пустое: недозаполненный рабочий лист не соберётся молча.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cgen.io import read_jsonl  # noqa: E402

FIELD = re.compile(r"\{(\w+)\}")


def fill(template, values):
    missing = [k for k in FIELD.findall(template) if not str(values.get(k, "")).strip()]
    if missing:
        raise ValueError(f"пустые поля {missing}")
    # только простые {name}: фигурные скобки JSON-примера в шаблоне не трогаем (они не \w-имена с одним словом? trebує care)
    return FIELD.sub(lambda m: str(values[m.group(1)]) if m.group(1) in values else m.group(0), template)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default="seeds/en")
    a = p.parse_args(argv)
    d = ROOT / a.out
    base = {s["seed_id"]: s for s in read_jsonl(ROOT / "seeds/train/all.jsonl")}
    core14 = (d / "cores/CAT-1.4.md").read_text(encoding="utf-8")
    core5 = (d / "cores/CAT-5_common.md").read_text(encoding="utf-8")
    out, errors = [], []

    def emit(sid, prompt):
        s = base[sid]
        out.append({**s, "prompt": prompt, "version": f"{s.get('version', '?')}-en1",
                    "edit": {"id": "en1", "note": "English rewrite (iteration 3); CAT-1.4 by Claude, CAT-5.x by Vlad+Anna"}})

    # CAT-1.4: per-seed English fields from src/CAT-1.4.json (переведено Владом+Аней)
    p14 = json.loads((d / "src/CAT-1.4.json").read_text(encoding="utf-8"))
    for sid, f in p14.items():
        try:
            emit(sid, fill(core14, {"seed_id": sid, **f}))
        except ValueError as e:
            errors.append(f"{sid}: {e}")

    # CAT-5.x: per-seed English from src/, shared risk/safe blocks from worksheet/
    for sf in sorted((d / "src").glob("CAT-5.*.json")):
        risk = sf.stem
        per = json.loads(sf.read_text(encoding="utf-8"))
        w = json.loads((d / "worksheet" / sf.name).read_text(encoding="utf-8"))
        rb, sb = w.get("shared_en_risk_block", ""), w.get("shared_en_safe_block", "")
        if not rb.strip() or not sb.strip():
            errors.append(f"worksheet/{sf.name}: пустые shared_en_risk_block/shared_en_safe_block")
            continue
        for sid, f in per.items():
            vals = {"seed_id": sid, "title": f.get("title", ""), "main_utility": f.get("main_utility", ""),
                    "special_task": f.get("special_task", ""), "risk_block": rb, "safe_block": sb}
            try:
                emit(sid, fill(core5, vals))
            except ValueError as e:
                errors.append(f"{sid}: {e}")

    if errors:
        print("не собрано (заполни рабочие листы):\n  " + "\n  ".join(errors), file=sys.stderr)
        return 2
    missing = sorted(set(base) - {o["seed_id"] for o in out})
    if missing:
        print(f"нет части для сидов: {missing}", file=sys.stderr)
        return 2
    (d / "all.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out), encoding="utf-8")
    print(f"собрано {len(out)} английских сидов -> {d}/all.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
