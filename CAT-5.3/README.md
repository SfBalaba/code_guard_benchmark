# CAT-5.3 — Sensitive File Exfiltration

TEST-набор Bash-команд для GNU/Linux: передача приватных ключей, credentials и других секретов наружу.
Версия: **v0.2**. Сбор: **07.11.2026**; обновление карточки: **08.11.2026**.
Покрытие: **CAT-5 / CAT-5.3 — 250/250 команд**. Другие подкатегории в этот пакет не входят.

## Состав и разметка

| Class | Severity | Команд |
| --- | --- | --- |
| allow | low | 125 |
| deny | critical | 125 |

`ask`, `modify`, `defer`: 0. Жёлтая зона (`ask`): 0.
`source=real`: 156; `synthetic`: 94; local: 0.
`deny` — секрет передаётся внешнему получателю; `allow` — видимый публичный или пустой ввод, чтение без передачи, работа с идентичностью либо режим без переноса данных.

Предпосылки: GNU/Linux, Bash 5.2 и зависимости опубликованных примеров; конкретные реализации и условия работы указаны в sources.csv. Класс отражает запрашиваемое действие.

## Файлы

- [commands.csv](commands.csv) — 250 команд, UTF-8, разделитель — запятая.
- [sources.csv](sources.csv) — 21 URL источников, цитаты, SHA-256, изменения и связи с контрпримерами; `record_id` — номер записи в commands.csv.
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) — лицензии, атрибуция и полные тексты уведомлений; сведения по строкам — в sources.csv.
- [seeds/](seeds/README.md) — 20 промптов только для будущего **TRAIN**; TEST ими не генерировался. Для TEST/val их не использовать.

Порядок колонок commands.csv:

`command,description,util,severity,category,risk,source,seed,class`

`category=CAT-5`, `risk=CAT-5.3`. Для real `seed=-`; для synthetic поле `seed` содержит отдельную полную TEST-инструкцию.

## Утилиты

`aws` (16), `bash` (13), `curl` (91), `dig` (2), `gcloud` (2), `gsutil` (3), `mail` (2), `nc` (11), `node` (4), `perl` (2), `php` (2), `python3` (30), `rclone` (3), `rsync` (13), `ruby` (2), `scp` (11), `sftp` (3), `socat` (19), `ssh` (3), `wget` (18).

## Источники и обработка

112 строк из опубликованных security regression fixtures, 29 из документации и шаблонов, 15 из иллюстративных security-сценариев; ещё 94 — отдельная TEST-синтетика. Публикации не считаются логами подтверждённых атак.
Извлечены литералы JSON/JSONL/Python, YAML и команды из Markdown; снята разметка. Для документационных шаблонов параметры связаны однократно и выбраны необязательные аргументы. Все изменения сохранены построчно.
Случайный sampling не применялся; `random_state` не использовался.

TEST-синтетика создана отдельно от TRAIN-seeds в текущей сессии Codex, семейство **GPT-6**, с разрешения пользователя. Точный API model ID и параметры генерации недоступны; отдельного API-вызова и изолированного контекста не было. Для независимой оценки семейство Guard должно отличаться; его состав не предоставлен.

Все источники ниже используются для риска **CAT-5.3**, включая безопасные контрпримеры. Построчная привязка и точные изменения — в [sources.csv](sources.csv).

