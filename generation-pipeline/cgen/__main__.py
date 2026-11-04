"""CLI: python -m cgen <команда> --config path/to/config.json

  run        весь конвейер: generate -> clean -> dedup -> validate -> export -> report
  check      только проверить конфиг и seed (без вызовов модели)
  generate   только генерация (поддерживает --resume, --limit, --dry-run)
  clean | dedup | validate | export | report   отдельные шаги по уже готовым файлам
"""
import argparse
import sys

from . import clean, dedup, export, generate, report, validate
from .config import load_config
from .seeds import load_seeds

POST = [("clean", clean.run), ("dedup", dedup.run), ("validate", validate.run),
        ("export", export.run), ("report", report.run)]


def main(argv=None):
    p = argparse.ArgumentParser(prog="cgen", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", choices=["run", "check", "generate"] + [n for n, _ in POST])
    p.add_argument("--config", required=True)
    p.add_argument("--resume", action="store_true", help="продолжить прерванную генерацию")
    p.add_argument("--limit", type=int, help="не больше N вызовов модели за запуск")
    p.add_argument("--dry-run", action="store_true", help="собрать промпты без вызова модели")
    a = p.parse_args(argv)
    try:
        cfg = load_config(a.config)
        if a.command == "check":
            seeds = load_seeds(cfg)
            print(f"ok: {len(seeds)} seed, split={cfg['split']}")
            return 0
        if a.command in ("run", "generate"):
            generate.run(cfg, resume=a.resume, limit=a.limit, dry_run=a.dry_run)
            if a.command == "generate" or a.dry_run:
                return 0
            for _, step in POST:
                step(cfg)
            return 0
        dict(POST)[a.command](cfg)
        return 0
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f"ошибка: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
