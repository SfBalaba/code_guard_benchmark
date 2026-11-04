"""Шаг 5: проверка. deduped.jsonl -> validated.jsonl + rejected_validate.jsonl + review_queue.jsonl.

Ни одна команда не исполняется: синтаксис проверяется через `bash -n`
(режим noexec — bash только разбирает текст), флаги — по словарю из man-страниц
(flagcheck), метки — правилами-якорями (anchors).

review_queue.jsonl — прошедшие строки, метку которых правило-якорь считает сомнительной:
их надо посмотреть человеку в первую очередь.
"""
import re
import shutil
import subprocess

from . import anchors, flagcheck
from .config import run_dir
from .io import read_jsonl, write_jsonl

SECRET_RE = re.compile(
    r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"
    r"|\bgh[pousr]_[A-Za-z0-9]{25,}"
    r"|\bAKIA[A-Z0-9]{16}\b"
    r"|\bsk-[A-Za-z0-9_-]{20,}"
    r"|\bxox[abpr]-[A-Za-z0-9-]{10,}"
)


def bash_syntax_ok(cmd):
    """True/False, или None если bash недоступен."""
    bash = shutil.which("bash")
    if not bash:
        return None
    try:
        r = subprocess.run([bash, "-n", "-c", cmd], capture_output=True, timeout=5,
                           stdin=subprocess.DEVNULL, env={"PATH": "/usr/bin:/bin"})
    except subprocess.TimeoutExpired:
        return False
    return r.returncode == 0


def check(c, cfg):
    """Список причин отклонения и список предупреждений."""
    reasons, warnings = [], []
    if c["class"] not in cfg["labels"]["classes"]:
        reasons.append(f"bad_class:{c['class']}")
    if c["severity"] not in cfg["labels"]["severities"]:
        reasons.append(f"bad_severity:{c['severity']}")
    for field in ("command", "description", "util"):
        if SECRET_RE.search(c[field]):
            reasons.append(f"possible_secret_in_{field}")
    if cfg["validate"]["bash_syntax_check"]:
        ok = bash_syntax_ok(c["command"])
        if ok is False:
            reasons.append("bash_syntax_error")
        elif ok is None:
            warnings.append("bash_not_found_syntax_unchecked")
    flag_problems = []
    mode = cfg["validate"].get("flag_check", "reject")
    if mode != "off":
        flag_problems, flag_warn = flagcheck.check(
            c["command"], cfg["validate"].get("flags_dir") or flagcheck.DEFAULT_DIR)
        (reasons if mode == "reject" else warnings).extend(flag_problems)
        warnings.extend(flag_warn)
    if cfg["validate"].get("label_anchors", True) and c["class"] in cfg["labels"]["classes"]:
        warnings.extend(anchors.check(c, cfg["labels"]["classes"], allow_read_only=not flag_problems))
    # util может быть намеренно спрятан (обфускация), поэтому это предупреждение, а не отказ
    if c["util"] not in c["command"]:
        warnings.append("util_not_literal_in_command")
    return reasons, warnings


def run(cfg, log=print):
    out = run_dir(cfg)
    kept, rejected = [], []
    for c in read_jsonl(out / "deduped.jsonl"):
        reasons, warnings = check(c, cfg)
        if reasons:
            rejected.append({**c, "stage": "validate", "reason": ";".join(reasons)})
        else:
            kept.append({**c, "warnings": warnings})
    write_jsonl(out / "validated.jsonl", kept)
    write_jsonl(out / "rejected_validate.jsonl", rejected)
    review = [c for c in kept if any(w.startswith("label_conflict:") for w in c["warnings"])]
    write_jsonl(out / "review_queue.jsonl", review)
    log(f"validate: прошло {len(kept)}, отброшено {len(rejected)}, на ревью (label_conflict) {len(review)}")
    return kept, rejected
