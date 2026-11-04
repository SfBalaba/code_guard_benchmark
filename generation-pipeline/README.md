# CodeGuard-Bench: каркас генерации синтетики

Скрипт генерирует синтетические bash-команды по seed (seed — это промпт-инструкция генератору,
а не готовая команда и не числовой random seed), отсеивает брак и собирает CSV в формате гайдлайна
(9 колонок, классы `allow`/`ask`/`deny`). Датасет нужен для модели-фильтра, которая проверяет команды
кодового агента до выполнения.

Код отвечает за то, **как** генерировать. **Что** получится, задаёт конфиг: модель, сервер,
параметры семплирования, seed, шаблон промпта, список классов. Новая категория или модель —
это новый конфиг, код не меняется.

```
load_seeds → generate → clean → dedup → validate → export (+ report)
```

На каждом шаге отсеянное пишется в `rejected_<шаг>.jsonl` с причиной, а `report.md` сводит всё вместе.
Validate проверяет не только формат: синтаксис (`bash -n`), выдуманные флаги утилит по словарю из man-страниц
и сомнительные метки (правила-якоря, строки уходят в `review_queue.jsonl`). Ни одна команда не исполняется.

Зависимостей нет, нужен только Python 3.10+ и `bash` (для проверки синтаксиса). Сеть нужна только
для пересборки словарей флагов (`tools/build_flags.py`); готовые словари лежат в `flags/`.

## Структура

| Путь | Что это |
|---|---|
| `cgen/` | код шагов: `generate`, `clean`, `dedup`, `validate`, `export`, `report`; `backends.py` (mock / OpenAI-совместимый) |
| `cgen/shparse.py`, `flagcheck.py`, `anchors.py` | разбор bash-команды, проверка флагов, правила-якоря меток |
| `configs/` | `mock.json`, `mock_dirty.json` (без модели), `openai_compatible.example.json` (шаблон), `local_qwen.json` (локальная модель) |
| `prompts/generation_v1.md` | шаблон промпта генерации |
| `examples/` | `seeds_example.jsonl` — формат-заглушка; `seeds_local_test.jsonl` — тестовые seed для локальной модели (не для настоящих прогонов) |
| `flags/` | словари флагов утилит (генерируются `tools/build_flags.py`) |
| `taxonomy.json` | названия категорий/подкатегорий |
| `tests/` | тесты (`unittest`) |
| `runs/` | результаты прогонов (`<run_name>/`) |

## Быстрый старт

```bash
python3 -m cgen run --config configs/mock.json          # прогон без модели
python3 -m unittest discover -s tests -v                # тесты
```

Результат лежит в `runs/<run_name>/`, главное — `dataset.csv` и `report.md`.

## Запуск с настоящей моделью

1. Подними модель где угодно за OpenAI-совместимым API (`/v1/chat/completions`):
   llama.cpp `llama-server`, vLLM, Ollama, OpenRouter, облачный API.
2. Скопируй `configs/openai_compatible.example.json` и поправь:
   - `backend.base_url`, `backend.model`;
   - `backend.api_key_env` — **имя** переменной окружения с ключом (сам ключ в конфиг не пишется), `null` если ключ не нужен;
   - `seeds_path` — твой файл seed.
3. Проверка без вызовов модели: `python3 -m cgen check --config my.json`,
   посмотреть собранные промпты: `python3 -m cgen generate --config my.json --dry-run`.
4. Запуск: `python3 -m cgen run --config my.json`. Если оборвалось —
   `python3 -m cgen generate --config my.json --resume`, потом `python3 -m cgen clean --config my.json` и дальше по шагам
   (или снова `run --resume`).
5. Поменял только настройки проверок — модель заново звать не нужно:
   `python3 -m cgen validate --config my.json`, затем `export` и `report`.

### Локально на Mac (llama.cpp)

На M1 с 8 ГБ комфортно работают модели до 4B в Q4. Пример с abliterated-моделью:

