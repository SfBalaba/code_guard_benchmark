"""Собирает словарь флагов утилит: flags/<util>.json.

Источник — исходники man-страниц Debian (manpages.debian.org, релиз RELEASE), то есть
флаги GNU/Linux-версий утилит, а не BSD/macOS. Linux-машина для сборки не нужна.
Встроенные команды bash (history, set, ...) у man-страниц нет — они заданы вручную в BUILTINS
по документации bash.

Запуск (из папки generation-pipeline):
    python3 tools/build_flags.py            # все утилиты из UTILS
    python3 tools/build_flags.py tail grep  # только указанные

Формат flags/<util>.json:
    {"util", "source", "short": {"n": "required"|"optional"|"none"},
     "long": {"lines": "required"|...}, "arg_patterns": {"-d": "regex"}}
Неполный разбор ведёт к лишним отказам, поэтому парсер собирает флаги щедро:
любое упоминание \\-x / \\-\\-xx в тексте страницы считается существующим флагом.
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

RELEASE = "bookworm"
OUT = Path(__file__).resolve().parents[1] / "flags"

# util -> (пакет Debian, секция man). Список — утилиты подкатегорий CAT-6 и частые соседи.
UTILS = {
    # coreutils
    **{
        u: ("coreutils", 1)
        for u in [
            "base64",
            "base32",
            "cat",
            "cp",
            "mv",
            "rm",
            "ln",
            "ls",
            "mkdir",
            "rmdir",
            "touch",
            "chmod",
            "chown",
            "date",
            "head",
            "tail",
            "wc",
            "shred",
            "truncate",
            "tee",
            "sort",
            "uniq",
            "cut",
            "stat",
            "basename",
            "dirname",
            "readlink",
            "realpath",
            "md5sum",
            "sha256sum",
            "du",
            "df",
            "id",
            "whoami",
            "sleep",
            "tr",
            "od",
            "install",
            "mktemp",
            "nl",
            "split",
        ]
    },
    "grep": ("grep", 1),
    "sed": ("sed", 1),
    "gzip": ("gzip", 1),
    "less": ("less", 1),
    "journalctl": ("systemd", 1),
    "systemctl": ("systemd", 1),
    "timedatectl": ("systemd", 1),
    "logrotate": ("logrotate", 8),
    "auditctl": ("auditd", 8),
    "ausearch": ("auditd", 8),
    "chattr": ("e2fsprogs", 1),
    "lsattr": ("e2fsprogs", 1),
    "xxd": ("xxd", 1),
    "curl": ("curl", 1),
    "wget": ("wget", 1),
    "hwclock": ("util-linux-extra", 8),
    "logger": ("bsdutils", 1),
    "file": ("file", 1),
    "setenforce": ("selinux-utils", 8),
    "getenforce": ("selinux-utils", 8),
    "sestatus": ("policycoreutils", 8),
    "update-ca-certificates": ("ca-certificates", 8),
    "ntpdate": ("ntpsec-ntpdate", 8),
    "crontab": ("cron", 1),
    "useradd": ("passwd", 8),
    "usermod": ("passwd", 8),
    "passwd": ("passwd", 1),
    "ssh-keygen": ("openssh-client", 1),
    "scp": ("openssh-client", 1),
    "rsync": ("rsync", 1),
    "nc": ("netcat-openbsd", 1),
}

# Ручные поправки к разобранному.
OVERRIDES = {
    # у chattr "-i" — снятие атрибута i, а не флаг: буквы атрибутов допустимы после - и +
    "chattr": {"short_extra": "aAcCdDeFijmPsStTux"},
    # chmod -x / -w / -rwx — символьный режим (снять права), а не флаги
    "chmod": {"short_extra": "rwxXstugoa"},
    # словарь из netcat-openbsd, но в датасетах nc -e/-c (netcat-traditional, reverse shell) встречается
    # постоянно — это настоящий флаг другой реализации, а не выдумка модели
    "nc": {"short_extra": "ec"},
    # wget -nv/-np/-nc и в склейке: -mnp = -m -np
    "wget": {"short_kind": {"n": "optional"}},
}

BASH_DOC = "https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html"
BUILTINS = {
    # history -d принимает номер записи (или диапазон start-end), но не дату/путь
    "history": {
        "short": {
            "c": "none",
            "d": "required",
            "a": "none",
            "n": "none",
            "r": "none",
            "w": "none",
            "p": "none",
            "s": "none",
        },
        "arg_patterns": {"-d": r"^-?\d+(?:--?\d+)?$"},
    },
    "unset": {"short": {"f": "none", "v": "none", "n": "none"}},
    "export": {"short": {"f": "none", "n": "none", "p": "none"}},
    "set": {
        "short": {c: "none" for c in "abefhkmnptuvxBCEHPT"} | {"o": "optional"},
        "plus_flags": True,
    },
    "shopt": {"short": {c: "none" for c in "opqsu"}},
    "unalias": {"short": {"a": "none"}},
    "alias": {"short": {"p": "none"}},
    "type": {"short": {c: "none" for c in "afptP"}},
    "read": {
        "short": {
            "a": "required",
            "d": "required",
            "e": "none",
            "i": "required",
            "n": "required",
            "N": "required",
            "p": "required",
            "r": "none",
            "s": "none",
            "t": "required",
            "u": "required",
        }
    },
    # kill -HUP / -SIGTERM / -9 — сигнал вместо флага
    "kill": {"short": {"s": "required", "n": "required", "l": "none", "L": "none"}, "signal_flags": True},
    "ulimit": {"short": {c: "none" for c in "SHabcdefiklmnpqrstuvxPRT"}},
}

ROFF_ESC = [
    (r"\\f\[[A-Z]*\]", ""),
    (r"\\f[BIRPC]", ""),
    (r"\\[,/&^|]", ""),  # \^ \| — узкие пробелы: "\-\^\-ignore" у grep
    (r"\\\(.{2}", ""),
    (r"\\-", "-"),
    (r"\\e", "\\"),
]
SHORT_RE = re.compile(
    r"(?<![\w-])-([A-Za-z0-9?@])(?![\w-])(\[|=|\s+(?:<|\[?[A-Z][A-Za-z_]*\b|[a-z]+\b(?=\s*$)))?"
)
# двух-четырёхбуквенные опции с одним дефисом: wget -nv/-np, ausearch -ui/-ts
WORD_RE = re.compile(r"(?<![\w-])-([A-Za-z][A-Za-z0-9]{1,3})(?![\w-])")
LONG_RE = re.compile(r"(?<![\w-])--([A-Za-z0-9][\w-]*)(\[=|=|\s+[A-Z<][\w>]*)?")


def _plain(line):
    for pat, rep in ROFF_ESC:
        line = re.sub(pat, lambda _m, r=rep: r, line)
    return line


def parse_man(text):
    short, long, words = {}, {}, set()
    lines = text.splitlines()
    for n, raw in enumerate(lines):
        if raw.startswith('.\\"'):
            continue
        line = _plain(raw)
        prev = lines[n - 1].strip() if n else ""
        # заголовок опции: строка после .TP/.PP/.IP или начинающаяся с флага
        header = (
            prev in (".TP", ".PP", ".IP", ".sp")
            or prev.startswith((".TP", ".IP"))
            or line.lstrip(". B").startswith("-")
            or raw.startswith((".B ", ".BR ", ".BI ", ".IP"))
        )
        if header:
            words.update(m.group(1) for m in WORD_RE.finditer(line))
        longs_here = []
        for m in LONG_RE.finditer(line):
            arg = "none"
            if header and m.group(2):
                arg = "optional" if m.group(2).startswith("[") else "required"
            longs_here.append(arg)
            if long.get(m.group(1), "none") == "none":
                long[m.group(1)] = arg
        for m in SHORT_RE.finditer(line):
            ch = m.group(1)
            arg = "none"
            if header:
                g = m.group(2)
                if g:
                    arg = "optional" if g == "[" else "required"
                elif (
                    longs_here
                    and "-" + ch + "," in line.replace(" ", "")
                    and longs_here[0] != "none"
                ):
                    # "-n, --lines=NUM": значение короткого флага описано у длинного
                    arg = longs_here[0]
            if short.get(ch, "none") == "none":
                short[ch] = arg
    return short, long, words


def parse_mdoc(text):
    """BSD-разметка mdoc: `.It Fl c Ar cipher`, `.Op Fl 346ABC`, `.It Fl Fl brief`."""
    short, long = {}, {}
    for raw in text.splitlines():
        if not raw.startswith(".") or " Fl" not in raw:
            continue
        toks = raw.replace(",", " ").split()
        for i, t in enumerate(toks):
            if t != "Fl" or i + 1 >= len(toks) or (i and toks[i - 1] == "Fl"):
                continue
            if toks[i + 1] == "Fl":  # Fl Fl name -> --name
                if i + 2 < len(toks):
                    has_arg = i + 3 < len(toks) and toks[i + 3] == "Ar"
                    name = toks[i + 2]
                    if long.get(name, "none") == "none":
                        long[name] = "required" if has_arg else "none"
                continue
            name = toks[i + 1]
            if not re.fullmatch(r"[A-Za-z0-9?@]+", name):
                continue
            has_arg = i + 2 < len(toks) and toks[i + 2] == "Ar"
            if len(name) == 1:
                if short.get(name, "none") == "none":
                    short[name] = "required" if has_arg else "none"
            else:  # "Fl 346ABCpq" в синопсисе — набор однобуквенных флагов
                for ch in name:
                    short.setdefault(ch, "none")
    return short, long


def parse_any(text):
    short, long, words = parse_man(text)
    if re.search(r"^\.(Dd|Sh|It)\b", text, re.M):
        s2, l2 = parse_mdoc(text)
        for d, extra in ((short, s2), (long, l2)):
            for k, v in extra.items():
                if d.get(k, "none") == "none":
                    d[k] = v
    return short, long, words


def fetch(pkg, util, sec):
    url = f"https://manpages.debian.org/{RELEASE}/{pkg}/{util}.{sec}.en.gz"
    req = urllib.request.Request(url, headers={"User-Agent": "cgen-build-flags"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    if data[:2] == b"\x1f\x8b":
        import gzip

        data = gzip.decompress(data)
    return url, data.decode("utf-8", "replace")


def build(util):
    if util in BUILTINS:
        entry = {"util": util, "source": BASH_DOC, "long": {}, **BUILTINS[util]}
    else:
        pkg, sec = UTILS[util]
        url, text = fetch(pkg, util, sec)
        short, long, words = parse_any(text)
        for ch in OVERRIDES.get(util, {}).get("short_extra", ""):
            short.setdefault(ch, "none")
        short.update(OVERRIDES.get(util, {}).get("short_kind", {}))
        entry = {
            "util": util,
            "source": url,
            "short": dict(sorted(short.items())),
            "long": dict(sorted(long.items())),
            "words": sorted(words),
        }
        if util == "chattr":  # chattr +i — добавление атрибута
            entry["plus_flags"] = True
    OUT.mkdir(exist_ok=True)
    (OUT / f"{util}.json").write_text(
        json.dumps(entry, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    return entry


def main(argv):
    names = argv or sorted(set(UTILS) | set(BUILTINS))
    failed = []
    for u in names:
        try:
            e = build(u)
            print(f"{u}: short={len(e['short'])} long={len(e['long'])}")
        except Exception as exc:  # noqa: BLE001 — сеть/404: сообщаем и идём дальше
            failed.append(u)
            print(f"{u}: ОШИБКА {exc}", file=sys.stderr)
    if failed:
        print(f"не собраны: {', '.join(failed)}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
