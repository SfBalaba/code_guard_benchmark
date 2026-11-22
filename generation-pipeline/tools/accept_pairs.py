"""Пул принятых пар из ревью-итераций: runs/review/iter*/verdicts.jsonl (verdict=good) -> runs/review/accepted/.

    python3 tools/accept_pairs.py

Пул пересобирается целиком при каждом запуске (идемпотентно). Берутся только пары, которые прошли весь
cgen (есть в dataset.csv модели) И получили verdict=good. Обе стороны пары — или ни одной.
В provenance: модель, итерация, версия seed, reviewer, why; human_reviewed остаётся false —
ревью модели не человеческая проверка. В v0 пул идёт только после near-dup и лимитов на рецепт.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cgen.io import FIELDS, read_jsonl, write_csv, write_jsonl  # noqa: E402


def main():
    review = ROOT / "runs/review"
    rows, prov, missing, dups, seen_cmds = [], [], [], [], set()
    for it in sorted(review.glob("iter*"), key=lambda p: int(p.name[4:]) if p.name[4:].isdigit() else 0):
        vpath = it / "verdicts.jsonl"
        if not vpath.exists():
            continue
        meta = json.loads((it / "meta.json").read_text(encoding="utf-8"))
        for v in read_jsonl(vpath):
            if v["verdict"] != "good":
                continue
            d = it / v["model"]
            with open(d / "dataset.csv", newline="", encoding="utf-8") as f:
                ds = list(csv.DictReader(f))
            pv = read_jsonl(d / "provenance.jsonl")
            sides = [(r, p) for r, p in zip(ds, pv) if p.get("pair_id") == v["pair_id"]]
            if {p["role"] for _, p in sides} != {"risky", "safe"}:
                missing.append(f"{it.name}/{v['model']}/{v['pair_id']}")
                continue
            # дедуп по пулу: одна и та же команда из разных итераций/моделей не считается дважды
            keys = {" ".join(r["command"].split()) for r, _ in sides}
            if keys & seen_cmds:
                dups.append(f"{it.name}/{v['model']}/{v['pair_id']}")
                continue
            seen_cmds |= keys
            for r, p in sides:
                fix = (v.get("relabel") or {}).get(p["role"])   # {"risky": ["deny", "critical"]} — правка метки ревьюером
                if fix:
                    p = {**p, "relabeled_from": [r["class"], r["severity"]]}
                    r = {**r, "class": fix[0], "severity": fix[1]}
                rows.append(r)
                prov.append({**p, "row": len(rows), "iteration": it.name, "model": v["model"],
                             "gguf_sha256": meta["models"][v["model"]]["gguf_sha256"], "seeds_file": meta["seeds"],
                             "reviewer": v["reviewer"], "review_verdict": v["verdict"], "review_why": v["why"],
                             "human_reviewed": False})
    out = review / "accepted"
    write_csv(out / "dataset.csv", rows)
    write_jsonl(out / "provenance.jsonl", prov)
    if missing:
        print("ВНИМАНИЕ: good-вердикт, но пары нет в dataset.csv (отсеяна пайплайном):", missing, file=sys.stderr)
    if dups:
        print("пропущены как дубли уже принятых команд:", dups, file=sys.stderr)
    print(f"принято пар: {len(rows) // 2} ({len(rows)} строк) -> {out}/")
    assert all(list(r) == FIELDS for r in rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