```bash
brew install llama.cpp
llama-server -hf mradermacher/Huihui-Qwen3.5-4B-abliterated-GGUF:Q4_K_M --jinja -c 8192 --port 8080 --no-mmproj
curl -s localhost:8080/health                              # {"status":"ok"} — готов
python3 -m cgen run --config configs/local_qwen.json
```

Qwen по умолчанию «думает» перед ответом (съедает `max_tokens`, ломает JSON) — в `configs/local_qwen.json`
это выключено через `backend.extra_body: {"chat_template_kwargs": {"enable_thinking": false}}`.
Скорость ~11–16 ток/с: один вызов на 4 команды — 20–40 с, поэтому `timeout` в конфиге увеличен до 300.

## Конфиг

| Поле | Что задаёт |
|---|---|
| `run_name`, `output_dir` | куда писать: `<output_dir>/<run_name>/` |
| `split` | `test` или `train`; все seed должны быть из этого split |
| `seeds_path` | JSONL с seed |
| `taxonomy_path` | названия категорий/подкатегорий для колонок `category`, `risk` |
| `prompt.template`, `prompt.version` | шаблон промпта и его версия |
| `prompt.candidates_per_call` | сколько команд просить за один вызов |
| `backend` | `mock` или `openai_compatible` (+ `base_url`, `model`, `api_key_env`, `json_mode`, `timeout`, `retries`, `extra_body`) |
| `sampling` | `temperature`, `top_p`, `max_tokens`, `seed` (числовой), `samples_per_seed` |
| `seeds.allowed_statuses` | какие `status` seed пускать в генерацию |
| `labels.classes`, `labels.severities` | допустимые значения (3 или 5 классов — как решим) |
| `clean` | `max_command_chars`, `allow_non_ascii_command` |
| `dedup.against` | CSV/JSONL, команды из которых нельзя повторять (например, test при генерации train) |
| `validate.bash_syntax_check` | проверять ли синтаксис через `bash -n` |
| `validate.flag_check` | `reject` (по умолчанию) / `warn` / `off` — проверка флагов по словарю `flags/` |
| `validate.flags_dir` | своя папка словарей флагов; `null` — `flags/` в репозитории |
| `validate.label_anchors` | правила-якоря для меток (`label_conflict` → `review_queue.jsonl`), по умолчанию `true` |
| `export.seed_column` | что писать в колонку `seed`: текст (`prompt`) или `seed_id` |

`extra_body` уходит в запрос как есть — туда кладутся параметры конкретного сервера (`top_k`, `min_p` и т.п.).
Если сервер не поддерживает `response_format`, поставь `json_mode: false`.

## Формат seed

JSONL, одна запись на строку. Совместим с `d3-judge-pipeline`:

```json
{"seed_id": "TRAIN-CAT-6.1-01", "split": "train", "risk": "CAT-6.1", "family_id": "CAT-6.1/...",
 "prompt": "текст инструкции генератору", "mechanism": "...", "source_kind": "abstract_synthetic_spec",
 "status": "approved_for_generation"}
```

Скрипт отклоняет seed, если: нет обязательных полей; повторяется `seed_id`; split не совпадает с запуском;
`risk` не вида `CAT-N.M`; есть `few_shot` или `source_commands` (реальные примеры запрещены);
`source_kind` не `abstract_synthetic_spec`; `status` не из разрешённых.

`examples/seeds_example.jsonl` — только пример формата с текстом-заглушкой, генерировать по нему нельзя.

## Шаги и файлы

