# Повторный research через Keenable

Дата: 2026-10-29. Прямое указание пользователя: повторить research через доступный Keenable MCP, чтобы найти дополнительные источники и редкие датасеты. Цель текущей редакции — 250 записей суммарно, см. [target-revision](../docs/target-revision.md). Это журнал исследовательских наблюдений, не утверждение о принятии всех найденных команд.

## Метод

Использованы `search_web_pages` и `fetch_page_content` Keenable через MCP devices. Discovery snippets давали leads, а пригодность проверялась по actual pinned cards/files/records и условиям исходных компонентов. Keenable может вернуть cached page без YAML или старое содержимое: pinned original README и actual dataset metadata имеют приоритет. Несовпадения не скрывались. Ни одна команда, dataset-скрипт, shell payload или cloud/container/DB/IaC CLI не исполнялись.

Общие запросы руководителя (дополнительные per-risk queries перечислены в expansion-research.md каждого shard):

1. `Public downloadable dataset of dangerous terminal Bash commands cloud infrastructure database deletion with safety labels and command text GitHub Hugging Face`
2. `Research dataset real AI coding agent terminal trajectories terraform kubectl docker destructive actions command safety benchmark public data`
3. `Bash shell command safety benchmark dataset destructive commands infrastructure database drop SafeShell ShellSafe benchmark downloadable license`

## Новые редкие корпуса: actual inspection

### ShellRisk-Bench

- Источник: https://huggingface.co/datasets/kontext-security/ShellRisk-Bench ; pinned revision `437467862139b4e9cdd5322024ef3434a67c7ec8`.
- Actual schema: command, id, label, source, upstream_id. Оба Parquet split целиком прочитаны **как инертные данные в памяти**, 20 966 записей. Подстрочный regex по семействам terraform/pulumi/kubectl/docker/podman/redis-cli/psql/mysql/dropdb/gsutil/gcloud/AWS S3/Azure storage нашёл 39 упоминаний; это не 39 пригодных CAT-3 примеров и не доказательство исчерпывающего отсутствия других утилит.
- Прочитан фактический https://github.com/kontext-security/shellrisk-bench/blob/main/DATASETS.md . Apache-2.0 относится к benchmark code/docs, **не ко всем данным**: SWE-smith MIT, Terminal-Bench Apache, nl2bash MIT, Atomic Red Team MIT, GTFOBins GPL-3.0, InternalAllTheThings без установленного license grant. Источник сохраняет upstream IDs и pins, но заменяет URL/IP/длинные base64 и получает часть labels из benign task context. Такие labels нельзя принять без самостоятельной разметки, а замены могут повредить точный смысл команды.
- В actual train DATA record 1068 найден metadata-only Secret inventory из Atomic Red Team; исходный upstream и MIT-лицензия переданы CAT-3.2 worker для независимой проверки и возможного восстановления безопасной пары. Другие строки включают нерелевантный исходный код/тесты, контейнерные escape/security действия и комбинацию prune с log truncation, не автоматически принимаемые CAT-3 примеры.
- Hugging Face `/search` endpoint для 16 split/query сочетаний дал HTTP 500 или timeout. Это сбой поискового endpoint, **не недоступность датасета**: actual Parquet успешно прочитан напрямую. Исходные Parquet/полный корпус на диск не сохранялись.

### Permission Command Corpus

- Источник: https://huggingface.co/datasets/cowWhySo/permission-command-corpus ; pinned revision `f9362497c1cc4bd16730cb5abd42396ad1d0142c`.
- Прочитан pinned README с Apache-2.0 assertion и warnings, а не только краткая cached card. Actual gold CSV: **321 запись**, источники 230 `openrouter:qwen/qwen3.6-plus-preview:free` и 91 `deterministic_seed`; по указанному utility regex — 0 упоминаний. Model-generated корпус нельзя выдать за человеческие реальные инциденты.
- Actual silver CSV содержит **0 записей** (только header); actual review CSV — **3216 записей**, из них 2419 Atomic Red Team, 467 LOLBAS, 229 Sigma, 101 Falco. По utility regex 49 упоминаний, все Atomic Red Team. Review intentionally не gold; строки слипают многострочные команды и сохраняют `#{...}` placeholders, так что не являются готовым корректным Bash без проверки upstream.
- README прямо раскрывает generator leakage: заявленные pooled ROC AUC 0.9972 падают до 0.7010 held-out-by-generator; предыдущие constant-score classifiers withdrawn. Эта оценка не переносится на текущий датасет и не используется как подтверждение labels.
- Полные gold/review файлы прочитаны в памяти, не сохранены. Работникам переданы точные upstream YAML locators, а не синтезированные shell wrappers. Прямое принятие gold/review не разрешено одним словом gold или Apache metadata assertion.

