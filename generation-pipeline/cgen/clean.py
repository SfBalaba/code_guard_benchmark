"""Шаг 3: очистка. raw.jsonl -> candidates.jsonl + rejected_clean.jsonl.

Достаёт JSON из ответа модели и убирает типичный мусор. Всё, что исправлено,
записывается в поле fixes; всё, что отброшено, — в rejected_clean.jsonl с причиной.
"""
import json
import re
import unicodedata

from .config import run_dir
from .io import digest, read_jsonl_tolerant, write_jsonl

THINK_RE = re.compile(r"<think>.*?</think>", re.S | re.I)
FENCE_RE = re.compile(r"```(?:json|JSON)?\s*(.*?)```", re.S)
# Письменности, которых не должно быть в bash-команде: CJK, кана, хангыль, арабская и др.
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
# Заголовки контекста, которые требуют сиды (# TASK: / # FS: / # ENV:), на любом языке.
HEADER_RE = re.compile(r"^\s*#\s*(TASK|FS|ENV)\b", re.I)
FOREIGN_RE = re.compile(r"[؀-ۿ฀-๿぀-ヿ㐀-䶿一-鿿가-힯豈-﫿]")
CANDIDATE_FIELDS = ("command", "description", "util", "class", "severity")
# В парном формате метки модели необязательны: часть сидов запрещает модели их ставить.
PAIR_FIELDS = ("command", "description", "util")


def extract_json(raw):
    """Вернуть (obj, fixes) или бросить ValueError с причиной."""
    fixes = []
    text = raw.strip()
    if THINK_RE.search(text):
        text = THINK_RE.sub("", text).strip()
        fixes.append("removed_think_block")
    m = FENCE_RE.search(text)
    if m:
        text = m.group(1).strip()
        fixes.append("removed_markdown_fence")
    if not text.startswith("{"):
        i, j = text.find("{"), text.rfind("}")
        if i == -1 or j <= i:
            raise ValueError("no_json_object")
        text = text[i:j + 1]
        fixes.append("trimmed_text_around_json")
    try:
        return json.loads(text), fixes
    except json.JSONDecodeError:
        raise ValueError("invalid_json") from None


def clean_command(cmd, cfg):
    """Вернуть (cmd, fixes) или бросить ValueError с причиной."""
    fixes = []
    c = unicodedata.normalize("NFC", cmd).strip()
    if len(c) >= 2 and c[0] == c[-1] == "`" and c.count("`") == 2:
        c = c[1:-1].strip()
        fixes.append("removed_backticks")
    if c.startswith("$ "):
        c = c[2:].lstrip()
        fixes.append("removed_prompt_sign")
    # Признак переэкранирования: все кавычки в команде идут как \" — модель экранировала их дважды.
    n_q, n_esc = c.count('"'), c.count('\\"')
    if n_q and n_q == n_esc:
        c = c.replace('\\"', '"')
        fixes.append("unescaped_quotes")
    c = "\n".join(line.rstrip() for line in c.splitlines())
    if cfg["clean"].get("strip_cyrillic_comment_lines"):
        # Сиды требуют заголовки # TASK/# FS на русском. Это не сигнал команды и может подсказывать метку,
        # поэтому целые строки-комментарии с кириллицей вырезаются (shebang #! не трогаем).
        lines = c.splitlines()
        kept = [ln for ln in lines if not (ln.lstrip().startswith("#") and not ln.lstrip().startswith("#!")
                                           and (CYRILLIC_RE.search(ln) or HEADER_RE.match(ln)))]
        if len(kept) != len(lines):
            c = "\n".join(kept).strip("\n")
            fixes.append("removed_header_comment_lines")
    if not c.strip():
        raise ValueError("empty_command")
    if len(c) > cfg["clean"]["max_command_chars"]:
        raise ValueError("command_too_long")
    if FOREIGN_RE.search(c):
        raise ValueError("foreign_script_in_command")
    if any(unicodedata.category(ch) == "Cc" and ch not in "\n\t" for ch in c):
        raise ValueError("control_chars_in_command")
    if not cfg["clean"]["allow_non_ascii_command"] and not c.isascii():
        raise ValueError("non_ascii_command")
    return c, fixes


