"""Собрать английские сиды из каркаса (cores/) и заполненных полей (parts/ для CAT-1.4, worksheet/ для CAT-5.x).

    python3 tools/build_en_seeds.py --out seeds/en

Берёт метаданные (split, family_id, origin, mechanism) из seeds/train/all.jsonl, подставляет английские
поля в шаблон и пишет <out>/all.jsonl в том же JSONL-формате, что ждёт cgen. version -> "<старая>-en1".
Падает, если хоть одно английское поле пустое: недозаполненный рабочий лист не соберётся молча.

Отдельная категория (CAT-4, CAT-6.1 …) — --cat, ничего из v0 (all.jsonl/v0.jsonl) не трогается:
    python3 tools/build_en_seeds.py --cat CAT-4
База — seeds/train/<cat>.jsonl (русские оригиналы, фолбэк), каркас cores/<cat>.md, необязательные блоки риска
cores/<cat>_risks.json ({risk: текст} -> {risk_block}), поля сида parts/<cat>.json. Служебные ключи parts:
  "_meta": {"en_version": N, "method": {seed_id|"*": "claude"|"local-qwen"|…}},
  "_dropped": {seed_id: причина} — сид исключается (стена возможностей моделей), файл сида остаётся.
Итог: seeds/en/<cat>.jsonl, version "<старая>-en<N>", поле edit с методом перевода и правками.
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


def build_cat(d, cat):
    """Английские сиды одной категории -> <d>/<cat>.jsonl. Возвращает код выхода."""
    base = read_jsonl(ROOT / f"seeds/train/{cat}.jsonl")
    core = (d / f"cores/{cat}.md").read_text(encoding="utf-8")
    rp = d / f"cores/{cat}_risks.json"
    risks = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
    parts = json.loads((d / f"parts/{cat}.json").read_text(encoding="utf-8"))
    meta, dropped = parts.pop("_meta", {}), parts.pop("_dropped", {})
    ver, method = meta.get("en_version", 1), meta.get("method", {})
    out, errors = [], []
    for s in base:
        sid = s["seed_id"]
        if sid in dropped:
            continue
        f = parts.get(sid)
        if f is None:
            errors.append(f"{sid}: нет части в parts/{cat}.json")
            continue
        vals = {"seed_id": sid, **({"risk_block": risks[s["risk"]]} if s["risk"] in risks else {}),
                **{k: v for k, v in f.items() if not k.startswith("_") and k not in ("translator_notes", "edits")}}
        try:
            prompt = fill(core, vals)
        except ValueError as e:
            errors.append(f"{sid}: {e}")
            continue
        if re.search(r"[\u0400-\u04FF]", prompt):
            errors.append(f"{sid}: в английском сиде осталась кириллица")
            continue
        out.append({**s, "prompt": prompt, "version": f"{s.get('version', '?')}-en{ver}",
                    "edit": {"id": f"en{ver}", "method": method.get(sid, method.get("*", "unknown")),
                             "edits": f.get("edits", []),
                             "note": f"English rewrite of {cat}; Russian original kept in seeds/train/{cat}.jsonl"}})
    unknown = sorted(set(parts) - {s["seed_id"] for s in base})
    if unknown:
        errors.append(f"в parts есть сиды, которых нет в базе: {unknown}")
    if errors:
        print("не собрано:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 2
    (d / f"{cat}.jsonl").write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out), encoding="utf-8")
    print(f"собрано {len(out)} английских сидов {cat} (en{ver}; исключено {len(dropped)}) -> {d}/{cat}.jsonl")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default="seeds/en")
    p.add_argument("--cat", help="собрать только эту категорию (CAT-4, CAT-6.1 …) в <out>/<cat>.jsonl")
    a = p.parse_args(argv)
    d = ROOT / a.out
    if a.cat:
        return build_cat(d, a.cat)
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
