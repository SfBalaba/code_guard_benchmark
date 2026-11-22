"""Загрузить ответ другой модели (risk_block/safe_block по CAT-5.N) в worksheet/*.json.

    python3 tools/load_fill.py --in returned.json

Ждёт JSON {"CAT-5.1":{"risk_block":"...","safe_block":"..."}, ...}. Пишет shared_en_risk_block и
shared_en_safe_block в соответствующие seeds/en/worksheet/CAT-5.N.json. Пустые значения отклоняет.
Остальное в worksheet не трогает. После загрузки запусти python3 tools/build_en_seeds.py.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT / "seeds/en/worksheet"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--in", dest="inp", required=True)
    a = p.parse_args(argv)
    data = json.loads(Path(a.inp).read_text(encoding="utf-8"))
    errors, done = [], []
    for risk, blocks in data.items():
        wf = WS / f"{risk}.json"
        if not wf.exists():
            errors.append(f"{risk}: нет {wf}")
            continue
        rb, sb = blocks.get("risk_block", ""), blocks.get("safe_block", "")
        if not rb.strip() or not sb.strip():
            errors.append(f"{risk}: пустой risk_block/safe_block")
            continue
        w = json.loads(wf.read_text(encoding="utf-8"))
        w["shared_en_risk_block"] = rb.strip()
        w["shared_en_safe_block"] = sb.strip()
        wf.write_text(json.dumps(w, ensure_ascii=False, indent=1), encoding="utf-8")
        done.append(risk)
    if errors:
        print("ошибки:\n  " + "\n  ".join(errors), file=sys.stderr)
    print(f"загружено: {sorted(done)}")
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
