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

Нужно ОЗУ ≈ размер GGUF + 1–2 ГБ на контекст 8192: на 8 ГБ — модели до 4B в Q4; на 24 ГБ — все три модели train v0 (7B/8B ≈ 5 ГБ, 12B ≈ 7,3 ГБ в Q4_K_M). Пример с abliterated-моделью:

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

### Полные сиды коллег (пары risky/safe) — шаблон v2

TRAIN-сиды из репозитория данных (`CAT-N.M/seeds/*-TRAIN-S*.txt`) — это полные промпты со своим форматом
ответа: одна пара `{"risky": {...}, "safe": {...}, "review": {...}}` или `{"rejected": true, "reason": ...}`.

```bash
python3 tools/convert_txt_seeds.py --repo .. --ref origin/feat/data_Cat-6.5 \
    --risk CAT-1.4 CAT-5.1 CAT-5.2 CAT-5.3 CAT-5.4 --out seeds/train
python3 -m cgen check --config configs/train_v0_pairs.mock.json
```

- Конвертер читает файлы прямо из git-ветки, пишет `origin` (ветка, коммит, путь, sha256) и отказывается брать
  сиды, помеченные как TEST (README папки или текст файла), без `TRAIN` в имени или с чужим `risk=`.
- `prompts/generation_v2.md` передаёт сид модели без изменений (system — только «ответь JSON»).
- `clean` понимает парный формат: пара живёт или уходит целиком (`pair_id`, `role`); `{"rejected": true}` —
  причина `model_refused`; `review` модели сохраняется в `provenance.jsonl`.
- Метки берутся из `labels.pair_contract` (по подкатегории, из текста сидов). Метка модели оставляется, если
  контракт её допускает. Конфликт с контрактом, неполная метка или отсутствие метки при неоднозначном контракте —
  пара отклоняется целиком (`pair_label_conflict`), метка не подменяется. Разные утилиты в сторонах —
  `pair_util_mismatch`; любой ответ с `rejected` — `model_refused`. Нет контракта — `no_pair_contract`.
- После dedup/validate сторона без пары отбрасывается (`pair_partner_rejected`): у опасного примера всегда есть контрпример.
- `export.seed_column: "full_request"` — в колонке `seed` ровно те сообщения, что ушли в модель (сверяется с
  `prompt_sha` в `raw.jsonl`; если сиды или шаблон поменялись после generate — export падает).
- `clean.strip_cyrillic_comment_lines: true` вырезает целые строки-комментарии с кириллицей и заголовки
  `# TASK:`/`# FS:`/`# ENV:` на любом языке (их требуют сиды; подсказывают метку и отсутствуют в test). Shebang и обычные
  английские комментарии не трогаются. Кириллица в остальной части команды по-прежнему отказ `non_ascii_command`.
- `category`/`risk` в CSV — голые коды (`CAT-5`, `CAT-5.1`), как в test-CSV; названия из `taxonomy.json` идут только в промпт v1.

### Train v0: три модели (локально, Mac 24 ГБ)

Решение 21.11 (Влад): вместо утверждённой 7–12B-тройки — модели покрупнее, по итогам ревью-итерации 1
(одни 10 сидов, ручное ревью): новая тройка 6/30 годных пар против 1/30 у старой. Все abliterated (huihui-ai),
коммит HF и файл зафиксированы в `backend.model`. Команде/ментору — сообщить в чат.

| Конфиг | Модель | Квант, ГБ | Вызовов на seed | Доля | с/вызов (M5 Pro) |
|---|---|---|---|---|---|
| `configs/train_v0_qwen38_27b.json` | Huihui-Qwen3.8-27B-abliterated | UD-IQ4_XS, 14,4 | 2 | 40% | ~42 |
| `configs/train_v0_gemma4_26b_a4b.json` | Huihui-gemma-4-26B-A4B-it-abliterated (квант groxaxo) | UD-IQ4_XS, 13,4 | 2 | 40% | ~10 |
| `configs/train_v0_devstral24b.json` | Huihui-Devstral-Small-2-24B-Instruct-abliterated | IQ4_XS, 12,9 | 1 | 20% | ~28 |

Старые конфиги (`train_v0_qwen25coder7b`, `train_v0_gemma3_12b`, `train_v0_llama31_8b`) оставлены как база сравнения.
Локальный прогон по очереди моделей: `tools/review_loop.py` (поднимает llama-server на 127.0.0.1). Colab T4 для
моделей 24–27B не подходит по памяти/скорости; старая инструкция ниже — только для 7–12B.

```bash
# Colab, GPU T4. Один раз: llama.cpp с CUDA (~10 мин)
git clone --depth 1 https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build -DGGML_CUDA=ON && cmake --build build -j --target llama-server && cd ..
pip install -q huggingface_hub

# На каждую модель: скачать ровно тот коммит, что в конфиге, поднять сервер, прогнать
python3 -c "from huggingface_hub import hf_hub_download as d; print(d('bartowski/Qwen2.5-Coder-7B-Instruct-abliterated-GGUF', 'Qwen2.5-Coder-7B-Instruct-abliterated-Q4_K_M.gguf', revision='a416f57ecabe9841551055493e6945895e54e135'))"
llama.cpp/build/bin/llama-server -m <путь из строки выше> --jinja -c 8192 -ngl 99 --port 8080 &
until curl -sf localhost:8080/health; do sleep 5; done
python3 -m cgen check --config configs/train_v0_qwen25coder7b.json
python3 -m cgen generate --config configs/train_v0_qwen25coder7b.json --limit 3   # сначала 3 пробных вызова
python3 -m cgen run --config configs/train_v0_qwen25coder7b.json --resume         # остальное; сессия упала — снова --resume
```

`data/test/` (см. ниже) нужен и в Colab: `dedup.against` без него не пройдёт `cgen check`.

### Антиутечка: test- и real-команды для `dedup.against`

```bash
git -C .. fetch origin
python3 tools/pull_test_data.py --repo .. --out data/test   # все commands.csv, commands_test.csv, CAT-7 inputs, логи D2
```

`dedup.against` принимает папку (`"../data/test"` из `configs/`): берутся все `*.csv`/`*.jsonl` рекурсивно.
Сравнение — после схлопывания пробелов и без строк-комментариев (`# TASK`/`# FS`), иначе test-команда под
заголовком проходила бы. `data/` в `.gitignore`. `split=train` с настоящей моделью и пустым `dedup.against` —
ошибка уже на `cgen check`. Near-dup (эмбеддинги) пока отдельным шагом не реализован.

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


