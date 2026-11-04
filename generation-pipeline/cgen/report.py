"""Отчёт по запуску: report.json + report.md.

Что показывает: сколько отсеялось на каждом шаге и почему, баланс классов и severity,
разнообразие утилит, выход по каждому seed и покрытие синтаксических конструкций
(вложенные вызовы, bash -c, пайпы и т.д. — то, что требовали на синке 29.10).
"""
import re
from collections import Counter

from .config import run_dir
from .io import read_jsonl, read_jsonl_tolerant, write_json

# Структурные признаки для стратификации и контроля покрытия — не метки опасности.
CONSTRUCTS = {
    "pipeline": r"(?<!\|)\|(?!\|)",
    "chain": r"&&|\|\||;",
    "nested_shell_c": r"\b(?:bash|sh|zsh|dash)\s+-[a-zA-Z]*c\b",
    "command_substitution": r"\$\(|`",
    "variable_expansion": r"\$\{?[A-Za-z_]",
    "heredoc": r"<<-?\s*['\"]?\w+",
    "process_substitution": r"[<>]\(",
    "loop": r"\b(?:for|while|until)\b.*\bdo\b",
    "function_def": r"\w+\s*\(\)\s*\{",
    "xargs_or_exec": r"\bxargs\b|-exec\b",
    "eval": r"\beval\b",
}


def constructs(cmd):
    return [name for name, pat in CONSTRUCTS.items() if re.search(pat, cmd, re.S)]


def run(cfg, log=print):
    out = run_dir(cfg)
    raw = read_jsonl_tolerant(out / "raw.jsonl")
    stages = {s: read_jsonl(out / f"rejected_{s}.jsonl") for s in ("clean", "dedup", "validate")}
    final = read_jsonl(out / "validated.jsonl")
    seeds = read_jsonl(cfg["seeds_path"])

    reasons = {s: dict(Counter(r["reason"] for r in rows).most_common()) for s, rows in stages.items()}
    per_seed = Counter(c["seed_id"] for c in final)
    utils = Counter(c["util"] for c in final)
    cov = Counter(x for c in final for x in constructs(c["command"]))
    rep = {
        "run_name": cfg["run_name"],
        "calls": dict(Counter(r["status"] for r in raw)),
        "rejected": {s: len(v) for s, v in stages.items()},
        "rejected_reasons": reasons,
        "final_rows": len(final),
        "class": dict(Counter(c["class"] for c in final).most_common()),
        "severity": dict(Counter(c["severity"] for c in final).most_common()),
        "risk": dict(Counter(c["risk"] for c in final).most_common()),
        "unique_utils": len(utils),
        "top_utils": dict(utils.most_common(15)),
        "constructs": {k: cov.get(k, 0) for k in CONSTRUCTS},
        "per_seed_yield": {s["seed_id"]: per_seed.get(s["seed_id"], 0) for s in seeds},
        "seeds_with_zero_yield": [s["seed_id"] for s in seeds if per_seed.get(s["seed_id"], 0) == 0],
        "fixes_applied": dict(Counter(f for c in final for f in c.get("fixes", []))),
        "warnings": dict(Counter(w for c in final for w in c.get("warnings", []))),
        # причины склеены через ";" — для флагов считаем каждую отдельно
        "flag_problems": dict(Counter(
            x for r in stages["validate"] for x in r["reason"].split(";")
            if x.startswith(("unknown_flag:", "bad_flag_value:"))).most_common())
        | dict(Counter(w for c in final for w in c.get("warnings", [])
                       if w.startswith(("unknown_flag:", "bad_flag_value:"))).most_common()),
        "label_conflicts": dict(Counter(
            w for c in final for w in c.get("warnings", []) if w.startswith("label_conflict:")).most_common()),
        "review_queue": len(read_jsonl(out / "review_queue.jsonl")),
        "flags_unchecked_utils": dict(Counter(
            w.split(":", 1)[1] for c in final for w in c.get("warnings", [])
            if w.startswith("flags_unchecked:")).most_common()),
    }
    write_json(out / "report.json", rep)
    (out / "report.md").write_text(_markdown(rep), encoding="utf-8")
    log(f"report: {out / 'report.md'}")
    return rep


def _table(d, head=("значение", "кол-во")):
    if not d:
        return "_нет_\n"
    lines = [f"| {head[0]} | {head[1]} |", "|---|---|"] + [f"| `{k}` | {v} |" for k, v in d.items()]
    return "\n".join(lines) + "\n"


def _markdown(r):
    total_calls = sum(r["calls"].values())
    parts = [
        f"# Отчёт: {r['run_name']}\n",
        f"Вызовов модели: {total_calls} ({', '.join(f'{k}: {v}' for k, v in r['calls'].items())}). "
        f"Итоговых строк: **{r['final_rows']}**.\n",
        "## Отсев по шагам\n",
        _table(r["rejected"], ("шаг", "отброшено")),
    ]
    for stage, rs in r["rejected_reasons"].items():
        if rs:
            parts += [f"\n**Причины, {stage}:**\n\n", _table(rs, ("причина", "кол-во"))]
    parts += [
        "\n## Баланс\n", "\n**class**\n\n", _table(r["class"]), "\n**severity**\n\n", _table(r["severity"]),
        "\n**risk**\n\n", _table(r["risk"]),
        f"\n## Разнообразие утилит\n\nУникальных утилит: {r['unique_utils']}.\n\n", _table(r["top_utils"], ("util", "кол-во")),
        "\n## Покрытие конструкций\n\nСколько итоговых команд содержит конструкцию.\n\n", _table(r["constructs"], ("конструкция", "команд")),
        "\n## Выход по seed\n\n", _table(r["per_seed_yield"], ("seed_id", "строк")),
    ]
    if r["seeds_with_zero_yield"]:
        parts.append(f"\nSeed без единой строки: {', '.join(r['seeds_with_zero_yield'])}\n")
    parts += [
        "\n## Флаги и метки\n\n",
        "Выдуманные флаги и неверные значения флагов (по словарю `flags/`):\n\n",
        _table(r["flag_problems"], ("проблема", "кол-во")),
        f"\nКонфликты меток с правилами-якорями — строк на ревью: **{r['review_queue']}** "
        "(`review_queue.jsonl`).\n\n",
        _table(r["label_conflicts"], ("конфликт", "кол-во")),
        "\nУтилиты без словаря флагов (флаги не проверены):\n\n",
        _table(r["flags_unchecked_utils"], ("util", "команд")),
    ]
    if r["fixes_applied"]:
        parts += ["\n## Исправления при очистке\n\n", _table(r["fixes_applied"], ("исправление", "кол-во"))]
    other = {k: v for k, v in r["warnings"].items()
             if not k.startswith(("label_conflict:", "flags_unchecked:", "unknown_flag:", "bad_flag_value:"))}
    if other:
        parts += ["\n## Прочие предупреждения\n\n", _table(other, ("предупреждение", "кол-во"))]
    return "".join(parts)