def _clean_one(c, cfg, fields=CANDIDATE_FIELDS):
    """Почистить одного кандидата: вернуть (cmd, desc, fixes) или бросить ValueError с причиной."""
    if not isinstance(c, dict):
        raise ValueError("candidate_not_object")
    missing = [k for k in fields if not isinstance(c.get(k), str) or not c[k].strip()]
    if missing:
        raise ValueError(f"missing_fields:{','.join(missing)}")
    cmd, fixes = clean_command(c["command"], cfg)
    desc = " ".join(c["description"].split())
    if FOREIGN_RE.search(desc):
        raise ValueError("foreign_script_in_description")
    return cmd, desc, fixes


def pair_labels(cfg, risk, role, c):
    """Метка стороны пары по контракту сида (labels.pair_contract).

    Возвращает (class, severity, fixes, warnings). Метка модели (expected_class/severity),
    если она есть и допустима контрактом, сохраняется; иначе ставится первая допустимая
    из контракта, а расхождение уходит в label_conflict -> review_queue.
    Нет контракта для risk — ValueError: метки сами не выдумываем.
    """
    contract = cfg["labels"].get("pair_contract", {}).get(risk)
    if not contract or role not in contract:
        raise ValueError(f"no_pair_contract:{risk}")
    allowed = [tuple(x) for x in contract[role]]
    # Модели пишут в поле класса что угодно: «risky», «rce», «risky/deny/critical». Берём из обоих полей
    # только слова из словаря меток; слово ровно одно — это метка модели, иначе метки модели нет.
    said = " ".join(str(c.get(k) or "") for k in ("expected_class", "class", "severity")).lower()
    words = re.findall(r"[a-z]+", said)
    cls_found = {w for w in words if w in cfg["labels"]["classes"]}
    sev_found = {w for w in words if w in cfg["labels"]["severities"]}
    m_cls = cls_found.pop() if len(cls_found) == 1 else None
    m_sev = sev_found.pop() if len(sev_found) == 1 else None
    vocab_fix = ["label_vocab_ignored"] if said.strip() and not (m_cls or m_sev) else []
    default = f"{allowed[0][0]}/{allowed[0][1]}"
    # Контрактные метки, совместимые с тем, что модель всё-таки сказала (класс и/или severity).
    fits = [x for x in allowed if (m_cls is None or x[0] == m_cls) and (m_sev is None or x[1] == m_sev)]
    if len(fits) == 1:
        src = ["label_from_model"] if (m_cls and m_sev) else (
            ["label_partly_from_model"] if (m_cls or m_sev) else ["label_from_seed_contract"] + vocab_fix)
        return fits[0][0], fits[0][1], src, []
    if not fits:  # модель назвала метку, которую контракт не допускает
        return allowed[0][0], allowed[0][1], ["label_from_seed_contract"], [
            f"label_conflict:model={m_cls or '?'}/{m_sev or '?'}:contract={default}"]
    # несколько допустимых, а модель не выбрала однозначно — решает человек
    return allowed[0][0], allowed[0][1], ["label_from_seed_contract"] + vocab_fix, [
        f"label_conflict:model={m_cls or 'none'}/{m_sev or 'none'}:contract_ambiguous="
        f"{'|'.join(a + '/' + b for a, b in allowed)}"]


