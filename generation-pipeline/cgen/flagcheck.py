"""Проверка флагов утилит по словарю flags/<util>.json (см. tools/build_flags.py).

Ловит выдуманные моделью флаги (`journalctl --zero-logs`, `logrotate --delay`) и неверные
значения флагов, для которых задан шаблон (`history -d 2023/12/12`).

Принцип — не отказывать, если не уверены:
- утилиты нет в словаре — флаги не проверяются (предупреждение flags_unchecked:<util>);
- имя команды вычисляется в рантайме ($a, ${r}${m}) — это приём обфускации (CAT-6.2), не ошибка;
- утилиты со своим синтаксисом аргументов (find, dd, tar, …) пропускаются;
- команду не удалось разобрать — предупреждение flags_parse_failed.
"""

import json
import re
from functools import lru_cache
from pathlib import Path

from .shparse import SHELLS, ParseError, is_dynamic, parse

DEFAULT_DIR = Path(__file__).resolve().parents[1] / "flags"

# Свой синтаксис аргументов или флаги зависят от подкоманды — словарь из man не подходит.
SKIP_UTILS = {
    "find",
    "dd",
    "tar",
    "ps",
    "git",
    "openssl",
    "iptables",
    "ip6tables",
    "ufw",
    "trust",
    "docker",
    "kubectl",
    "python",
    "python3",
    "perl",
    "ruby",
    "node",
    "awk",
    "gawk",
    "java",
    "echo",
    "printf",
    "test",
    "[",
    "[[",
    "eval",
    "source",
    ".",
    "true",
    "false",
    ":",
    "cd",
    "pushd",
    "popd",
    "exit",
    "return",
    "trap",
    "wait",
    "jobs",
    "fg",
    "bg",
    "local",
    "declare",
    "typeset",
    "let",
    "pip",
    "npm",
    "apt",
    "apt-get",
    "yum",
    "dnf",
    "brew",
    "make",
    "security",
} | SHELLS


@lru_cache(maxsize=None)
def _load(flags_dir, util):
    p = Path(flags_dir) / f"{util}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _check_args(util, args, d):
    """Список проблем для одной простой команды по словарю d."""
    problems = []
    short, long_, patterns = (
        d.get("short", {}),
        d.get("long", {}),
        d.get("arg_patterns", {}),
    )
    i = 0
    while i < len(args):
        a = args[i]
        i += 1
        if a == "--":
            break
        if a.startswith("--") and len(a) > 2:
            name, eq, _ = a[2:].partition("=")
            kind = long_.get(name)
            if kind is None:
                # GNU getopt принимает однозначные сокращения: --verb для --verbose
                if not [k for k in long_ if k.startswith(name)]:
                    problems.append(f"unknown_flag:{util}:--{name}")
            elif kind == "required" and not eq:
                i += 1
            continue
        if (
            a.startswith("+") and d.get("plus_flags") and len(a) > 1
        ):  # set +o, chattr +i
            for ch in a[1:]:
                if ch not in short:
                    problems.append(f"unknown_flag:{util}:+{ch}")
                    break
            continue
        if not a.startswith("-") or a == "-" or is_dynamic(a):
            continue
        body = a[1:]
        if body in d.get("words", ()):  # wget -nv, ausearch -ui
            continue
        if d.get("signal_flags") and re.fullmatch(r"(?:SIG)?[A-Z][A-Z0-9+-]*|RTMIN.*|RTMAX.*", body):
            continue
        if re.fullmatch(r"\d+", body):  # head -5, kill -9, nice -10
            continue
        for j, ch in enumerate(body):
            kind = short.get(ch)
            if kind is None:
                problems.append(f"unknown_flag:{util}:-{ch}")
                break
            if kind in ("required", "optional"):
                value = body[j + 1 :]
                if not value and kind == "required" and i < len(args):
                    value = args[i]
                    i += 1
                pat = patterns.get("-" + ch)
                if (
                    pat
                    and value
                    and not is_dynamic(value)
                    and not re.fullmatch(pat, value)
                ):
                    problems.append(f"bad_flag_value:{util}:-{ch}")
                break
    return problems


def check(cmd, flags_dir=DEFAULT_DIR):
    """(problems, warnings). problems — найденные выдуманные флаги / неверные значения."""
    try:
        simples = parse(cmd)
    except ParseError:
        return [], ["flags_parse_failed"]
    problems, warnings = [], []
    for s in simples:
        if is_dynamic(s.raw_util) or s.util in SKIP_UTILS:
            continue
        d = _load(str(flags_dir), s.util)
        if d is None:
            warnings.append(f"flags_unchecked:{s.util}")
            continue
        problems += _check_args(s.util, s.args, d)
    return list(dict.fromkeys(problems)), list(dict.fromkeys(warnings))
