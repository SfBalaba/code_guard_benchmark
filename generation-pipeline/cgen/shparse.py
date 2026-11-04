"""Лёгкий разбор bash-команды на простые команды: утилита + аргументы + перенаправления.

Это не полноценный парсер bash (без зависимостей не написать), а приближение, достаточное для
проверки флагов и правил-якорей. Принцип: если не уверены — не разбираем, а сообщаем,
что разбор не удался (вызывающий код ставит предупреждение, а не отказ).

Команда не исполняется: только shlex-токенизация текста.
"""

import os
import re
import shlex

SEPARATORS = {"|", "||", "&&", ";", "&", "(", ")", ";;", "|&", "\n"}
REDIRECTS = {">", ">>", "<", "<<", "<<<", ">&", "<&", "&>", "&>>", ">|", "<>"}
# Ключевые слова, после которых сразу идёт команда.
PREFIX_KEYWORDS = {
    "then",
    "do",
    "else",
    "elif",
    "if",
    "while",
    "until",
    "!",
    "{",
    "}",
    "time",
    "fi",
    "done",
    "esac",
}
# Конструкции, сегмент которых целиком не команда (for i in ...; case x in ...).
SKIP_KEYWORDS = {"for", "case", "select", "function", "in"}
ASSIGN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\[[^]]*\])?\+?=")
SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}

# Обёртки: снимаем и проверяем вложенную команду. Значение — флаги обёртки, принимающие аргумент.
WRAPPERS = {
    "sudo": set("ugCDhprtTU"),
    "doas": set("uC"),
    "env": set("uSC"),
    "nohup": set(),
    "nice": set("n"),
    "ionice": set("cnpPu"),
    "stdbuf": set("ioe"),
    "exec": set("a"),
    "command": set(),
    "builtin": set(),
    "xargs": set("IinLlPdaEs"),
    "watch": set("nd"),
    "timeout": set("sk"),
    "chroot": set(),
}


class ParseError(Exception):
    pass


class Simple:
    """Одна простая команда: util (basename), args, redirect-цели, сырой первый токен."""

    def __init__(self, util, args, redirects, raw_util):
        self.util, self.args, self.redirects, self.raw_util = (
            util,
            args,
            redirects,
            raw_util,
        )

    def __repr__(self):
        return f"Simple({self.util!r}, {self.args!r}, redirects={self.redirects!r})"


HEREDOC_RE = re.compile(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")


def _drop_heredoc_bodies(cmd):
    """Тело heredoc — данные, а не команды: вырезаем строки до разделителя."""
    out, delims = [], []
    for line in cmd.split("\n"):
        if delims:
            if line.strip() == delims[0]:
                delims.pop(0)
            continue
        out.append(line)
        delims.extend(m.group(2) for m in HEREDOC_RE.finditer(line))
    return "\n".join(out)


def _tokens(cmd):
    cmd = _drop_heredoc_bodies(cmd.replace("\\\n", " "))
    # перевод строки вне кавычек разделяет команды, как ";"
    lex = shlex.shlex(cmd, posix=True, punctuation_chars="();<>|&\n")
    lex.whitespace = " \t\r"
    lex.whitespace_split = True
    lex.commenters = ""
    try:
        return list(lex)
    except ValueError as exc:  # незакрытая кавычка и т.п.
        raise ParseError(str(exc)) from None


def _split(tokens):
    """Токены -> сегменты простых команд. `$( … )` и `<( … )` разбираются как отдельные
    команды, а внешняя команда после закрывающей скобки продолжается."""
    segs, cur, stack = (
        [],
        [],
        [],
    )  # stack: (сохранённый внешний сегмент, это подстановка?)
    for t in tokens:
        # "$(" токенизируется как "...$" + "(", а "<(" / ">(" — одним токеном
        cmd_subst = t == "(" and bool(cur) and cur[-1].endswith("$")
        proc_subst = t in ("<(", ">(")
        if cmd_subst or proc_subst:
            if cmd_subst:
                cur[-1] = cur[-1][:-1] + "$SUBST"  # значение подстановки неизвестно
            stack.append((cur, True))
            cur = []
            continue
        if t == "(":  # подоболочка ( … ) — обычная группа команд
            if cur:
                segs.append(cur)
            stack.append((None, False))
            cur = []
            continue
        if t == ")" and stack:
            outer, subst = stack.pop()
            if cur:
                segs.append(cur)
            cur = outer if subst else []
            continue
        if t in SEPARATORS or (t and set(t) <= set("|&;()") and t not in REDIRECTS):
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        segs.append(cur)
    return segs


def _strip_wrapper(name, words):
    """words — аргументы после обёртки; вернуть слова вложенной команды."""
    takes_arg = WRAPPERS[name]
    i = 0
    while i < len(words):
        w = words[i]
        if name == "env" and ASSIGN_RE.match(w):
            i += 1
            continue
        if w == "--":
            i += 1
            break
        if w.startswith("--"):
            i += 1
            continue
        if w.startswith("-") and len(w) > 1:
            if name in ("nice",) and w[1:].lstrip("-").isdigit():  # nice -10 cmd
                i += 1
                continue
            last = w[-1]
            i += 2 if (last in takes_arg and len(w) == 2) else 1
            continue
        break
    words = words[i:]
    if name == "timeout" and words:  # timeout [opts] DURATION cmd
        words = words[1:]
    return words


def _simple(seg):
    """Сегмент токенов -> Simple или None (не команда / не разобрать уверенно)."""
    words, redirects = [], []
    i = 0
    while i < len(seg):
        t = seg[i]
        if t in REDIRECTS or (t.endswith((">", "<")) and set(t) <= set("<>&")):
            if i + 1 < len(seg):
                redirects.append(seg[i + 1])
            i += 2
            continue
        # fd перед перенаправлением: "2" в "2>" после токенизации — отдельное слово
        if t.isdigit() and i + 1 < len(seg) and seg[i + 1] in REDIRECTS | {">&", "<&"}:
            i += 1
            continue
        words.append(t)
        i += 1
    while words and words[0] in PREFIX_KEYWORDS:
        words = words[1:]
    while words and ASSIGN_RE.match(words[0]):
        words = words[1:]
    if not words or words[0] in SKIP_KEYWORDS:
        return None
    for _ in range(4):  # sudo env nohup cmd
        name = os.path.basename(words[0])
        if name in WRAPPERS:
            words = _strip_wrapper(name, words[1:])
            while words and ASSIGN_RE.match(words[0]):
                words = words[1:]
            if not words:
                return None
        else:
            break
    raw = words[0]
    return Simple(os.path.basename(raw), words[1:], redirects, raw)


def parse(cmd, depth=0):
    """Список Simple. Рекурсивно заходит в `bash -c "..."`. Бросает ParseError."""
    out = []
    for seg in _split(_tokens(cmd)):
        s = _simple(seg)
        if s is None:
            continue
        out.append(s)
        if s.util in SHELLS and depth < 3:
            for j, a in enumerate(s.args):
                if (
                    a.startswith("-")
                    and not a.startswith("--")
                    and "c" in a[1:]
                    and j + 1 < len(s.args)
                ):
                    out.extend(parse(s.args[j + 1], depth + 1))
                    break
    return out


def is_dynamic(word):
    """Имя команды вычисляется в рантайме: $a, ${x}, $(…), `…`, eval-обфускация."""
    return "$" in word or "`" in word or word == ""