def _pair_records(r, obj, resp_fixes, cfg, base):
    """Ответ формата {"risky":…,"safe":…,"review":…} -> (kept, rejected). Пара живёт или отбрасывается целиком."""
    pair_id = f"{r['seed_id']}#{r['sample_idx']}"
    out, problems = [], []
    for i, role in enumerate(("risky", "safe")):
        c = obj.get(role)
        try:
            cmd, desc, fixes = _clean_one(c, cfg, PAIR_FIELDS)
            cls, sev, lfix, warns = pair_labels(cfg, r["risk"], role, c)
        except ValueError as exc:
            problems.append(f"{role}:{exc}")
            continue
        out.append({
            **base, "cand_idx": i, "pair_id": pair_id, "role": role,
            "record_id": digest([r["seed_id"], r["sample_idx"], i, cmd])[:16],
            "command": cmd, "description": desc, "util": c["util"].strip(),
            "class": cls, "severity": sev, "fixes": resp_fixes + fixes + lfix, "warnings": warns,
            "review": obj.get("review"),
        })
    rej = lambda reason, **kw: ([], [{**base, "pair_id": pair_id, "stage": "clean", "reason": reason, **kw}])
    if problems:
        return rej("pair_rejected:" + ";".join(problems), raw=r["raw"][:2000])
    # Сиды: «конфликтующие кандидаты исключаются» — метку не подменяем, пара уходит целиком.
    conflicts = [w for x in out for w in x["warnings"] if w.startswith("label_conflict:")]
    if conflicts:
        return rej("pair_label_conflict", details=conflicts)
    # Сиды требуют одну основную утилиту на обе стороны пары. Модель иногда перечисляет несколько
    # («cp, ed»): пара годится, если основная утилита общая; в колонку util идёт она.
    split_utils = lambda u: [x for x in re.split(r"[\s,;/+|&]+", u.lower()) if x and x != "and"]
    ur, us = split_utils(out[0]["util"]), split_utils(out[1]["util"])
    common = [x for x in ur if x in us]
    if not common:
        return rej("pair_util_mismatch", details=[out[0]["util"], out[1]["util"]])
    if out[0]["util"].lower() != out[1]["util"].lower():
        for x in out:
            x["util"] = common[0]
            x["fixes"].append("util_normalized")
    if out[0]["command"] == out[1]["command"]:
        return rej("pair_identical_commands")
    return out, []


def run(cfg, log=print):
    out = run_dir(cfg)
    raws = [r for r in read_jsonl_tolerant(out / "raw.jsonl") if r["status"] == "ok"]
    kept, rejected, seen_ids = [], [], set()
    n_pairs = n_refused = 0
    for r in raws:
        base = {k: r[k] for k in ("seed_id", "sample_idx", "risk", "family_id")}
        if "model" in r:
            base["model"] = r["model"]
        try:
            obj, resp_fixes = extract_json(r["raw"])
            if not isinstance(obj, dict):
                raise ValueError("no_candidates_list")
        except ValueError as exc:
            rejected.append({**base, "stage": "clean", "reason": str(exc), "raw": r["raw"][:2000]})
            continue
        # Формат 1: модель отказалась по контракту сида ({"rejected": true, "reason": ...}).
        if obj.get("rejected"):
            n_refused += 1
            rejected.append({**base, "stage": "clean", "reason": "model_refused",
                             "model_reason": str(obj.get("reason", ""))[:500]})
            continue
        # Формат 2: пара risky/safe (сиды коллег, шаблон v2).
        if "risky" in obj or "safe" in obj:
            recs, rej = _pair_records(r, obj, resp_fixes, cfg, base)
            rejected += rej
            n_pairs += bool(recs)
            for x in recs:
                if x["record_id"] not in seen_ids:
                    seen_ids.add(x["record_id"])
                    kept.append(x)
            continue
        # Формат 3: список кандидатов (шаблон v1).
        cands = obj.get("candidates")
        if not isinstance(cands, list) or not cands:
            rejected.append({**base, "stage": "clean", "reason": "no_candidates_list", "raw": r["raw"][:2000]})
            continue
        for i, c in enumerate(cands):
            item = {**base, "cand_idx": i}
            try:
                cmd, desc, fixes = _clean_one(c, cfg)
            except ValueError as exc:
                rejected.append({**item, "stage": "clean", "reason": str(exc), "candidate": c})
                continue
            rid = digest([r["seed_id"], r["sample_idx"], i, cmd])[:16]
            if rid in seen_ids:
                continue
            seen_ids.add(rid)
            kept.append({
                **item, "record_id": rid, "command": cmd, "description": desc,
                "util": c["util"].strip(), "class": c["class"].strip().lower(),
                "severity": c["severity"].strip().lower(), "fixes": resp_fixes + fixes,
            })
    write_jsonl(out / "candidates.jsonl", kept)
    write_jsonl(out / "rejected_clean.jsonl", rejected)
    extra = f", пар {n_pairs}, отказов модели {n_refused}" if n_pairs or n_refused else ""
    log(f"clean: вызовов {len(raws)}, кандидатов оставлено {len(kept)}, отброшено {len(rejected)}{extra}")
    return kept, rejected
