"""Шаг 4b: near-duplicate фильтр. deduped.jsonl -> neardeduped.jsonl + rejected_neardup.jsonl.

Exact-dedup (шаг 4) ловит только побайтно совпадающие команды. Здесь — близкие: один сид при
samples>=4 плодит варианты-близнецы, а сиды CAT-5 разрешают не больше N близких вариантов рецепта.
Без этого шага лимиты рецептов фиктивны, а разнообразие пула мнимое.

Две проверки, обе лексические (без зависимостей и GPU), сходство — Jaccard по символьным k-граммам
нормализованной команды (комментарии-заголовки убраны, как в dedup.normalize):
  1. ВНУТРИ прогона: жадная кластеризация — пара отбрасывается, если её risky-команда (для не-пар —
     сама команда) ближе порога к уже оставленной; плюс cap на число пар с одним family_id.
  2. ПРОТИВ test (neardup.against_test): та же мера против команд из dedup.against. Exact-dedup роняет
     только побайтные совпадения train↔test; здесь добавляется near-leak (близнецы, отличающиеся лишь
     хостом/портом/именем файла), который иначе завышает метрики guard. Семантический near-dup по
     эмбеддингам можно добавить позже отдельным режимом.
"""
from .config import run_dir
from .dedup import against_files, normalize
from .io import read_commands, read_jsonl, write_jsonl

def shingles(cmd, k=4):
    """Символьные k-граммы нормализованной команды. На коротких командах они устойчивее токенных:
    команды-близнецы (отличаются только хостом/именем файла) дают высокий Jaccard, а разные рецепты —
    низкий (откалибровано на реальных парах: близнецы >=0.56, разные <=0.19 при k=4)."""
    t = normalize(cmd)
    return frozenset(t[i:i + k] for i in range(len(t) - k + 1)) if len(t) >= k else frozenset([t])


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _units(rows):
    """Сгруппировать записи в единицы: пара (по pair_id) или одиночная запись.
    Возвращает список (records, repr_command, family_id)."""
    pairs, singles = {}, []
    for r in rows:
        if r.get("pair_id"):
            pairs.setdefault(r["pair_id"], []).append(r)
        else:
            singles.append(r)
    units = []
    for recs in pairs.values():
        risky = next((x for x in recs if x.get("role") == "risky"), recs[0])
        units.append((recs, risky["command"], risky.get("family_id", "")))
    for r in singles:
        units.append(([r], r["command"], r.get("family_id", "")))
    return units


def _load_test_sigs(cfg, k, log):
    """Сигнатуры команд из dedup.against (те же файлы, что и для exact-dedup)."""
    sigs = []
    for path in against_files(cfg):
        for c in read_commands(path):
            t = normalize(c)
            sigs.append((len(t), shingles(c, k)))
    log(f"neardup: команд test для сверки (against_test): {len(sigs)}")
    return sigs


def run(cfg, log=print):
    out = run_dir(cfg)
    nd = cfg.get("neardup", {})
    rows = read_jsonl(out / "deduped.jsonl")
    if not nd.get("enabled", False):
        write_jsonl(out / "neardeduped.jsonl", rows)
        write_jsonl(out / "rejected_neardup.jsonl", [])
        log("neardup: выключен (neardup.enabled=false) — пропускаю")
        return rows, []
    thr = nd.get("threshold", 0.8)
    k = nd.get("shingle_k", 3)
    default_cap = nd.get("family_cap")
    caps = nd.get("family_cap_by_risk", {})
    test_sigs = _load_test_sigs(cfg, k, log) if nd.get("against_test", False) else []
    test_thr = nd.get("test_threshold", thr)

    def near_test(sig, tlen):
        """Ближайшая test-команда >= test_thr, иначе None. Префильтр по длине: близнецы по символьным
        k-граммам не могут сильно различаться длиной, так что далёкие по длине пропускаем."""
        for L, ts in test_sigs:
            if tlen and (L < tlen * 0.5 or L > tlen * 2):
                continue
            j = jaccard(sig, ts)
            if j >= test_thr:
                return j
        return None

    kept, rejected, kept_sig, fam_count = [], [], [], {}
    for recs, cmd, fam in _units(rows):
        risk = recs[0].get("risk", "")
        cap = caps.get(risk, default_cap)
        sig = shingles(cmd, k)
        dup = next(((j, jaccard(sig, s)) for j, s in enumerate(kept_sig) if jaccard(sig, s) >= thr), None)
        if dup is not None:
            for r in recs:
                rejected.append({**r, "stage": "neardup", "reason": "near_duplicate",
                                 "similarity": round(dup[1], 3)})
            continue
        if test_sigs:
            # против test сверяется КАЖДАЯ сторона пары (safe тоже может быть близнецом test-строки allow)
            jt = next((j for j in (near_test(shingles(r["command"], k), len(normalize(r["command"])))
                                   for r in recs) if j is not None), None)
            if jt is not None:
                for r in recs:
                    rejected.append({**r, "stage": "neardup", "reason": "near_duplicate_test",
                                     "similarity": round(jt, 3)})
                continue
        if cap is not None and fam_count.get(fam, 0) >= cap:
            for r in recs:
                rejected.append({**r, "stage": "neardup", "reason": f"family_cap:{cap}", "family_id": fam})
            continue
        kept_sig.append(sig)
        fam_count[fam] = fam_count.get(fam, 0) + 1
        kept.extend(recs)
    write_jsonl(out / "neardeduped.jsonl", kept)
    write_jsonl(out / "rejected_neardup.jsonl", rejected)
    n_test = sum(1 for r in rejected if r.get("reason") == "near_duplicate_test")
    log(f"neardup: оставлено {len(kept)}, отброшено {len(rejected)} "
        f"(порог {thr}, shingle {k}, cap {default_cap or caps or 'нет'}"
        f"{f', vs test {test_thr}: -{n_test}' if test_sigs else ''})")
    return kept, rejected