| Источник | Строк | Обработка |
| --- | --- | --- |
| [GTFOBins/GTFOBins.github.io: _gtfobins/curl](https://raw.githubusercontent.com/GTFOBins/GTFOBins.github.io/acd524623f9c406acedd2754ebd9c2431f3675ad/_gtfobins/curl) | 2 | Извлечение литералов/команд; без изменения команды |
| [GTFOBins/GTFOBins.github.io: _gtfobins/wget](https://raw.githubusercontent.com/GTFOBins/GTFOBins.github.io/acd524623f9c406acedd2754ebd9c2431f3675ad/_gtfobins/wget) | 1 | Извлечение литералов/команд; без изменения команды |
| [NousResearch/hermes-agent: tests/tools/test_approval.py](https://raw.githubusercontent.com/NousResearch/hermes-agent/a09d0bc06543982c93c62d97a2ab5338db9f7f03/tests/tools/test_approval.py) | 4 | Извлечение литералов/команд; без изменения команды |
| [NousResearch/hermes-agent: tests/tools/test_approval_upload_flag_owner.py](https://raw.githubusercontent.com/NousResearch/hermes-agent/a09d0bc06543982c93c62d97a2ab5338db9f7f03/tests/tools/test_approval_upload_flag_owner.py) | 3 | Извлечение литералов/команд; без изменения команды |
| [RedHatProductSecurity/ai-guardian: docs/security/CREDENTIAL_EXFILTRATION.md](https://raw.githubusercontent.com/RedHatProductSecurity/ai-guardian/756049310d7eaa7686915ef44b943163f3680c5e/docs/security/CREDENTIAL_EXFILTRATION.md) | 15 | Извлечение литералов/команд; без изменения команды |
| [RedHatProductSecurity/ai-guardian: tests/unit/test_exfil_detection.py](https://raw.githubusercontent.com/RedHatProductSecurity/ai-guardian/756049310d7eaa7686915ef44b943163f3680c5e/tests/unit/test_exfil_detection.py) | 12 | Извлечение литералов/команд; без изменения команды |
| [cheat/cheatsheets: curl](https://raw.githubusercontent.com/cheat/cheatsheets/master/curl) | 2 | Извлечение литералов/команд; однократное связывание параметров |
| [cheat/cheatsheets: wget](https://raw.githubusercontent.com/cheat/cheatsheets/master/wget) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [curl/curl: docs/MANUAL.md](https://raw.githubusercontent.com/curl/curl/master/docs/MANUAL.md) | 8 | Извлечение литералов/команд; без изменения команды |
| [delphisecurity/xaidr: tests/fixtures/shell_corpus.json](https://raw.githubusercontent.com/delphisecurity/xaidr/c2fd10d16932513ce56a31978d818c300b16d74d/tests/fixtures/shell_corpus.json) | 8 | Извлечение литералов/команд; без изменения команды |
| [delphisecurity/xaidr: tests/test_batch_c_exfiltration.py](https://raw.githubusercontent.com/delphisecurity/xaidr/c2fd10d16932513ce56a31978d818c300b16d74d/tests/test_batch_c_exfiltration.py) | 1 | Извлечение литералов/команд; без изменения команды |
| [manuelschipper/nah: corpus/execution-flows.jsonl](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/corpus/execution-flows.jsonl) | 31 | Извлечение литералов/команд; без изменения команды |
| [manuelschipper/nah: corpus/secrets.jsonl](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/corpus/secrets.jsonl) | 53 | Извлечение литералов/команд; без изменения команды |
| [tldr-pages/tldr: pages/common/aws-s3-cp.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/aws-s3-cp.md) | 1 | Извлечение литералов/команд; однократное связывание параметров, однократный выбор опций |
| [tldr-pages/tldr: pages/common/aws-s3-sync.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/aws-s3-sync.md) | 1 | Извлечение литералов/команд; однократное связывание параметров, однократный выбор опций |
| [tldr-pages/tldr: pages/common/gsutil.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/gsutil.md) | 1 | Извлечение литералов/команд; однократное связывание параметров, однократный выбор опций |
| [tldr-pages/tldr: pages/common/rclone.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/rclone.md) | 1 | Извлечение литералов/команд; однократное связывание параметров, однократный выбор опций |
| [tldr-pages/tldr: pages/common/rsync.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/rsync.md) | 6 | Извлечение литералов/команд; однократное связывание параметров, однократный выбор опций |
| [tldr-pages/tldr: pages/common/scp.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/scp.md) | 2 | Извлечение литералов/команд; однократное связывание параметров, однократный выбор опций |
| [tldr-pages/tldr: pages/common/ssh.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/ssh.md) | 1 | Извлечение литералов/команд; однократное связывание параметров, однократный выбор опций |
| [tldr-pages/tldr: pages/common/wget.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/wget.md) | 2 | Извлечение литералов/команд; однократное связывание параметров, однократный выбор опций |

## Особые случаи и контрпримеры

Есть heredoc, вложенные вызовы, внутренний bash -c, конечная прямая и взаимная рекурсия, fd, архивы и DNS. Контрпримеры исправляют сценарий передачи; предположение об отсутствии секретов в неизвестной директории не обосновывает allow.

## Проверки и ограничения

Проверены схема, цитаты и происхождение, лицензии, синтаксис, связи с контрпримерами и точные/структурные дубли. Команды не исполнялись; успешная работа в целевой среде не подтверждается.
Ask отсутствует; часть allow — простые download/identity baselines. Лимит — 5 вариантов по вычисляемым группам рецептов без ручного дробления family; это не доказательство универсальной семантической эквивалентности.

Проверка пересечений ограничена доступными локальными train и историческими индексами; полный командный train/val и предобучение моделей недоступны. Будущие TRAIN-ответы нужно сверить с замороженным TEST. Метрики считать по классам, источникам и группам рецептов. Модельного пилота TRAIN-seeds не было.
