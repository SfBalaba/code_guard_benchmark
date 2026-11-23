# CAT-4 train (синтетика, НЕ gold)

`dataset.csv` — 1 072 строки синтетического **train** для CAT-4 (Privilege Escalation & Permission Abuse / Secret Reading).
Статус: `human_reviewed=false`, не gold. Дальше — judge Дарины + ручное ревью.

| | |
|---|---|
| Классы | allow 536 / deny 513 / ask 23 |
| Подкатегории | CAT-4.1 178 · 4.2 252 · 4.3 254 · 4.4 174 · 4.5 214 |
| Пары | 536 пар risky/safe, у каждой опасной строки есть безопасный контрпример с той же утилитой |
| Формат | 9 колонок `command, description, util, severity, category, risk, source, seed, class`; `source=synthetic`, в `seed` — полный промпт |

## Происхождение

- **Сиды:** 100 TRAIN-сидов a.kirillov, ветка `feat/data_CAT-4`, коммит `2efa9ea`, `CAT-4/seeds/*.md` (по 20 на подкатегорию). Сконвертированы `tools/convert_txt_seeds.py` с провенансом (путь, sha256), переведены на английский (`seeds/en/CAT-4.jsonl`, changelog — `seeds/en/parts/CAT-4.json` → `_meta`). В генерации 99: `CAT-4.4-TRAIN-S19` (pwck) исключён — давал near-dup с test у всех моделей.
- **Модели** (abliterated, llama.cpp, локально; набор согласован командой 22.11), thinking выключен:
  - Qwen3.8-27B — `huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF`, UD-IQ4_XS @ `c4b9022`
  - gemma-4-26B-A4B — `groxaxo/Huihui-gemma-4-26B-A4B-it-abliterated-GGUF`, UD-IQ4_XS @ `5d4351c`
  - Devstral-Small-2-24B — `mradermacher/Huihui-Devstral-Small-2-24B-Instruct-2512-abliterated-GGUF`, IQ4_XS @ `1e85953`
- **Семплирование:** temperature 0.8, top_p 0.95, max_tokens 3000, 3 сэмпла на сид на модель, seed 20261141 / 20261142 / 20261143. Сырые ответы, `prompt_sha` и `call_seed` — в `raw.jsonl`/`provenance.jsonl`.
- **Прогон:** `tools/run_v0.py --prefix train_cat4`, 23.11.2026 01:58–08:26, 891 вызов, 0 ошибок. Пересборка после чистки: `--skip-generate`.

## Метки

Модель метку не ставит — метки из контракта сида (`labels.pair_contract`, per-seed записи важнее подкатегории):
- risky сида S19 каждой подкатегории → `ask/medium` (сид явно задаёт эталон ask);
- остальные risky → `deny/critical`;
- safe → `allow/low`.

## Конвейер и отсев

clean → exact-dedup против всех test-CSV → near-dup (char-4-gram Jaccard 0.5; внутри прогона и против 11 811 test-команд, по обеим сторонам пары) → validate (`bash -n`, словари флагов, `contamination`, пары целиком) → export.
Отсев: near-dup 340 (из них против test 80), validate 212 (синтаксис, мусор-обвязка 30 пар, 13 пар с сомнительной меткой отложены на ревью — `rejected_validate.jsonl`, `held_for_review`), dedup 94, clean 32. Подробно — `report.md`.

Независимый валидатор (23.11): GO на передачу. Утечки нет (max Jaccard против test 0.49), формат/пары/метки чистые.

## Известные ограничения

1. **Смысловая годность ~65–70%** (выборка 42 пары, один ревьюер, ±15 п.п.): встречаются «опасные» команды без реального повышения привилегий, dry-run/проверки с меткой critical, почти одинаковые стороны.
2. **B1 — возможная близость к test (правило 2).** Семейства сидов S19 (ask) и `CAT-4.5-TRAIN-S20` по форме похожи на отдельные test-строки того же автора (та же утилита и класс). Это подозрение, не доказательство; решение Влада — оставить. Затронуто 52 строки (S19: 23 ask + 23 allow; 4.5-S20: 6). Убрать: фильтр по `seed_id` в `provenance.jsonl`.
3. **ask только 2%** (в test CAT-4 — 8%); severity у risky всегда critical (в test есть deny/high).
4. **Объём ниже 250** в 4.1, 4.4, 4.5. 13 пар `held_for_review` в основном корректны (ложный якорь read_only) — ручное ревью может вернуть ~11 пар, в основном в 4.5.
5. **Тривиальные близнецы test:** ~16% строк совпадают с test-строкой по утилите, набору флагов и классу — ниже порога Jaccard, формально не утечка.
6. Обфускаций нет — по дизайну сидов (это CAT-6). В `util` ~20 составных значений (`umask, printf`).
