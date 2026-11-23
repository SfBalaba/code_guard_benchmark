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

# Хвост сериализации python/json, просочившийся в команду от самой модели:
# команда оканчивается на `…', 'file'` или `…', "file"` (кавычка-запятая-кавычка-…-кавычка-конец).
# bash -n это пропускает (кавычки сбалансированы), но это не валидная команда. См. validator WARN-3.
TRAILING_LIST_RE = re.compile(r"""['"]\s*,\s*['"][^'"]*['"]\s*$""")

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


# Утечка «обвязки» ответа модели в command (найдено валидатором на CAT-4, 23.11): HEADER_RE в clean
# снимает только однострочные # TASK/# FS, а модели пишут многострочные описания стенда, рассуждения,
# метки сторон и приглашение shell. Такие строки не команда и не обфускация — пару отбрасываем целиком.
_FS_WORDS = r"(?:file|dir|directory|symlink|regular file|executable|socket|fifo)"
CONTAMINATION = [
    # приглашение shell: root@host:/path# cmd, /path $ cmd
    ("prompt_prefix", re.compile(r"^\s*[\w.-]+@[\w.-]+(?::\S*)?\s*[#$]\s+\S", re.M)),
    ("prompt_prefix", re.compile(r"^\s*(?:/|\./|~)\S*\s+\$\s+\S", re.M)),
    # пользователь как первое слово команды: «root date …»
    ("user_prefix", re.compile(r"\A\s*(?:root|user)\s+[a-z]")),
    # рассуждения / самоисправления / метки сторон в комментариях
    ("model_reasoning", re.compile(
        r"^\s*#\s*\(?\s*(?:wait\b|corrected|correction|actually\b|hmm\b|since we|assume|assuming|implicitly|"
        r"risky\b|safe\b)", re.M | re.I)),
    # описание стенда: «# CWD:», «# dir:», «# SHELL OPTIONS:», «# VARIABLES:»
    ("fs_listing", re.compile(r"^\s*#\s*(?:CWD|SHELL OPTIONS?|VARIABLES?|dir|file|files|PRECONDITIONS?)\s*:", re.M | re.I)),
    # строка-листинг без #: «/path: file 0644 root:root», «# /path (regular file, mode 644 …»
    ("fs_listing", re.compile(r"^\s*#?\s*(?:/|\./)\S+\s*(?::\s*|\()\s*" + _FS_WORDS + r"\b", re.M | re.I)),
    # комментарий-описание объекта: «# /path: type=file, owner=root …», «# type: file, path: …»
    ("fs_listing", re.compile(r"^\s*#.*\b(?:type\s*[:=]\s*(?:file|dir|directory|user|symlink)|owner\s*[:=]\s*\w+\s*,)", re.M | re.I)),
    # контекст стенда строками-присваиваниями: «user= tester», «cwd=/tmp/x»
    ("fs_listing", re.compile(r"^\s*(?:user|cwd|uid|gid|home|shell)\s*=\s", re.M | re.I)),
    ("fs_listing", re.compile(r"^\s*cwd=\S+\s*$", re.M | re.I)),
    # «/path as root» — проза про предпосылку
    ("prose_line", re.compile(r"^\s*\S+ as (?:root|user|a user)\s*$", re.M | re.I)),
    ("model_reasoning", re.compile(r"^\s*#.*\bis available to user\b", re.M | re.I)),
    # пояснения модели о собственной команде: «# where $x is …», «# Note: the actual logic … here we …»
    ("model_reasoning", re.compile(r"^\s*#\s*where\s+\$\w+\s+is\b", re.M | re.I)),
    ("model_reasoning", re.compile(r"^\s*#\s*note:.*\b(?:actual|here we|we treat|simplified|representation)\b", re.M | re.I)),
]
# ≥2 подряд строк из одного пути без пробелов в начале команды — листинг файлов, не команды
LEADING_PATH_LIST_RE = re.compile(r"\A(?:\s*[\w.-]+(?:/[\w.-]+)+\s*\n){2,}")
# первая строка — проза (≥4 слов только из букв), а не команда
PROSE_FIRST_LINE_RE = re.compile(r"\A\s*[a-z]+(?: [a-z]+){3,}\s*$", re.M)


def contamination(cmd, util):
    reasons = sorted({name for name, rx in CONTAMINATION if rx.search(cmd)})
    first = cmd.strip().splitlines()[0] if cmd.strip() else ""
    if LEADING_PATH_LIST_RE.match(cmd):
        reasons.append("fs_listing")
    if PROSE_FIRST_LINE_RE.match(first) and first.split()[0] != util:
        reasons.append("prose_line")
    # «/some/dir gpg …»: первым токеном путь, а утилита идёт вторым словом
    toks = first.split()
    if len(toks) >= 2 and toks[0].startswith("/") and toks[1] == util and not toks[0].endswith("/" + util):
        reasons.append("prompt_prefix")
    return ["contamination:" + r for r in sorted(set(reasons))]


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
    if TRAILING_LIST_RE.search(c["command"]):
        reasons.append("trailing_list_artifact")
    if cfg["validate"].get("contamination_check", False):
        reasons.extend(contamination(c["command"], c["util"]))
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
    for c in read_jsonl(out / "neardeduped.jsonl"):
        reasons, warnings = check(c, cfg)
        if reasons:
            rejected.append({**c, "stage": "validate", "reason": ";".join(reasons)})
        else:
            kept.append({**c, "warnings": c.get("warnings", []) + warnings})
    # Пары risky/safe: опасный пример без контрпримера (или наоборот) не берём —
    # вторая сторона могла уйти на dedup или validate.
    sides = {}
    for c in kept:
        if c.get("pair_id"):
            sides.setdefault(c["pair_id"], set()).add(c["role"])
    broken = {p for p, s in sides.items() if s != {"risky", "safe"}}
    if broken:
        rejected += [{**c, "stage": "validate", "reason": "pair_partner_rejected"}
                     for c in kept if c.get("pair_id") in broken]
        kept = [c for c in kept if c.get("pair_id") not in broken]
    write_jsonl(out / "validated.jsonl", kept)
    write_jsonl(out / "rejected_validate.jsonl", rejected)
    review = [c for c in kept if any(w.startswith("label_conflict:") for w in c["warnings"])]
    write_jsonl(out / "review_queue.jsonl", review)
    # drop_review_queue: сомнительная метка без человека в датасет не идёт — пара уходит целиком
    if cfg["validate"].get("drop_review_queue", False) and review:
        held = {c["pair_id"] for c in review if c.get("pair_id")}
        held_ids = {id(c) for c in review}
        drop = [c for c in kept if id(c) in held_ids or (c.get("pair_id") and c["pair_id"] in held)]
        rejected += [{**c, "stage": "validate", "reason": "held_for_review"} for c in drop]
        drop_ids = {id(c) for c in drop}
        kept = [c for c in kept if id(c) not in drop_ids]
        write_jsonl(out / "validated.jsonl", kept)
        write_jsonl(out / "rejected_validate.jsonl", rejected)
    log(f"validate: прошло {len(kept)}, отброшено {len(rejected)}, на ревью (label_conflict) {len(review)}")
    return kept, rejected
