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
FOREIGN_RE = re.compile(r"[؀-ۿ฀-๿぀-ヿ㐀-䶿一-鿿가-힯豈-﫿]")
CANDIDATE_FIELDS = ("command", "description", "util", "class", "severity")


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
    if not c:
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


def run(cfg, log=print):
    out = run_dir(cfg)
    raws = [r for r in read_jsonl_tolerant(out / "raw.jsonl") if r["status"] == "ok"]
    kept, rejected, seen_ids = [], [], set()
    for r in raws:
        base = {k: r[k] for k in ("seed_id", "sample_idx", "risk", "family_id")}
        try:
            obj, resp_fixes = extract_json(r["raw"])
            cands = obj.get("candidates") if isinstance(obj, dict) else None
            if not isinstance(cands, list) or not cands:
                raise ValueError("no_candidates_list")
        except ValueError as exc:
            rejected.append({**base, "stage": "clean", "reason": str(exc), "raw": r["raw"][:2000]})
            continue
        for i, c in enumerate(cands):
            item = {**base, "cand_idx": i}
            if not isinstance(c, dict):
                rejected.append({**item, "stage": "clean", "reason": "candidate_not_object"})
                continue
            missing = [k for k in CANDIDATE_FIELDS if not isinstance(c.get(k), str) or not c[k].strip()]
            if missing:
                rejected.append({**item, "stage": "clean", "reason": f"missing_fields:{','.join(missing)}", "candidate": c})
                continue
            try:
                cmd, fixes = clean_command(c["command"], cfg)
            except ValueError as exc:
                rejected.append({**item, "stage": "clean", "reason": str(exc), "candidate": c})
                continue
            desc = " ".join(c["description"].split())
            if FOREIGN_RE.search(desc):
                rejected.append({**item, "stage": "clean", "reason": "foreign_script_in_description", "candidate": c})
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
    log(f"clean: вызовов {len(raws)}, кандидатов оставлено {len(kept)}, отброшено {len(rejected)}")
    return kept, rejected
