"""Загрузка конфига запуска. Пути в конфиге считаются от папки, где лежит сам конфиг."""
import json
from copy import deepcopy
from pathlib import Path

DEFAULTS = {
    "run_name": "run",
    "split": None,                     # "test" | "train" — обязателен
    "seeds_path": None,                # JSONL в формате d3-judge-pipeline
    "output_dir": "runs",              # итог: <output_dir>/<run_name>/
    "taxonomy_path": None,             # JSON: {"CAT-6": "...", "CAT-6.1": "..."}
    "prompt": {"template": None, "version": "v1", "candidates_per_call": 4},
    "backend": {"provider": "mock"},
    "sampling": {
        "temperature": 0.8,
        "top_p": 0.95,
        "max_tokens": 1024,
        "seed": 20261103,              # числовой random seed модели (не путать с seed-промптом)
        "samples_per_seed": 1,         # сколько вызовов модели на один seed
        "samples_per_seed_by_risk": {},  # переопределение числа семплов по risk (двухуровневый сэмплинг)
    },
    "seeds": {"allowed_statuses": ["approved_for_generation"]},
    "labels": {
        "classes": ["allow", "ask", "deny"],
        "severities": ["low", "medium", "high", "critical"],
    },
    "clean": {
        "max_command_chars": 2000,
        "allow_non_ascii_command": False,
        "strip_cyrillic_comment_lines": False,  # вырезать строки-комментарии с кириллицей (# TASK/# FS из сидов)
    },
    "dedup": {"against": []},          # пути к CSV/JSONL, команды из которых нельзя повторять (например, test)
    "neardup": {                       # лексический near-dup (шаг 4b); эмбеддинги можно добавить позже
        "enabled": False,
        "threshold": 0.5,              # Jaccard по символьным k-граммам; >= порога -> near-dup (0.5 разделяет близнецов и разные рецепты)
        "shingle_k": 4,
        "family_cap": None,            # максимум оставленных пар с одним family_id (None — без лимита)
        "family_cap_by_risk": {},      # переопределение cap по risk, напр. {"CAT-5.1": 3}
        "against_test": False,         # near-dup ПРОТИВ команд из dedup.against (не только точные совпадения)
        "test_threshold": 0.5,         # порог Jaccard для near-leak train↔test
    },
    "validate": {
        "bash_syntax_check": True,
        "flag_check": "reject",        # "off" | "warn" | "reject": выдуманные флаги по словарю flags/
        "flags_dir": None,             # своя папка словарей; null — flags/ рядом с пакетом
        "label_anchors": True,         # правила-якоря: label_conflict -> review_queue.jsonl
    },
    "export": {"seed_column": "prompt"},  # "prompt" — текст seed в колонке seed, "seed_id" — только id
}

PROVIDERS = {"mock", "openai_compatible"}


def _merge(base, over):
    out = deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path):
    path = Path(path).resolve()
    cfg = _merge(DEFAULTS, json.loads(path.read_text(encoding="utf-8")))
    base = path.parent

    def resolve(p):
        return str((base / p).resolve()) if p else p

    cfg["seeds_path"] = resolve(cfg["seeds_path"])
    cfg["output_dir"] = resolve(cfg["output_dir"])
    cfg["taxonomy_path"] = resolve(cfg["taxonomy_path"])
    cfg["prompt"]["template"] = resolve(cfg["prompt"]["template"])
    cfg["dedup"]["against"] = [resolve(p) for p in cfg["dedup"]["against"]]
    cfg["validate"]["flags_dir"] = resolve(cfg["validate"]["flags_dir"])
    cfg["_config_path"] = str(path)
    check_config(cfg)
    return cfg


def check_config(cfg):
    errors = []
    if cfg["split"] not in ("test", "train"):
        errors.append("split должен быть 'test' или 'train'")
    if not cfg["seeds_path"]:
        errors.append("не задан seeds_path")
    if not cfg["prompt"]["template"]:
        errors.append("не задан prompt.template")
    if cfg["backend"].get("provider") not in PROVIDERS:
        errors.append(f"backend.provider должен быть одним из {sorted(PROVIDERS)}")
    if not cfg["labels"]["classes"]:
        errors.append("labels.classes пуст")
    if cfg["validate"]["flag_check"] not in ("off", "warn", "reject"):
        errors.append("validate.flag_check: 'off', 'warn' или 'reject'")
    if cfg["export"]["seed_column"] not in ("prompt", "seed_id", "full_request"):
        errors.append("export.seed_column: 'prompt', 'seed_id' или 'full_request'")
    for risk, sides in cfg["labels"].get("pair_contract", {}).items():
        for role in ("risky", "safe"):
            pairs = sides.get(role) or []
            if not pairs:
                errors.append(f"labels.pair_contract.{risk}.{role}: пусто")
            for cls, sev in pairs:
                if cls not in cfg["labels"]["classes"] or sev not in cfg["labels"]["severities"]:
                    errors.append(f"labels.pair_contract.{risk}.{role}: {cls}/{sev} вне labels.classes/severities")
    if cfg["split"] == "train" and cfg["backend"].get("provider") != "mock" and not cfg["dedup"]["against"]:
        errors.append("split=train с настоящей моделью: dedup.against пуст — укажи все test-CSV (антиутечка)")
    missing = [p for p in cfg["dedup"]["against"] if not Path(p).exists()]
    if missing:
        errors.append(f"dedup.against: нет файлов/папок {missing} (выгрузи test: tools/pull_test_data.py)")
    if errors:
        raise ValueError("Ошибки конфига:\n  - " + "\n  - ".join(errors))


def run_dir(cfg) -> Path:
    return Path(cfg["output_dir"]) / cfg["run_name"]
