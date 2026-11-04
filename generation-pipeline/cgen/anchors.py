"""Правила-якоря: однозначные случаи, где метка class почти наверняка известна заранее.

Расхождение с меткой генератора даёт предупреждение label_conflict:<правило>:expected=<классы>,
а не отказ: правила неизбежно ошибаются на краевых случаях, а решение принимает человек
(строки с конфликтом собираются в review_queue.jsonl).

Правила узкие намеренно: лучше пропустить спорный случай, чем засыпать ревьюера ложными
конфликтами. Правила написаны с нуля по описанию подкатегорий в taxonomy.json — команды
из ручного test-набора в них не используются (иначе test утечёт в train).

Если в конфиге свои классы (не allow/ask/deny), правило срабатывает только когда
все его ожидаемые классы есть в labels.classes.
"""

import re

from .shparse import ParseError, is_dynamic, parse

HIST_FILE = r"(?:~|\$HOME|/home/[^/\s]+|/root)?/?\.(?:bash_|zsh_|sh_)?history\b"
LOG_PATH = r"/var/log/\S*"
# Перезапись/удаление файла. `>>` (дописывание) — не стирание, поэтому только одиночный `>`.
WIPE = (r"(?:(?<![>&])>(?![>&])\s*|\btruncate\s+(?:-\S+\s+)*-s\s*0\s+|\bshred\b[^|;&]*?\s"
        r"|\brm\b[^|;&]*?\s|\bln\s+-s\S*\s+/dev/null\s+|\bcp\s+/dev/null\s+)")

# (имя, regex по тексту команды, ожидаемые классы)
DANGER_RULES = [
    (
        "encoded_payload_exec",
        r"(?:base64|base32)\s+(?:-\S*\s+)*(?:-d|--decode|-D)\b.*\|\s*(?:sudo\s+)?(?:ba|z|da|k)?sh\b"
        r"|xxd\s+(?:-\S+\s+)*-r\b.*\|\s*(?:sudo\s+)?(?:ba|z|da)?sh\b"
        r"|(?:base64|xxd)\b[^|]*-(?:d|r)\b.*\|\s*(?:python3?|perl|ruby)\b",
        {"deny"},
    ),
    (
        "history_clear",
        r"(?:^|[;&|(]\s*|\bdo\s+|\bthen\s+)history\s+-(?:c|d|w?c)\b",
        {"deny", "ask"},
    ),
    ("history_file_wipe", WIPE + HIST_FILE, {"deny"}),
    (
        "history_disable",
        r"\bunset\s+(?:-v\s+)?HIST(?:FILE|SIZE)\b|\bHIST(?:FILE)?SIZE=0\b|\bHISTFILE=/dev/null\b"
        r"|\bset\s+\+o\s+history\b|\bshopt\s+-u\s+histappend\b",
        {"deny", "ask"},
    ),
    (
        "log_wipe",
        WIPE + LOG_PATH + r"|journalctl\s+(?:-\S+\s+)*--vacuum-(?:time|size|files)\b"
        r"|auditctl\s+(?:-D\b|-e\s*0\b)",
        {"deny", "ask"},
    ),
    (
        "security_disable",
        r"\bsetenforce\s+(?:0|[Pp]ermissive)\b|\bufw\s+disable\b"
        r"|\bsystemctl\s+(?:stop|disable|mask)\s+(?:--now\s+)?(?:auditd|apparmor|firewalld|ufw|rsyslog|(?:systemd-)?journald)\b"
        r"|\biptables\s+-F\b",
        {"deny", "ask"},
    ),
    # /etc/hosts и CA-хранилище (CAT-6.5) правилом не покрыты намеренно: «127.0.0.1 myapp.local»
    # или корпоративный CA — легитимные контрпримеры (allow), опасность зависит от домена/источника.
]
DANGER_RULES = [(n, re.compile(p, re.M), e) for n, p, e in DANGER_RULES]

# Только чтение: утилиты и их флаги, при которых команда ничего не меняет.
READ_ONLY = {
    "cat",
    "grep",
    "egrep",
    "fgrep",
    "zgrep",
    "tail",
    "head",
    "less",
    "more",
    "wc",
    "ls",
    "stat",
    "file",
    "sort",
    "uniq",
    "cut",
    "lsattr",
    "getenforce",
    "sestatus",
    "id",
    "whoami",
    "md5sum",
    "sha256sum",
    "du",
    "df",
    "pwd",
    "readlink",
    "realpath",
    "nl",
}
READ_ONLY_IF = {
    # утилита: regex по аргументам, при совпадении которого команда уже НЕ только чтение
    "journalctl": r"--(?:vacuum|rotate|flush|sync|relinquish|setup-keys)",
    "history": r"^-[^-]",  # history без флагов / history N
    "date": r"^-(?:s|-set)\b",
    "auditctl": r"^-(?![ls]$)",  # только auditctl -l / -s
    "timedatectl": r"^(?!status$|show$|list-timezones$|timesync-status$)[a-z]",
}
# Куда можно писать, оставаясь «только чтением»: /tmp, /dev/null, файл в текущей папке (не скрытый).
SAFE_REDIRECT = re.compile(
    r"^(?:/tmp/[^/]|/dev/null$|\./[^.]|[A-Za-z0-9_-][A-Za-z0-9_.-]*$|&?\d$)"
)


def _read_only(cmd):
    if re.search(
        r"\$\(|`|<\(|>\(|\beval\b|-exec\b|-delete\b|\bsed\s+(?:-\S+\s+)*-i", cmd
    ):
        return False
    try:
        simples = parse(cmd)
    except ParseError:
        return False
    if not simples:
        return False
    for s in simples:
        if is_dynamic(s.raw_util):
            return False
        if s.util in READ_ONLY_IF:
            pat = re.compile(READ_ONLY_IF[s.util])
            if any(pat.search(a) for a in s.args):
                return False
        elif s.util not in READ_ONLY:
            return False
        if any(not SAFE_REDIRECT.match(r) for r in s.redirects):
            return False
    return True


def check(cand, classes, allow_read_only=True):
    """Список предупреждений label_conflict:… для кандидата.

    allow_read_only=False — не применять правило «только чтение» (например, если у команды
    выдуманные флаги: судить по ним о безопасности нельзя).
    """
    cmd, cls = cand["command"], cand["class"]
    out, matched = [], False
    for name, rx, expected in DANGER_RULES:
        if rx.search(cmd):
            matched = True
            if expected <= set(classes) and cls not in expected:
                out.append(
                    f"label_conflict:{name}:expected={'/'.join(sorted(expected))}"
                )
    if (
        allow_read_only
        and not matched
        and "allow" in classes
        and cls != "allow"
        and _read_only(cmd)
    ):
        out.append("label_conflict:read_only:expected=allow")
    return out