| Шаг | Вход → выход | Что делает |
|---|---|---|
| generate | seed → `raw.jsonl`, `manifest.json` | по строке на вызов модели с сырым ответом; свой числовой seed на каждый вызов; `--resume` |
| clean | `raw.jsonl` → `candidates.jsonl`, `rejected_clean.jsonl` | достаёт JSON (убирает `<think>`, markdown, текст вокруг), чистит команды: обёртки, `$ `, двойное экранирование кавычек; отбрасывает пустые, слишком длинные, с иероглифами/управляющими символами |
| dedup | → `deduped.jsonl`, `rejected_dedup.jsonl` | точные дубликаты после схлопывания пробелов, внутри запуска и против `dedup.against` |
| validate | → `validated.jsonl`, `rejected_validate.jsonl`, `review_queue.jsonl` | `class`/`severity` из списков, нет секретов, синтаксис через `bash -n`, флаги по словарю, метки по правилам-якорям (команда не исполняется) |
| export | → `dataset.csv`, `provenance.jsonl` | 9 колонок гайдлайна; `source=synthetic`; связь строки с seed, моделью и версией промпта — в `provenance.jsonl` |
| report | → `report.json`, `report.md` | отсев по шагам и причинам, баланс классов/severity/risk, разнообразие утилит, покрытие конструкций (`bash -c`, пайпы, подстановки, heredoc, циклы…), выход по каждому seed |

`manifest.json` хранит хеши конфига, шаблона и seed: `--resume` откажет, если что-то из этого поменялось.

## Проверка флагов и меток

Модель часто выдумывает флаги (`journalctl --zero-logs`, `logrotate --delay`) и ставит неверные метки
(удаление истории как `allow`). `bash -n` этого не видит, поэтому в validate есть ещё две проверки.

**Флаги** (`cgen/flagcheck.py`). Команда разбирается на простые команды (`cgen/shparse.py`: пайпы, `&&`,
`$(…)`, `<(…)`, `bash -c "…"`; снимаются `sudo`, `env`, `nohup`, `timeout`, `xargs` …), флаги каждой
сверяются со словарём `flags/<util>.json`. Нет флага — `unknown_flag:<util>:<флаг>`; значение не подходит
под шаблон — `bad_flag_value` (сейчас только `history -d` — номер, а не дата). Не отказываем, если не уверены:
утилиты без словаря (`flags_unchecked:<util>` в отчёте), имя команды из переменных (`$a $b` — это CAT-6.2,
не ошибка), утилиты со своим синтаксисом (`find`, `dd`, `tar`, `git`, `openssl`, `iptables` …) не проверяются.

Словари собираются из man-страниц Debian (GNU/Linux-флаги, не macOS), Linux для сборки не нужен:

```bash
python3 tools/build_flags.py            # все утилиты из списка UTILS в скрипте
python3 tools/build_flags.py curl wget  # выборочно
```

Встроенные команды bash (`history`, `set`, `unset`, `kill` …) заданы вручную в `BUILTINS`. Особый синтаксис
(`chmod -x`, `chattr -i`, `nc -e` из netcat-traditional, `wget -mnp`) — в `OVERRIDES`. Новая утилита —
строка в `UTILS` (пакет Debian и секция man) и перезапуск скрипта.

**Метки** (`cgen/anchors.py`). Узкие правила для однозначных случаев: исполнение раскодированного
base64/hex, очистка/отключение истории, стирание логов, отключение SELinux/аудита/файрвола →
ожидается `deny`/`ask`; команда только читает (cat/grep/tail…, запись лишь в `/tmp`) → ожидается `allow`.
Расхождение — **предупреждение**, а не отказ: строка попадает в `review_queue.jsonl` и в отчёт.
`/etc/hosts` и CA-хранилище правилами не покрыты: там есть легитимные `allow` (локальные домены,
корпоративный CA).

**Как проверялось.** Команды из ручного test-набора (`CAT-6_dataset_v0`) в правила и словари не копировались,
но набор использовался для замера ложных срабатываний: 0 `unknown_flag` и 0 `label_conflict` на 100 строках.
Это замер *в выборке*: правило для `/etc/hosts`/CA убрано именно после расхождения с ручной разметкой.
Независимая проверка словарей — примеры tldr-pages для тех же утилит: из 544 примеров срабатываний 4,
все на плейсхолдерах tldr (`-1..9`, `-group_id`, `history -d offset`). Если на реальных данных появятся
ложные `unknown_flag`, временно поставь `validate.flag_check: "warn"` и поправь `OVERRIDES` в `tools/build_flags.py`.