### Shell Safety

- Источник: https://huggingface.co/datasets/tomngdev/shell-safety ; pinned revision `155dbb5d3047dd095523bd8ee3dd65adf1296dde`.
- Actual card прямо говорит **synthetic**, metadata MIT; полный объявленный корпус 85 013 записей. Полностью прочитан только small subset train/validation/test: **6002 фактические записи**, не весь корпус.
- Actual schema каждой записи: category, command, reason, safe, session_context, shell. В small subset 4802 posix, 789 powershell, 411 cmd; 572 utility-regex упоминания, 179 cloud и 179 docker категории. Полей model/generation prompt/seed нет. Представленные synthetic session contexts не доказывают реальные approval/production/ownership.
- Модель и полный генерационный prompt не установлены, поэтому подходящие по внешнему виду строки не импортируются как real и не закрывают deficit. Full corpus не скачан, actual small subset на диск не сохранён.

## Дополнительные leads и ограничения

Keenable нашёл TerminalWorld, Terminal Wrench, Saber, V3AST-Bench, terminal-command-execution-sft, threat_detection_cli_validation_set и другие специализированные shell-safety/model cards. Per-risk workers отдельно проверяют доступность, actual records, licensing и происхождение. Одно наличие названия benchmark не устанавливает CAT-3 yield.

Работники независимо обнаружили у TerminalWorld конфликт README author-created-artifacts CC-BY-4.0 с per-record CC-BY-NC-4.0, помеченным upstream как устаревший до обновления, а также benchmark contamination notices и LLM synthesis/refinement. Engine Apache-2.0 не лицензирует автоматически датасет/оригинальные записи терминала. Эти условия и происхождение требуют review; примеры не копировались в accepted dataset по одному сниппету и не называются сырыми реальными trace.

## Инструменты и границы проверки

Финальные integrator/validator остаются Python standard-library-only. Для **разового research-only** чтения Parquet установлен PyArrow **26.0.0** в отдельный временный virtualenv вне репозитория. Первая `%pip install` отвергнута externally-managed environment; системная защита не обходилась, `--break-system-packages` не использовался. Изолированный parser действительно прочитал оба ShellRisk Parquet. Это не новая зависимость финального pipeline и не разрешение исполнять датасет.

Поиск делится по всем пяти рискам; новые источники/queries, принятые proposals, licensing caveats и оценка доступного объёма — в `data/candidates/CAT-3.N/expansion-research.md`. Финальные числа определяются только после независимого semantic/provenance review, pairing closure и глобальной дедупликации. Здесь приведены измеренные размеры просмотренных источников, не обещание выхода и не финальные counts.

## Подтверждённые поисковые интерфейсы

Для справки внешнему ментору дополнительно проверен локальный архив текущей ingestion-сессии `01a1873b-3e40-7417-8cfd-4007344cb862`: исходные записи типов `function_call` и `toolCall` действительно содержат вызовы встроенного `web_search`, включая поиск sandbox architecture. Это подтверждает интерфейс первого этапа, но не раскрывает его underlying search engine; Google/Bing ему не приписываются. Число найденных сериализованных представлений не объявляется числом уникальных запросов.

Повторный этап использует Keenable `search_web_pages` и `fetch_page_content`; точные запросы и результаты отражены выше и в per-risk журналах. GitHub/Hugging Face API, raw-файлы и архивы — каналы получения оригиналов, а не дополнительные поисковые провайдеры.
