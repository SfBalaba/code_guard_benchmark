"""Сборка промпта из шаблона.

Шаблон — markdown-файл с двумя секциями, разделёнными строками-маркерами:
    <<<SYSTEM>>>
    ...
    <<<USER>>>
    ...
Подстановки вида {{name}}. Фигурные скобки и $ в bash-примерах шаблона не трогаются.
Доступные переменные: risk, risk_name, category, mechanism, seed_prompt,
classes, severities, n_candidates, split.
"""
import re
from pathlib import Path

VAR_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")


def load_template(path):
    text = Path(path).read_text(encoding="utf-8")
    m = re.search(r"^<<<SYSTEM>>>\s*$(.*?)^<<<USER>>>\s*$(.*)", text, re.S | re.M)
    if not m:
        raise ValueError(f"{path}: в шаблоне нужны маркеры <<<SYSTEM>>> и <<<USER>>>")
    return {"system": m.group(1).strip(), "user": m.group(2).strip(), "raw": text}


def render(text, values):
    def sub(m):
        key = m.group(1)
        if key not in values:
            raise KeyError(f"в шаблоне неизвестная переменная {{{{{key}}}}}")
        return str(values[key])
    return VAR_RE.sub(sub, text)


def build_messages(template, seed, cfg, taxonomy):
    risk = seed["risk"]
    cat = risk.split(".")[0]
    values = {
        "risk": risk,
        "risk_name": taxonomy.get(risk, risk),
        "category": taxonomy.get(cat, cat),
        "mechanism": seed.get("mechanism", ""),
        "seed_prompt": seed["prompt"],
        "classes": ", ".join(cfg["labels"]["classes"]),
        "severities": ", ".join(cfg["labels"]["severities"]),
        "n_candidates": cfg["prompt"]["candidates_per_call"],
        "split": cfg["split"],
    }
    return [
        {"role": "system", "content": render(template["system"], values)},
        {"role": "user", "content": render(template["user"], values)},
    ]
