# CAT-6.3 — Audit & History Erasure

TEST-набор, очистка shell-history и системных журналов, безопасные контрпримеры. Покрытие CAT-6.3, 250 команд. Версия v0.3-mixed, обновление 12.11.2026.

## Состав и разметка

| Class | Severity | Команд |
| --- | --- | --- |
| allow | low | 188 |
| deny | high | 62 |

Остальные классы — 0. Источники, 226 real, 24 synthetic, local — 0.
deny/high — удаление записанных событий, allow/low — чтение, сохранение записей и обслуживание собственных тестовых логов.

GNU/Linux и Bash 5.2, для отдельных примеров требуется macOS. Для builtin history нужен текущий интерактивный Bash. В изменяющих application-log примерах создание собственного каталога и файлов видно в command.

## Файлы

- [commands.csv](commands.csv) — TEST, UTF-8, разделитель запятая.
- `seeds/` в комплекте для PR — 20 отдельных TRAIN-заданий для безопасных Bash-контрпримеров и текстовых сценариев оценки риска.

Порядок колонок: `command,description,util,severity,category,risk,source,seed,class`. Во всех 226 строках `real` в поле `seed` стоит `-`. Во всех 24 строках `synthetic` поле `seed` содержит полный текст отдельного TEST-задания, зафиксированного до подготовки ответа. Промпты из экспортируемой папки `seeds/` в CSV не использованы. Переводы строк и значимый синтаксис сохранены. Правки по источникам указаны ниже. Случайный отбор не применялся.

## Утилиты

`atuin`, `auditctl`, `aureport`, `ausearch`, `awk`, `bash`, `cat`, `cp`, `dmesg`, `du`, `echo`, `fc`, `find`, `grep`, `history`, `journalctl`, `last`, `lastb`, `lastlog`, `less`, `log`, `logread`, `logrotate`, `ls`, `mv`, `printf`, `rm`, `sed`, `shred`, `tail`, `tee`, `truncate`, `unlink`, `utmpdump`, `wc`.

## Происхождение и ограничения

Real — опубликованные тесты, документация и примеры сообществ, не подтверждённые инциденты. TEST-синтетика создана отдельно с разрешения пользователя, без TRAIN-seeds. Шаблоны написаны в сессии GPT-6, Guard не относится к GPT по подтверждению пользователя. Нового API-сэмплирования не было, точный backend model ID и полный provider-контекст недоступны. Лицензии баз сохранены для производных.

В TEST есть исполняемый heredoc и конечная рекурсия функций. По ТЗ CAT-6.3 лимит составляет пять близких вариаций вычисляемого рецепта. Валидатор определяет рецепт по тексту команды и находит максимум пять строк в каждой из 92 групп. У всех 62 записей `deny` есть связанный `allow`-контрпример той же утилитой. При дополнительном подсчёте с присоединением контрпримеров из других групп максимум равен девяти. ТЗ CAT-6.3 не задаёт этот подсчёт как критерий приёмки. Синтаксис проверен без исполнения. Проверены доступные TEST и TRAIN. Будущий TRAIN, независимая экспертная приёмка и модельный пилот экспортируемых TRAIN-промптов пока недоступны.

## Источники TEST

Источники относятся к `CAT-6.3`. Ссылки на репозитории ведут на использованные снимки. Правки перечислены для записей, где они применялись.

| Источник | Тип | Real | Synthetic | Лицензии | Правки |
| --- | --- | ---: | ---: | --- | --- |
| [anthony-bible/code-agent-demo @ `6b043ba3b2`](https://github.com/anthony-bible/code-agent-demo/tree/6b043ba3b2e2539924d824acbaa950da76122c55) | опубликованная основа синтетики, тесты | 2 | 1 | Apache-2.0 | сборка по отдельному TEST-заданию, тестовый сценарий на основе источника |
| [Ask Different, ответ 430164](https://apple.stackexchange.com/a/430164) | ответ сообщества | 2 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, вопрос 1308989](https://askubuntu.com/q/1308989) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, вопрос 1349306](https://askubuntu.com/q/1349306) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, вопрос 1456580](https://askubuntu.com/q/1456580) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, вопрос 1504263](https://askubuntu.com/q/1504263) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, вопрос 1545856](https://askubuntu.com/q/1545856) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, вопрос 1563179](https://askubuntu.com/q/1563179) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | удаление приглашения оболочки |
| [Ask Ubuntu, вопрос 605270](https://askubuntu.com/q/605270) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, вопрос 91344](https://askubuntu.com/q/91344) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | удаление приглашения оболочки |
| [Ask Ubuntu, ответ 1307774](https://askubuntu.com/a/1307774) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, ответ 1491766](https://askubuntu.com/a/1491766) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, ответ 1531483](https://askubuntu.com/a/1531483) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, ответ 1550952](https://askubuntu.com/a/1550952) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, ответ 1562934](https://askubuntu.com/a/1562934) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, ответ 1568980](https://askubuntu.com/a/1568980) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, ответ 406681](https://askubuntu.com/a/406681) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | удаление приглашения оболочки |
| [Ask Ubuntu, ответ 524249](https://askubuntu.com/a/524249) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Ask Ubuntu, ответ 536225](https://askubuntu.com/a/536225) | опубликованная основа синтетики | 0 | 1 | CC-BY-SA-3.0 | сборка по отдельному TEST-заданию, тестовый сценарий на основе источника |
| [Ask Ubuntu, ответ 633409](https://askubuntu.com/a/633409) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Ask Ubuntu, ответ 706130](https://askubuntu.com/a/706130) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Ask Ubuntu, ответ 903364](https://askubuntu.com/a/903364) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Ask Ubuntu, ответ 952541](https://askubuntu.com/a/952541) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Ask Ubuntu, ответ 952724](https://askubuntu.com/a/952724) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Ask Ubuntu, ответ 956314](https://askubuntu.com/a/956314) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [atuinsh/atuin @ `28fcb3db32`](https://github.com/atuinsh/atuin/tree/28fcb3db32e5550543fc7ed93537963e246abf7c) | документация | 19 | 0 | MIT | удаление приглашения оболочки |
| [cheat/cheatsheets @ `36bdb99dcf`](https://github.com/cheat/cheatsheets/tree/36bdb99dcfadde210503d8c2dcf94b34ee950e1d) | документация | 4 | 0 | CC0-1.0 | без содержательных правок |
| [delphisecurity/xaidr @ `c2fd10d169`](https://github.com/delphisecurity/xaidr/tree/c2fd10d16932513ce56a31978d818c300b16d74d) | тесты безопасности | 10 | 0 | Apache-2.0 | без содержательных правок |
| [gitGNU/gnu_bash @ `bc007799f0`](https://github.com/gitGNU/gnu_bash/tree/bc007799f0e1362100375bb95d952d28de4c62fb) | тесты | 6 | 0 | GPL-3.0-or-later | без содержательных правок |
| [manuelschipper/nah @ `7230be14c0`](https://github.com/manuelschipper/nah/tree/7230be14c0586c8ebe9a6be0c4d9a43f4949216a) | опубликованная основа синтетики, тесты безопасности | 3 | 1 | MIT | сборка по отдельному TEST-заданию, тестовый сценарий на основе источника |
| [NousResearch/hermes-agent @ `a09d0bc065`](https://github.com/NousResearch/hermes-agent/tree/a09d0bc06543982c93c62d97a2ab5338db9f7f03) | опубликованная основа синтетики, тесты безопасности | 1 | 1 | MIT | сборка по отдельному TEST-заданию, тестовый сценарий на основе источника |
| [redcanaryco/atomic-red-team @ `a0e3f9bc69`](https://github.com/redcanaryco/atomic-red-team/tree/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6) | тесты | 12 | 0 | MIT | подстановка опубликованных значений по умолчанию, удаление некорректного исходного комментария |
| [Stack Overflow, вопрос 46076417](https://stackoverflow.com/q/46076417) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Stack Overflow, вопрос 47890353](https://stackoverflow.com/q/47890353) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Stack Overflow, вопрос 54225341](https://stackoverflow.com/q/54225341) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Stack Overflow, вопрос 65215163](https://stackoverflow.com/q/65215163) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Stack Overflow, вопрос 68755810](https://stackoverflow.com/q/68755810) | опубликованная основа синтетики | 0 | 3 | CC-BY-SA-4.0 | сборка по отдельному TEST-заданию, тестовый сценарий на основе источника |
| [Stack Overflow, вопрос 980283](https://stackoverflow.com/q/980283) | опубликованная основа синтетики | 0 | 1 | CC-BY-SA-2.5 | сборка по отдельному TEST-заданию, тестовый сценарий на основе источника |
| [Stack Overflow, ответ 33444185](https://stackoverflow.com/a/33444185) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Stack Overflow, ответ 33444394](https://stackoverflow.com/a/33444394) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Stack Overflow, ответ 59151960](https://stackoverflow.com/a/59151960) | опубликованная основа синтетики | 0 | 1 | CC-BY-SA-4.0 | сборка по отдельному TEST-заданию, тестовый сценарий на основе источника |
| [Stack Overflow, ответ 68756091](https://stackoverflow.com/a/68756091) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | удаление приглашения оболочки |
| [systemd/systemd @ `ca78951bd3`](https://github.com/systemd/systemd/tree/ca78951bd398e191ebc4550710e33ef34190514e) | документация, тесты | 36 | 0 | LGPL-2.1-or-later | без содержательных правок |
| [tldr-pages/tldr @ `ed1f496b34`](https://github.com/tldr-pages/tldr/tree/ed1f496b347fa32446122aa56e254431e2b50fa0) | документация, опубликованная основа синтетики | 48 | 10 | CC-BY-4.0 | подстановка документированных значений и выбор варианта, сборка по отдельному TEST-заданию, тестовый сценарий на основе источника |
| [Unix & Linux, вопрос 184488](https://unix.stackexchange.com/q/184488) | вопрос сообщества | 2 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 243828](https://unix.stackexchange.com/q/243828) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 272662](https://unix.stackexchange.com/q/272662) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 312528](https://unix.stackexchange.com/q/312528) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 314017](https://unix.stackexchange.com/q/314017) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 386852](https://unix.stackexchange.com/q/386852) | опубликованная основа синтетики | 0 | 1 | CC-BY-SA-3.0 | сборка по отдельному TEST-заданию, тестовый сценарий на основе источника |
| [Unix & Linux, вопрос 405550](https://unix.stackexchange.com/q/405550) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 435719](https://unix.stackexchange.com/q/435719) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | удаление приглашения оболочки |
| [Unix & Linux, вопрос 462266](https://unix.stackexchange.com/q/462266) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 496588](https://unix.stackexchange.com/q/496588) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 503059](https://unix.stackexchange.com/q/503059) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 604769](https://unix.stackexchange.com/q/604769) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 62412](https://unix.stackexchange.com/q/62412) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 644305](https://unix.stackexchange.com/q/644305) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 690567](https://unix.stackexchange.com/q/690567) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 718902](https://unix.stackexchange.com/q/718902) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 721538](https://unix.stackexchange.com/q/721538) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 755616](https://unix.stackexchange.com/q/755616) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 774531](https://unix.stackexchange.com/q/774531) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 796754](https://unix.stackexchange.com/q/796754) | вопрос сообщества | 2 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 797704](https://unix.stackexchange.com/q/797704) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 801911](https://unix.stackexchange.com/q/801911) | вопрос сообщества | 3 | 0 | CC-BY-SA-4.0 | удаление приглашения оболочки |
| [Unix & Linux, вопрос 806257](https://unix.stackexchange.com/q/806257) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | удаление приглашения оболочки |
| [Unix & Linux, вопрос 89006](https://unix.stackexchange.com/q/89006) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 123539](https://unix.stackexchange.com/a/123539) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 123544](https://unix.stackexchange.com/a/123544) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 145456](https://unix.stackexchange.com/a/145456) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 149127](https://unix.stackexchange.com/a/149127) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 150179](https://unix.stackexchange.com/a/150179) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | удаление приглашения оболочки |
| [Unix & Linux, ответ 178956](https://unix.stackexchange.com/a/178956) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 184492](https://unix.stackexchange.com/a/184492) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 275101](https://unix.stackexchange.com/a/275101) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 328153](https://unix.stackexchange.com/a/328153) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 330511](https://unix.stackexchange.com/a/330511) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 350640](https://unix.stackexchange.com/a/350640) | ответ сообщества | 2 | 0 | CC-BY-SA-3.0 | удаление приглашения оболочки |
| [Unix & Linux, ответ 369425](https://unix.stackexchange.com/a/369425) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 370682](https://unix.stackexchange.com/a/370682) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 467856](https://unix.stackexchange.com/a/467856) | ответ сообщества | 2 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 555971](https://unix.stackexchange.com/a/555971) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 573267](https://unix.stackexchange.com/a/573267) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 607279](https://unix.stackexchange.com/a/607279) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 616732](https://unix.stackexchange.com/a/616732) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | удаление приглашения оболочки |
| [Unix & Linux, ответ 669707](https://unix.stackexchange.com/a/669707) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 680906](https://unix.stackexchange.com/a/680906) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 715296](https://unix.stackexchange.com/a/715296) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 721846](https://unix.stackexchange.com/a/721846) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 743063](https://unix.stackexchange.com/a/743063) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 766558](https://unix.stackexchange.com/a/766558) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 766875](https://unix.stackexchange.com/a/766875) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |

Синтетика без внешнего первоисточника: 4 записей. Метод и сведения о модели указаны выше.

## Атрибуция и лицензии

Published excerpts retain their source licenses, independently of dataset labels. No blanket MIT license is asserted for this collection. Changes on 2026-11-08 and 2026-11-09: extraction, shell-prompt removal, one documented template/default binding where recorded, a consistent absolute time interval, and removal of one incorrect upstream comment without changing executable tokens. Four records separately marked synthetic are original session-authored TEST examples, not third-party excerpts. Source URLs, exact excerpts, immutable refs/snapshot hashes, authors, license scope and per-row changes are in sources.csv. Community adaptations remain under each stated CC BY-SA version. No additional restrictions are imposed on those excerpts.

### atomic — MIT

Red Canary, Inc. (2018). [Applicable license](https://raw.githubusercontent.com/redcanaryco/atomic-red-team/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6/LICENSE.txt); [scope](https://raw.githubusercontent.com/redcanaryco/atomic-red-team/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6/LICENSE.txt).
- [atomics/T1070.003/T1070.003.yaml](https://raw.githubusercontent.com/redcanaryco/atomic-red-team/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6/atomics/T1070.003/T1070.003.yaml), ref `a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6`.
- [atomics/T1685.006/T1685.006.yaml](https://raw.githubusercontent.com/redcanaryco/atomic-red-team/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6/atomics/T1685.006/T1685.006.yaml), ref `a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6`.

Full license notice:

```text

The MIT License

Copyright (c) 2018 Red Canary, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

### atuin — MIT

Atuin, Inc. (2026). [Applicable license](https://raw.githubusercontent.com/atuinsh/atuin/28fcb3db32e5550543fc7ed93537963e246abf7c/LICENSE); [scope](https://raw.githubusercontent.com/atuinsh/atuin/28fcb3db32e5550543fc7ed93537963e246abf7c/LICENSE).
- [README.md](https://raw.githubusercontent.com/atuinsh/atuin/28fcb3db32e5550543fc7ed93537963e246abf7c/README.md), ref `28fcb3db32e5550543fc7ed93537963e246abf7c`.
- [docs/docs/guide/delete-history.md](https://raw.githubusercontent.com/atuinsh/atuin/28fcb3db32e5550543fc7ed93537963e246abf7c/docs/docs/guide/delete-history.md), ref `28fcb3db32e5550543fc7ed93537963e246abf7c`.
- [docs/docs/reference/search.md](https://raw.githubusercontent.com/atuinsh/atuin/28fcb3db32e5550543fc7ed93537963e246abf7c/docs/docs/reference/search.md), ref `28fcb3db32e5550543fc7ed93537963e246abf7c`.
- [docs/docs/reference/stats.md](https://raw.githubusercontent.com/atuinsh/atuin/28fcb3db32e5550543fc7ed93537963e246abf7c/docs/docs/reference/stats.md), ref `28fcb3db32e5550543fc7ed93537963e246abf7c`.

Full license notice:

```text
MIT License

Copyright (c) 2026 Atuin, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### bashmirror — GPL-3.0-or-later

Free Software Foundation and Bash contributors. [Applicable license](https://raw.githubusercontent.com/gitGNU/gnu_bash/bc007799f0e1362100375bb95d952d28de4c62fb/COPYING); [scope](https://raw.githubusercontent.com/gitGNU/gnu_bash/bc007799f0e1362100375bb95d952d28de4c62fb/COPYING).
- [tests/history.tests](https://raw.githubusercontent.com/gitGNU/gnu_bash/bc007799f0e1362100375bb95d952d28de4c62fb/tests/history.tests), ref `bc007799f0e1362100375bb95d952d28de4c62fb`.

GNU Bash regression-test source excerpts, under GPL v3 or later; the separately licensed Bash manual is not distributed. Literal source form and modification/extraction records accompany every excerpt.

Full license notice:

```text
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<http://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<http://www.gnu.org/philosophy/why-not-lgpl.html>.
```

### cheat — CC0-1.0

cheat/cheatsheets community contributors. [Applicable license](https://raw.githubusercontent.com/cheat/cheatsheets/36bdb99dcfadde210503d8c2dcf94b34ee950e1d/.github/LICENSE.txt); [scope](https://raw.githubusercontent.com/cheat/cheatsheets/36bdb99dcfadde210503d8c2dcf94b34ee950e1d/.github/README.md).
- [history](https://raw.githubusercontent.com/cheat/cheatsheets/36bdb99dcfadde210503d8c2dcf94b34ee950e1d/history), ref `36bdb99dcfadde210503d8c2dcf94b34ee950e1d`.
- [journalctl](https://raw.githubusercontent.com/cheat/cheatsheets/36bdb99dcfadde210503d8c2dcf94b34ee950e1d/journalctl), ref `36bdb99dcfadde210503d8c2dcf94b34ee950e1d`.

The pinned project README explicitly dedicates the cheatsheets to CC0; this scope statement is retained in research evidence.

Full license notice:

```text
Creative Commons Legal Code

CC0 1.0 Universal

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
    PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
    THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
    HEREUNDER.

Statement of Purpose

The laws of most jurisdictions throughout the world automatically confer
exclusive Copyright and Related Rights (defined below) upon the creator
and subsequent owner(s) (each and all, an "owner") of an original work of
authorship and/or a database (each, a "Work").

Certain owners wish to permanently relinquish those rights to a Work for
the purpose of contributing to a commons of creative, cultural and
scientific works ("Commons") that the public can reliably and without fear
of later claims of infringement build upon, modify, incorporate in other
works, reuse and redistribute as freely as possible in any form whatsoever
and for any purposes, including without limitation commercial purposes.
These owners may contribute to the Commons to promote the ideal of a free
culture and the further production of creative, cultural and scientific
works, or to gain reputation or greater distribution for their Work in
part through the use and efforts of others.

For these and/or other purposes and motivations, and without any
expectation of additional consideration or compensation, the person
associating CC0 with a Work (the "Affirmer"), to the extent that he or she
is an owner of Copyright and Related Rights in the Work, voluntarily
elects to apply CC0 to the Work and publicly distribute the Work under its
terms, with knowledge of his or her Copyright and Related Rights in the
Work and the meaning and intended legal effect of CC0 on those rights.

1. Copyright and Related Rights. A Work made available under CC0 may be
protected by copyright and related or neighboring rights ("Copyright and
Related Rights"). Copyright and Related Rights include, but are not
limited to, the following:

  i. the right to reproduce, adapt, distribute, perform, display,
     communicate, and translate a Work;
 ii. moral rights retained by the original author(s) and/or performer(s);
iii. publicity and privacy rights pertaining to a person's image or
     likeness depicted in a Work;
 iv. rights protecting against unfair competition in regards to a Work,
     subject to the limitations in paragraph 4(a), below;
  v. rights protecting the extraction, dissemination, use and reuse of data
     in a Work;
 vi. database rights (such as those arising under Directive 96/9/EC of the
     European Parliament and of the Council of 11 March 1996 on the legal
     protection of databases, and under any national implementation
     thereof, including any amended or successor version of such
     directive); and
vii. other similar, equivalent or corresponding rights throughout the
     world based on applicable law or treaty, and any national
     implementations thereof.

2. Waiver. To the greatest extent permitted by, but not in contravention
of, applicable law, Affirmer hereby overtly, fully, permanently,
irrevocably and unconditionally waives, abandons, and surrenders all of
Affirmer's Copyright and Related Rights and associated claims and causes
of action, whether now known or unknown (including existing as well as
future claims and causes of action), in the Work (i) in all territories
worldwide, (ii) for the maximum duration provided by applicable law or
treaty (including future time extensions), (iii) in any current or future
medium and for any number of copies, and (iv) for any purpose whatsoever,
including without limitation commercial, advertising or promotional
purposes (the "Waiver"). Affirmer makes the Waiver for the benefit of each
member of the public at large and to the detriment of Affirmer's heirs and
successors, fully intending that such Waiver shall not be subject to
revocation, rescission, cancellation, termination, or any other legal or
equitable action to disrupt the quiet enjoyment of the Work by the public
as contemplated by Affirmer's express Statement of Purpose.

3. Public License Fallback. Should any part of the Waiver for any reason
be judged legally invalid or ineffective under applicable law, then the
Waiver shall be preserved to the maximum extent permitted taking into
account Affirmer's express Statement of Purpose. In addition, to the
extent the Waiver is so judged Affirmer hereby grants to each affected
person a royalty-free, non transferable, non sublicensable, non exclusive,
irrevocable and unconditional license to exercise Affirmer's Copyright and
Related Rights in the Work (i) in all territories worldwide, (ii) for the
maximum duration provided by applicable law or treaty (including future
time extensions), (iii) in any current or future medium and for any number
of copies, and (iv) for any purpose whatsoever, including without
limitation commercial, advertising or promotional purposes (the
"License"). The License shall be deemed effective as of the date CC0 was
applied by Affirmer to the Work. Should any part of the License for any
reason be judged legally invalid or ineffective under applicable law, such
partial invalidity or ineffectiveness shall not invalidate the remainder
of the License, and in such case Affirmer hereby affirms that he or she
will not (i) exercise any of his or her remaining Copyright and Related
Rights in the Work or (ii) assert any associated claims and causes of
action with respect to the Work, in either case contrary to Affirmer's
express Statement of Purpose.

4. Limitations and Disclaimers.

 a. No trademark or patent rights held by Affirmer are waived, abandoned,
    surrendered, licensed or otherwise affected by this document.
 b. Affirmer offers the Work as-is and makes no representations or
    warranties of any kind concerning the Work, express, implied,
    statutory or otherwise, including without limitation warranties of
    title, merchantability, fitness for a particular purpose, non
    infringement, or the absence of latent or other defects, accuracy, or
    the present or absence of errors, whether or not discoverable, all to
    the greatest extent permissible under applicable law.
 c. Affirmer disclaims responsibility for clearing rights of other persons
    that may apply to the Work or any use thereof, including without
    limitation any person's Copyright and Related Rights in the Work.
    Further, Affirmer disclaims responsibility for obtaining any necessary
    consents, permissions or other rights required for any use of the
    Work.
 d. Affirmer understands and acknowledges that Creative Commons is not a
    party to this document and has no duty or obligation with respect to
    this CC0 or use of the Work.
```

### hermes — MIT

Nous Research (2025). [Applicable license](https://raw.githubusercontent.com/NousResearch/hermes-agent/a09d0bc06543982c93c62d97a2ab5338db9f7f03/LICENSE); [scope](https://raw.githubusercontent.com/NousResearch/hermes-agent/a09d0bc06543982c93c62d97a2ab5338db9f7f03/LICENSE).
- [tests/tools/test_approval.py](https://raw.githubusercontent.com/NousResearch/hermes-agent/a09d0bc06543982c93c62d97a2ab5338db9f7f03/tests/tools/test_approval.py), ref `a09d0bc06543982c93c62d97a2ab5338db9f7f03`.

Full license notice:

```text
MIT License

Copyright (c) 2025 Nous Research

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### nah — MIT

Manuel Schipper (2026). [Applicable license](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/LICENSE); [scope](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/LICENSE).
- [corpus/filesystem.jsonl](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/corpus/filesystem.jsonl), ref `7230be14c0586c8ebe9a6be0c4d9a43f4949216a`.
- [corpus/native.jsonl](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/corpus/native.jsonl), ref `7230be14c0586c8ebe9a6be0c4d9a43f4949216a`.

Full license notice:

```text
MIT License

Copyright (c) 2026 Manuel Schipper

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### systemd — LGPL-2.1-or-later

systemd contributors; per-file SPDX notice retained. [Applicable license](https://raw.githubusercontent.com/systemd/systemd/ca78951bd398e191ebc4550710e33ef34190514e/LICENSE.LGPL2.1); [scope](https://raw.githubusercontent.com/systemd/systemd/ca78951bd398e191ebc4550710e33ef34190514e/LICENSE.LGPL2.1).
- [man/journalctl.xml](https://raw.githubusercontent.com/systemd/systemd/ca78951bd398e191ebc4550710e33ef34190514e/man/journalctl.xml), ref `ca78951bd398e191ebc4550710e33ef34190514e`.
- [test/units/TEST-04-JOURNAL.LogFilterPatterns.sh](https://raw.githubusercontent.com/systemd/systemd/ca78951bd398e191ebc4550710e33ef34190514e/test/units/TEST-04-JOURNAL.LogFilterPatterns.sh), ref `ca78951bd398e191ebc4550710e33ef34190514e`.
- [test/units/TEST-04-JOURNAL.bsod.sh](https://raw.githubusercontent.com/systemd/systemd/ca78951bd398e191ebc4550710e33ef34190514e/test/units/TEST-04-JOURNAL.bsod.sh), ref `ca78951bd398e191ebc4550710e33ef34190514e`.
- [test/units/TEST-04-JOURNAL.cat.sh](https://raw.githubusercontent.com/systemd/systemd/ca78951bd398e191ebc4550710e33ef34190514e/test/units/TEST-04-JOURNAL.cat.sh), ref `ca78951bd398e191ebc4550710e33ef34190514e`.
- [test/units/TEST-04-JOURNAL.fss.sh](https://raw.githubusercontent.com/systemd/systemd/ca78951bd398e191ebc4550710e33ef34190514e/test/units/TEST-04-JOURNAL.fss.sh), ref `ca78951bd398e191ebc4550710e33ef34190514e`.
- [test/units/TEST-04-JOURNAL.journal-corrupt.sh](https://raw.githubusercontent.com/systemd/systemd/ca78951bd398e191ebc4550710e33ef34190514e/test/units/TEST-04-JOURNAL.journal-corrupt.sh), ref `ca78951bd398e191ebc4550710e33ef34190514e`.
- [test/units/TEST-04-JOURNAL.journal.sh](https://raw.githubusercontent.com/systemd/systemd/ca78951bd398e191ebc4550710e33ef34190514e/test/units/TEST-04-JOURNAL.journal.sh), ref `ca78951bd398e191ebc4550710e33ef34190514e`.

Selected sources explicitly state `SPDX-License-Identifier: LGPL-2.1-or-later`. The extracted source form is retained in sources.csv; changes are recorded there.

Full license notice:

```text
                  GNU LESSER GENERAL PUBLIC LICENSE
                       Version 2.1, February 1999

 Copyright (C) 1991, 1999 Free Software Foundation, Inc.
 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

[This is the first released version of the Lesser GPL.  It also counts
 as the successor of the GNU Library Public License, version 2, hence
 the version number 2.1.]

                            Preamble

  The licenses for most software are designed to take away your
freedom to share and change it.  By contrast, the GNU General Public
Licenses are intended to guarantee your freedom to share and change
free software--to make sure the software is free for all its users.

  This license, the Lesser General Public License, applies to some
specially designated software packages--typically libraries--of the
Free Software Foundation and other authors who decide to use it.  You
can use it too, but we suggest you first think carefully about whether
this license or the ordinary General Public License is the better
strategy to use in any particular case, based on the explanations below.

  When we speak of free software, we are referring to freedom of use,
not price.  Our General Public Licenses are designed to make sure that
you have the freedom to distribute copies of free software (and charge
for this service if you wish); that you receive source code or can get
it if you want it; that you can change the software and use pieces of
it in new free programs; and that you are informed that you can do
these things.

  To protect your rights, we need to make restrictions that forbid
distributors to deny you these rights or to ask you to surrender these
rights.  These restrictions translate to certain responsibilities for
you if you distribute copies of the library or if you modify it.

  For example, if you distribute copies of the library, whether gratis
or for a fee, you must give the recipients all the rights that we gave
you.  You must make sure that they, too, receive or can get the source
code.  If you link other code with the library, you must provide
complete object files to the recipients, so that they can relink them
with the library after making changes to the library and recompiling
it.  And you must show them these terms so they know their rights.

  We protect your rights with a two-step method: (1) we copyright the
library, and (2) we offer you this license, which gives you legal
permission to copy, distribute and/or modify the library.

  To protect each distributor, we want to make it very clear that
there is no warranty for the free library.  Also, if the library is
modified by someone else and passed on, the recipients should know
that what they have is not the original version, so that the original
author's reputation will not be affected by problems that might be
introduced by others.

  Finally, software patents pose a constant threat to the existence of
any free program.  We wish to make sure that a company cannot
effectively restrict the users of a free program by obtaining a
restrictive license from a patent holder.  Therefore, we insist that
any patent license obtained for a version of the library must be
consistent with the full freedom of use specified in this license.

  Most GNU software, including some libraries, is covered by the
ordinary GNU General Public License.  This license, the GNU Lesser
General Public License, applies to certain designated libraries, and
is quite different from the ordinary General Public License.  We use
this license for certain libraries in order to permit linking those
libraries into non-free programs.

  When a program is linked with a library, whether statically or using
a shared library, the combination of the two is legally speaking a
combined work, a derivative of the original library.  The ordinary
General Public License therefore permits such linking only if the
entire combination fits its criteria of freedom.  The Lesser General
Public License permits more lax criteria for linking other code with
the library.

  We call this license the "Lesser" General Public License because it
does Less to protect the user's freedom than the ordinary General
Public License.  It also provides other free software developers Less
of an advantage over competing non-free programs.  These disadvantages
are the reason we use the ordinary General Public License for many
libraries.  However, the Lesser license provides advantages in certain
special circumstances.

  For example, on rare occasions, there may be a special need to
encourage the widest possible use of a certain library, so that it becomes
a de-facto standard.  To achieve this, non-free programs must be
allowed to use the library.  A more frequent case is that a free
library does the same job as widely used non-free libraries.  In this
case, there is little to gain by limiting the free library to free
software only, so we use the Lesser General Public License.

  In other cases, permission to use a particular library in non-free
programs enables a greater number of people to use a large body of
free software.  For example, permission to use the GNU C Library in
non-free programs enables many more people to use the whole GNU
operating system, as well as its variant, the GNU/Linux operating
system.

  Although the Lesser General Public License is Less protective of the
users' freedom, it does ensure that the user of a program that is
linked with the Library has the freedom and the wherewithal to run
that program using a modified version of the Library.

  The precise terms and conditions for copying, distribution and
modification follow.  Pay close attention to the difference between a
"work based on the library" and a "work that uses the library".  The
former contains code derived from the library, whereas the latter must
be combined with the library in order to run.

                  GNU LESSER GENERAL PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. This License Agreement applies to any software library or other
program which contains a notice placed by the copyright holder or
other authorized party saying it may be distributed under the terms of
this Lesser General Public License (also called "this License").
Each licensee is addressed as "you".

  A "library" means a collection of software functions and/or data
prepared so as to be conveniently linked with application programs
(which use some of those functions and data) to form executables.

  The "Library", below, refers to any such software library or work
which has been distributed under these terms.  A "work based on the
Library" means either the Library or any derivative work under
copyright law: that is to say, a work containing the Library or a
portion of it, either verbatim or with modifications and/or translated
straightforwardly into another language.  (Hereinafter, translation is
included without limitation in the term "modification".)

  "Source code" for a work means the preferred form of the work for
making modifications to it.  For a library, complete source code means
all the source code for all modules it contains, plus any associated
interface definition files, plus the scripts used to control compilation
and installation of the library.

  Activities other than copying, distribution and modification are not
covered by this License; they are outside its scope.  The act of
running a program using the Library is not restricted, and output from
such a program is covered only if its contents constitute a work based
on the Library (independent of the use of the Library in a tool for
writing it).  Whether that is true depends on what the Library does
and what the program that uses the Library does.

  1. You may copy and distribute verbatim copies of the Library's
complete source code as you receive it, in any medium, provided that
you conspicuously and appropriately publish on each copy an
appropriate copyright notice and disclaimer of warranty; keep intact
all the notices that refer to this License and to the absence of any
warranty; and distribute a copy of this License along with the
Library.

  You may charge a fee for the physical act of transferring a copy,
and you may at your option offer warranty protection in exchange for a
fee.

  2. You may modify your copy or copies of the Library or any portion
of it, thus forming a work based on the Library, and copy and
distribute such modifications or work under the terms of Section 1
above, provided that you also meet all of these conditions:

    a) The modified work must itself be a software library.

    b) You must cause the files modified to carry prominent notices
    stating that you changed the files and the date of any change.

    c) You must cause the whole of the work to be licensed at no
    charge to all third parties under the terms of this License.

    d) If a facility in the modified Library refers to a function or a
    table of data to be supplied by an application program that uses
    the facility, other than as an argument passed when the facility
    is invoked, then you must make a good faith effort to ensure that,
    in the event an application does not supply such function or
    table, the facility still operates, and performs whatever part of
    its purpose remains meaningful.

    (For example, a function in a library to compute square roots has
    a purpose that is entirely well-defined independent of the
    application.  Therefore, Subsection 2d requires that any
    application-supplied function or table used by this function must
    be optional: if the application does not supply it, the square
    root function must still compute square roots.)

These requirements apply to the modified work as a whole.  If
identifiable sections of that work are not derived from the Library,
and can be reasonably considered independent and separate works in
themselves, then this License, and its terms, do not apply to those
sections when you distribute them as separate works.  But when you
distribute the same sections as part of a whole which is a work based
on the Library, the distribution of the whole must be on the terms of
this License, whose permissions for other licensees extend to the
entire whole, and thus to each and every part regardless of who wrote
it.

Thus, it is not the intent of this section to claim rights or contest
your rights to work written entirely by you; rather, the intent is to
exercise the right to control the distribution of derivative or
collective works based on the Library.

In addition, mere aggregation of another work not based on the Library
with the Library (or with a work based on the Library) on a volume of
a storage or distribution medium does not bring the other work under
the scope of this License.

  3. You may opt to apply the terms of the ordinary GNU General Public
License instead of this License to a given copy of the Library.  To do
this, you must alter all the notices that refer to this License, so
that they refer to the ordinary GNU General Public License, version 2,
instead of to this License.  (If a newer version than version 2 of the
ordinary GNU General Public License has appeared, then you can specify
that version instead if you wish.)  Do not make any other change in
these notices.

  Once this change is made in a given copy, it is irreversible for
that copy, so the ordinary GNU General Public License applies to all
subsequent copies and derivative works made from that copy.

  This option is useful when you wish to copy part of the code of
the Library into a program that is not a library.

  4. You may copy and distribute the Library (or a portion or
derivative of it, under Section 2) in object code or executable form
under the terms of Sections 1 and 2 above provided that you accompany
it with the complete corresponding machine-readable source code, which
must be distributed under the terms of Sections 1 and 2 above on a
medium customarily used for software interchange.

  If distribution of object code is made by offering access to copy
from a designated place, then offering equivalent access to copy the
source code from the same place satisfies the requirement to
distribute the source code, even though third parties are not
compelled to copy the source along with the object code.

  5. A program that contains no derivative of any portion of the
Library, but is designed to work with the Library by being compiled or
linked with it, is called a "work that uses the Library".  Such a
work, in isolation, is not a derivative work of the Library, and
therefore falls outside the scope of this License.

  However, linking a "work that uses the Library" with the Library
creates an executable that is a derivative of the Library (because it
contains portions of the Library), rather than a "work that uses the
library".  The executable is therefore covered by this License.
Section 6 states terms for distribution of such executables.

  When a "work that uses the Library" uses material from a header file
that is part of the Library, the object code for the work may be a
derivative work of the Library even though the source code is not.
Whether this is true is especially significant if the work can be
linked without the Library, or if the work is itself a library.  The
threshold for this to be true is not precisely defined by law.

  If such an object file uses only numerical parameters, data
structure layouts and accessors, and small macros and small inline
functions (ten lines or less in length), then the use of the object
file is unrestricted, regardless of whether it is legally a derivative
work.  (Executables containing this object code plus portions of the
Library will still fall under Section 6.)

  Otherwise, if the work is a derivative of the Library, you may
distribute the object code for the work under the terms of Section 6.
Any executables containing that work also fall under Section 6,
whether or not they are linked directly with the Library itself.

  6. As an exception to the Sections above, you may also combine or
link a "work that uses the Library" with the Library to produce a
work containing portions of the Library, and distribute that work
under terms of your choice, provided that the terms permit
modification of the work for the customer's own use and reverse
engineering for debugging such modifications.

  You must give prominent notice with each copy of the work that the
Library is used in it and that the Library and its use are covered by
this License.  You must supply a copy of this License.  If the work
during execution displays copyright notices, you must include the
copyright notice for the Library among them, as well as a reference
directing the user to the copy of this License.  Also, you must do one
of these things:

    a) Accompany the work with the complete corresponding
    machine-readable source code for the Library including whatever
    changes were used in the work (which must be distributed under
    Sections 1 and 2 above); and, if the work is an executable linked
    with the Library, with the complete machine-readable "work that
    uses the Library", as object code and/or source code, so that the
    user can modify the Library and then relink to produce a modified
    executable containing the modified Library.  (It is understood
    that the user who changes the contents of definitions files in the
    Library will not necessarily be able to recompile the application
    to use the modified definitions.)

    b) Use a suitable shared library mechanism for linking with the
    Library.  A suitable mechanism is one that (1) uses at run time a
    copy of the library already present on the user's computer system,
    rather than copying library functions into the executable, and (2)
    will operate properly with a modified version of the library, if
    the user installs one, as long as the modified version is
    interface-compatible with the version that the work was made with.

    c) Accompany the work with a written offer, valid for at
    least three years, to give the same user the materials
    specified in Subsection 6a, above, for a charge no more
    than the cost of performing this distribution.

    d) If distribution of the work is made by offering access to copy
    from a designated place, offer equivalent access to copy the above
    specified materials from the same place.

    e) Verify that the user has already received a copy of these
    materials or that you have already sent this user a copy.

  For an executable, the required form of the "work that uses the
Library" must include any data and utility programs needed for
reproducing the executable from it.  However, as a special exception,
the materials to be distributed need not include anything that is
normally distributed (in either source or binary form) with the major
components (compiler, kernel, and so on) of the operating system on
which the executable runs, unless that component itself accompanies
the executable.

  It may happen that this requirement contradicts the license
restrictions of other proprietary libraries that do not normally
accompany the operating system.  Such a contradiction means you cannot
use both them and the Library together in an executable that you
distribute.

  7. You may place library facilities that are a work based on the
Library side-by-side in a single library together with other library
facilities not covered by this License, and distribute such a combined
library, provided that the separate distribution of the work based on
the Library and of the other library facilities is otherwise
permitted, and provided that you do these two things:

    a) Accompany the combined library with a copy of the same work
    based on the Library, uncombined with any other library
    facilities.  This must be distributed under the terms of the
    Sections above.

    b) Give prominent notice with the combined library of the fact
    that part of it is a work based on the Library, and explaining
    where to find the accompanying uncombined form of the same work.

  8. You may not copy, modify, sublicense, link with, or distribute
the Library except as expressly provided under this License.  Any
attempt otherwise to copy, modify, sublicense, link with, or
distribute the Library is void, and will automatically terminate your
rights under this License.  However, parties who have received copies,
or rights, from you under this License will not have their licenses
terminated so long as such parties remain in full compliance.

  9. You are not required to accept this License, since you have not
signed it.  However, nothing else grants you permission to modify or
distribute the Library or its derivative works.  These actions are
prohibited by law if you do not accept this License.  Therefore, by
modifying or distributing the Library (or any work based on the
Library), you indicate your acceptance of this License to do so, and
all its terms and conditions for copying, distributing or modifying
the Library or works based on it.

  10. Each time you redistribute the Library (or any work based on the
Library), the recipient automatically receives a license from the
original licensor to copy, distribute, link with or modify the Library
subject to these terms and conditions.  You may not impose any further
restrictions on the recipients' exercise of the rights granted herein.
You are not responsible for enforcing compliance by third parties with
this License.

  11. If, as a consequence of a court judgment or allegation of patent
infringement or for any other reason (not limited to patent issues),
conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot
distribute so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you
may not distribute the Library at all.  For example, if a patent
license would not permit royalty-free redistribution of the Library by
all those who receive copies directly or indirectly through you, then
the only way you could satisfy both it and this License would be to
refrain entirely from distribution of the Library.

If any portion of this section is held invalid or unenforceable under any
particular circumstance, the balance of the section is intended to apply,
and the section as a whole is intended to apply in other circumstances.

It is not the purpose of this section to induce you to infringe any
patents or other property right claims or to contest validity of any
such claims; this section has the sole purpose of protecting the
integrity of the free software distribution system which is
implemented by public license practices.  Many people have made
generous contributions to the wide range of software distributed
through that system in reliance on consistent application of that
system; it is up to the author/donor to decide if he or she is willing
to distribute software through any other system and a licensee cannot
impose that choice.

This section is intended to make thoroughly clear what is believed to
be a consequence of the rest of this License.

  12. If the distribution and/or use of the Library is restricted in
certain countries either by patents or by copyrighted interfaces, the
original copyright holder who places the Library under this License may add
an explicit geographical distribution limitation excluding those countries,
so that distribution is permitted only in or among countries not thus
excluded.  In such case, this License incorporates the limitation as if
written in the body of this License.

  13. The Free Software Foundation may publish revised and/or new
versions of the Lesser General Public License from time to time.
Such new versions will be similar in spirit to the present version,
but may differ in detail to address new problems or concerns.

Each version is given a distinguishing version number.  If the Library
specifies a version number of this License which applies to it and
"any later version", you have the option of following the terms and
conditions either of that version or of any later version published by
the Free Software Foundation.  If the Library does not specify a
license version number, you may choose any version ever published by
the Free Software Foundation.

  14. If you wish to incorporate parts of the Library into other free
programs whose distribution conditions are incompatible with these,
write to the author to ask for permission.  For software which is
copyrighted by the Free Software Foundation, write to the Free
Software Foundation; we sometimes make exceptions for this.  Our
decision will be guided by the two goals of preserving the free status
of all derivatives of our free software and of promoting the sharing
and reuse of software generally.

                            NO WARRANTY

  15. BECAUSE THE LIBRARY IS LICENSED FREE OF CHARGE, THERE IS NO
WARRANTY FOR THE LIBRARY, TO THE EXTENT PERMITTED BY APPLICABLE LAW.
EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR
OTHER PARTIES PROVIDE THE LIBRARY "AS IS" WITHOUT WARRANTY OF ANY
KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE
LIBRARY IS WITH YOU.  SHOULD THE LIBRARY PROVE DEFECTIVE, YOU ASSUME
THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN
WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY
AND/OR REDISTRIBUTE THE LIBRARY AS PERMITTED ABOVE, BE LIABLE TO YOU
FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR
CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE
LIBRARY (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING
RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A
FAILURE OF THE LIBRARY TO OPERATE WITH ANY OTHER SOFTWARE), EVEN IF
SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGES.

                     END OF TERMS AND CONDITIONS

           How to Apply These Terms to Your New Libraries

  If you develop a new library, and you want it to be of the greatest
possible use to the public, we recommend making it free software that
everyone can redistribute and change.  You can do so by permitting
redistribution under these terms (or, alternatively, under the terms of the
ordinary General Public License).

  To apply these terms, attach the following notices to the library.  It is
safest to attach them to the start of each source file to most effectively
convey the exclusion of warranty; and each file should have at least the
"copyright" line and a pointer to where the full notice is found.

    <one line to give the library's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA

Also add information on how to contact you by electronic and paper mail.

You should also get your employer (if you work as a programmer) or your
school, if any, to sign a "copyright disclaimer" for the library, if
necessary.  Here is a sample; alter the names:

  Yoyodyne, Inc., hereby disclaims all copyright interest in the
  library `Frob' (a library for tweaking knobs) written by James Random Hacker.

  <signature of Ty Coon>, 1 April 1990
  Ty Coon, President of Vice

That's all there is to it!
```

### testguard — Apache-2.0

anthony-bible/code-agent-demo contributors. [Applicable license](https://raw.githubusercontent.com/anthony-bible/code-agent-demo/6b043ba3b2e2539924d824acbaa950da76122c55/LICENSE); [scope](https://raw.githubusercontent.com/anthony-bible/code-agent-demo/6b043ba3b2e2539924d824acbaa950da76122c55/LICENSE).
- [internal/domain/safety/command_whitelist_test.go](https://raw.githubusercontent.com/anthony-bible/code-agent-demo/6b043ba3b2e2539924d824acbaa950da76122c55/internal/domain/safety/command_whitelist_test.go), ref `6b043ba3b2e2539924d824acbaa950da76122c55`.

Full license notice:

```text

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright 2026 Anthony Bible

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

### tldr — CC-BY-4.0

tldr-pages team and contributors (2014–present). [Applicable license](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/LICENSE.md); [scope](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/LICENSE.md).
- [pages/common/fc.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/fc.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/common/history.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/history.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/common/rm.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/rm.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/common/shred.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/shred.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/common/tee.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/tee.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/common/truncate.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/truncate.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/common/unlink.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/unlink.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/auditctl.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/auditctl.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/aureport.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/aureport.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/ausearch.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/ausearch.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/dmesg.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/dmesg.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/journalctl.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/journalctl.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/last.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/last.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/lastb.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/lastb.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/lastlog.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/lastlog.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/logread.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/logread.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/utmpdump.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/utmpdump.md), ref `ed1f496b347fa32446122aa56e254431e2b50fa0`.

Selected command pages are documentation under CC BY 4.0. The scripts-only MIT exception does not apply to them.

Full license notice:

```text
<!-- markdownlint-disable MD041 -->
Copyright © 2014—present the [tldr-pages team](https://github.com/orgs/tldr-pages/people)
and [contributors](https://github.com/tldr-pages/tldr/graphs/contributors).

**This work is licensed under the
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)
(CC-BY).**

----

The contents of the [scripts/](https://github.com/tldr-pages/tldr/tree/main/scripts) directory
are licensed under the MIT license:

> **The MIT License**
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.
```

### xaidr — Apache-2.0

delphisecurity/xaidr contributors. [Applicable license](https://raw.githubusercontent.com/delphisecurity/xaidr/c2fd10d16932513ce56a31978d818c300b16d74d/LICENSE); [scope](https://raw.githubusercontent.com/delphisecurity/xaidr/c2fd10d16932513ce56a31978d818c300b16d74d/LICENSE).
- [tests/fixtures/shell_corpus.json](https://raw.githubusercontent.com/delphisecurity/xaidr/c2fd10d16932513ce56a31978d818c300b16d74d/tests/fixtures/shell_corpus.json), ref `c2fd10d16932513ce56a31978d818c300b16d74d`.

Full license notice:

```text

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright 2026 Delphi Security Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

Upstream NOTICE (dependencies mentioned here are not redistributed by this dataset):

```text
xaidr
Copyright 2026 Delphi Security Inc.

This product includes software developed at Delphi Security Inc.

This product includes data from the Public Suffix List
(https://publicsuffix.org/list/public_suffix_list.dat), vendored as
xaidr/value_origin/_psl_data.py. That file is subject to the terms of the
Mozilla Public License, v. 2.0. A copy of the MPL is available at
https://mozilla.org/MPL/2.0/.

This product includes data derived from the Unicode Character Database and
the Unicode IDNA Compatibility Processing tables (UTS #46), version 13.0.0,
vendored as xaidr/value_origin/_idna_data.py. Copyright (c) 1991-2020
Unicode, Inc. Distributed under the Unicode License Agreement - Data Files
and Software (https://www.unicode.org/license.txt).
```

### GNU GPL version 2

Included additionally for the LGPL 2.1 terms:

```text
                    GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991

 Copyright (C) 1989, 1991 Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The licenses for most software are designed to take away your
freedom to share and change it.  By contrast, the GNU General Public
License is intended to guarantee your freedom to share and change free
software--to make sure the software is free for all its users.  This
General Public License applies to most of the Free Software
Foundation's software and to any other program whose authors commit to
using it.  (Some other Free Software Foundation software is covered by
the GNU Lesser General Public License instead.)  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
this service if you wish), that you receive source code or can get it
if you want it, that you can change the software or use pieces of it
in new free programs; and that you know you can do these things.

  To protect your rights, we need to make restrictions that forbid
anyone to deny you these rights or to ask you to surrender the rights.
These restrictions translate to certain responsibilities for you if you
distribute copies of the software, or if you modify it.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must give the recipients all the rights that
you have.  You must make sure that they, too, receive or can get the
source code.  And you must show them these terms so they know their
rights.

  We protect your rights with two steps: (1) copyright the software, and
(2) offer you this license which gives you legal permission to copy,
distribute and/or modify the software.

  Also, for each author's protection and ours, we want to make certain
that everyone understands that there is no warranty for this free
software.  If the software is modified by someone else and passed on, we
want its recipients to know that what they have is not the original, so
that any problems introduced by others will not reflect on the original
authors' reputations.

  Finally, any free program is threatened constantly by software
patents.  We wish to avoid the danger that redistributors of a free
program will individually obtain patent licenses, in effect making the
program proprietary.  To prevent this, we have made it clear that any
patent must be licensed for everyone's free use or not licensed at all.

  The precise terms and conditions for copying, distribution and
modification follow.

                    GNU GENERAL PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. This License applies to any program or other work which contains
a notice placed by the copyright holder saying it may be distributed
under the terms of this General Public License.  The "Program", below,
refers to any such program or work, and a "work based on the Program"
means either the Program or any derivative work under copyright law:
that is to say, a work containing the Program or a portion of it,
either verbatim or with modifications and/or translated into another
language.  (Hereinafter, translation is included without limitation in
the term "modification".)  Each licensee is addressed as "you".

Activities other than copying, distribution and modification are not
covered by this License; they are outside its scope.  The act of
running the Program is not restricted, and the output from the Program
is covered only if its contents constitute a work based on the
Program (independent of having been made by running the Program).
Whether that is true depends on what the Program does.

  1. You may copy and distribute verbatim copies of the Program's
source code as you receive it, in any medium, provided that you
conspicuously and appropriately publish on each copy an appropriate
copyright notice and disclaimer of warranty; keep intact all the
notices that refer to this License and to the absence of any warranty;
and give any other recipients of the Program a copy of this License
along with the Program.

You may charge a fee for the physical act of transferring a copy, and
you may at your option offer warranty protection in exchange for a fee.

  2. You may modify your copy or copies of the Program or any portion
of it, thus forming a work based on the Program, and copy and
distribute such modifications or work under the terms of Section 1
above, provided that you also meet all of these conditions:

    a) You must cause the modified files to carry prominent notices
    stating that you changed the files and the date of any change.

    b) You must cause any work that you distribute or publish, that in
    whole or in part contains or is derived from the Program or any
    part thereof, to be licensed as a whole at no charge to all third
    parties under the terms of this License.

    c) If the modified program normally reads commands interactively
    when run, you must cause it, when started running for such
    interactive use in the most ordinary way, to print or display an
    announcement including an appropriate copyright notice and a
    notice that there is no warranty (or else, saying that you provide
    a warranty) and that users may redistribute the program under
    these conditions, and telling the user how to view a copy of this
    License.  (Exception: if the Program itself is interactive but
    does not normally print such an announcement, your work based on
    the Program is not required to print an announcement.)

These requirements apply to the modified work as a whole.  If
identifiable sections of that work are not derived from the Program,
and can be reasonably considered independent and separate works in
themselves, then this License, and its terms, do not apply to those
sections when you distribute them as separate works.  But when you
distribute the same sections as part of a whole which is a work based
on the Program, the distribution of the whole must be on the terms of
this License, whose permissions for other licensees extend to the
entire whole, and thus to each and every part regardless of who wrote it.

Thus, it is not the intent of this section to claim rights or contest
your rights to work written entirely by you; rather, the intent is to
exercise the right to control the distribution of derivative or
collective works based on the Program.

In addition, mere aggregation of another work not based on the Program
with the Program (or with a work based on the Program) on a volume of
a storage or distribution medium does not bring the other work under
the scope of this License.

  3. You may copy and distribute the Program (or a work based on it,
under Section 2) in object code or executable form under the terms of
Sections 1 and 2 above provided that you also do one of the following:

    a) Accompany it with the complete corresponding machine-readable
    source code, which must be distributed under the terms of Sections
    1 and 2 above on a medium customarily used for software interchange; or,

    b) Accompany it with a written offer, valid for at least three
    years, to give any third party, for a charge no more than your
    cost of physically performing source distribution, a complete
    machine-readable copy of the corresponding source code, to be
    distributed under the terms of Sections 1 and 2 above on a medium
    customarily used for software interchange; or,

    c) Accompany it with the information you received as to the offer
    to distribute corresponding source code.  (This alternative is
    allowed only for noncommercial distribution and only if you
    received the program in object code or executable form with such
    an offer, in accord with Subsection b above.)

The source code for a work means the preferred form of the work for
making modifications to it.  For an executable work, complete source
code means all the source code for all modules it contains, plus any
associated interface definition files, plus the scripts used to
control compilation and installation of the executable.  However, as a
special exception, the source code distributed need not include
anything that is normally distributed (in either source or binary
form) with the major components (compiler, kernel, and so on) of the
operating system on which the executable runs, unless that component
itself accompanies the executable.

If distribution of executable or object code is made by offering
access to copy from a designated place, then offering equivalent
access to copy the source code from the same place counts as
distribution of the source code, even though third parties are not
compelled to copy the source along with the object code.

  4. You may not copy, modify, sublicense, or distribute the Program
except as expressly provided under this License.  Any attempt
otherwise to copy, modify, sublicense or distribute the Program is
void, and will automatically terminate your rights under this License.
However, parties who have received copies, or rights, from you under
this License will not have their licenses terminated so long as such
parties remain in full compliance.

  5. You are not required to accept this License, since you have not
signed it.  However, nothing else grants you permission to modify or
distribute the Program or its derivative works.  These actions are
prohibited by law if you do not accept this License.  Therefore, by
modifying or distributing the Program (or any work based on the
Program), you indicate your acceptance of this License to do so, and
all its terms and conditions for copying, distributing or modifying
the Program or works based on it.

  6. Each time you redistribute the Program (or any work based on the
Program), the recipient automatically receives a license from the
original licensor to copy, distribute or modify the Program subject to
these terms and conditions.  You may not impose any further
restrictions on the recipients' exercise of the rights granted herein.
You are not responsible for enforcing compliance by third parties to
this License.

  7. If, as a consequence of a court judgment or allegation of patent
infringement or for any other reason (not limited to patent issues),
conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot
distribute so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you
may not distribute the Program at all.  For example, if a patent
license would not permit royalty-free redistribution of the Program by
all those who receive copies directly or indirectly through you, then
the only way you could satisfy both it and this License would be to
refrain entirely from distribution of the Program.

If any portion of this section is held invalid or unenforceable under
any particular circumstance, the balance of the section is intended to
apply and the section as a whole is intended to apply in other
circumstances.

It is not the purpose of this section to induce you to infringe any
patents or other property right claims or to contest validity of any
such claims; this section has the sole purpose of protecting the
integrity of the free software distribution system, which is
implemented by public license practices.  Many people have made
generous contributions to the wide range of software distributed
through that system in reliance on consistent application of that
system; it is up to the author/donor to decide if he or she is willing
to distribute software through any other system and a licensee cannot
impose that choice.

This section is intended to make thoroughly clear what is believed to
be a consequence of the rest of this License.

  8. If the distribution and/or use of the Program is restricted in
certain countries either by patents or by copyrighted interfaces, the
original copyright holder who places the Program under this License
may add an explicit geographical distribution limitation excluding
those countries, so that distribution is permitted only in or among
countries not thus excluded.  In such case, this License incorporates
the limitation as if written in the body of this License.

  9. The Free Software Foundation may publish revised and/or new versions
of the General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

Each version is given a distinguishing version number.  If the Program
specifies a version number of this License which applies to it and "any
later version", you have the option of following the terms and conditions
either of that version or of any later version published by the Free
Software Foundation.  If the Program does not specify a version number of
this License, you may choose any version ever published by the Free Software
Foundation.

  10. If you wish to incorporate parts of the Program into other free
programs whose distribution conditions are different, write to the author
to ask for permission.  For software which is copyrighted by the Free
Software Foundation, write to the Free Software Foundation; we sometimes
make exceptions for this.  Our decision will be guided by the two goals
of preserving the free status of all derivatives of our free software and
of promoting the sharing and reuse of software generally.

                            NO WARRANTY

  11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
REPAIR OR CORRECTION.

  12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED
TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY
YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER
PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGES.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
convey the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Also add information on how to contact you by electronic and paper mail.

If the program is interactive, make it output a short notice like this
when it starts in an interactive mode:

    Gnomovision version 69, Copyright (C) year name of author
    Gnomovision comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, the commands you use may
be called something other than `show w' and `show c'; they could even be
mouse-clicks or menu items--whatever suits your program.

You should also get your employer (if you work as a programmer) or your
school, if any, to sign a "copyright disclaimer" for the program, if
necessary.  Here is a sample; alter the names:

  Yoyodyne, Inc., hereby disclaims all copyright interest in the program
  `Gnomovision' (which makes passes at compilers) written by James Hacker.

  <signature of Ty Coon>, 1 April 1989
  Ty Coon, President of Vice

This General Public License does not permit incorporating your program into
proprietary programs.  If your program is a subroutine library, you may
consider it more useful to permit linking proprietary applications with the
library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.
```

### Community excerpts

Each linked post is the attributed work of the named author under the official API content_license for that specific post. A question and its answers can have different licenses. Extractions, any parameter rendering and other changes are recorded per row in sources.csv; adapted excerpts retain the same CC BY-SA version. Follow each license link for its complete terms.

| Post | Author | License | Records |
| --- | --- | --- | --- |
| [se-apple-430164](https://apple.stackexchange.com/a/430164) | [jksoegaard](https://apple.stackexchange.com/users/77912/jksoegaard) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R241, CAT-6.3-R242 |
| [se-askubuntu-1307774](https://askubuntu.com/a/1307774) | [eeezyy](https://askubuntu.com/users/308325/eeezyy) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R162 |
| [se-askubuntu-1308989](https://askubuntu.com/q/1308989) | [andyman](https://askubuntu.com/users/1087589/andyman) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R211 |
| [se-askubuntu-1349306](https://askubuntu.com/q/1349306) | [Going Bananas](https://askubuntu.com/users/581662/going-bananas) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R069 |
| [se-askubuntu-1456580](https://askubuntu.com/q/1456580) | [oooYooo](https://askubuntu.com/users/1675733/oooyooo) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R009 |
| [se-askubuntu-1491766](https://askubuntu.com/a/1491766) | [aditya sadawarte](https://askubuntu.com/users/1743916/aditya-sadawarte) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R212 |
| [se-askubuntu-1504263](https://askubuntu.com/q/1504263) | [Adrian](https://askubuntu.com/users/469028/adrian) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R144 |
| [se-askubuntu-1531483](https://askubuntu.com/a/1531483) | [Chester Gillon](https://askubuntu.com/users/1660836/chester-gillon) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R173 |
| [se-askubuntu-1545856](https://askubuntu.com/q/1545856) | [AlanQ](https://askubuntu.com/users/592679/alanq) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R186 |
| [se-askubuntu-1550952](https://askubuntu.com/a/1550952) | [guettli](https://askubuntu.com/users/42348/guettli) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R020 |
| [se-askubuntu-1562934](https://askubuntu.com/a/1562934) | [Maciej Gorny](https://askubuntu.com/users/2414966/maciej-gorny) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R190 |
| [se-askubuntu-1563179](https://askubuntu.com/q/1563179) | [Matteo Carotta](https://askubuntu.com/users/769670/matteo-carotta) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R181 |
| [se-askubuntu-1568980](https://askubuntu.com/a/1568980) | [Travis Britz](https://askubuntu.com/users/937447/travis-britz) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R191 |
| [se-askubuntu-406681](https://askubuntu.com/a/406681) | [eggonlegs](https://askubuntu.com/users/36685/eggonlegs) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R172 |
| [se-askubuntu-524249](https://askubuntu.com/a/524249) | [g_p](https://askubuntu.com/users/146791/g-p) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R049 |
| [se-askubuntu-536225](https://askubuntu.com/a/536225) | [zorbon.cz](https://askubuntu.com/users/35669/zorbon-cz) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R202 |
| [se-askubuntu-605270](https://askubuntu.com/q/605270) | [homeServ](https://askubuntu.com/users/394388/homeserv) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R106 |
| [se-askubuntu-633409](https://askubuntu.com/a/633409) | [Sergiy Kolodyazhnyy](https://askubuntu.com/users/295286/sergiy-kolodyazhnyy) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R205 |
| [se-askubuntu-706130](https://askubuntu.com/a/706130) | [NZD](https://askubuntu.com/users/425630/nzd) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R245 |
| [se-askubuntu-903364](https://askubuntu.com/a/903364) | [Ravexina](https://askubuntu.com/users/264781/ravexina) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R203 |
| [se-askubuntu-91344](https://askubuntu.com/q/91344) | [Tom](https://askubuntu.com/users/32256/tom) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R182 |
| [se-askubuntu-952541](https://askubuntu.com/a/952541) | [dessert](https://askubuntu.com/users/507051/dessert) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R244 |
| [se-askubuntu-952724](https://askubuntu.com/a/952724) | [Div](https://askubuntu.com/users/732955/div) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R071 |
| [se-askubuntu-956314](https://askubuntu.com/a/956314) | [dessert](https://askubuntu.com/users/507051/dessert) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R200 |
| [se-stackoverflow-33444185](https://stackoverflow.com/a/33444185) | [AAM111](https://stackoverflow.com/users/5407797/aam111) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R040 |
| [se-stackoverflow-33444394](https://stackoverflow.com/a/33444394) | [Todd A. Jacobs](https://stackoverflow.com/users/1301972/todd-a-jacobs) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R153 |
| [se-stackoverflow-46076417](https://stackoverflow.com/q/46076417) | [Simpom](https://stackoverflow.com/users/3909303/simpom) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R165 |
| [se-stackoverflow-47890353](https://stackoverflow.com/q/47890353) | [Seth Holladay](https://stackoverflow.com/users/2990144/seth-holladay) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R152 |
| [se-stackoverflow-54225341](https://stackoverflow.com/q/54225341) | [ideasman42](https://stackoverflow.com/users/432509/ideasman42) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R156 |
| [se-stackoverflow-59151960](https://stackoverflow.com/a/59151960) | [dash-o](https://stackoverflow.com/users/12098405/dash-o) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R004 |
| [se-stackoverflow-65215163](https://stackoverflow.com/q/65215163) | [yunfei](https://stackoverflow.com/users/1153026/yunfei) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R185 |
| [se-stackoverflow-68755810](https://stackoverflow.com/q/68755810) | [tanatan](https://stackoverflow.com/users/15196604/tanatan) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R168, CAT-6.3-R177, CAT-6.3-R178 |
| [se-stackoverflow-68756091](https://stackoverflow.com/a/68756091) | [koyaanisqatsi](https://stackoverflow.com/users/11740758/koyaanisqatsi) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R161 |
| [se-stackoverflow-980283](https://stackoverflow.com/q/980283) | [Hobo](https://stackoverflow.com/users/1714/hobo) | [CC-BY-SA-2.5](https://creativecommons.org/licenses/by-sa/2.5/) | CAT-6.3-R179 |
| [se-unix-123539](https://unix.stackexchange.com/a/123539) | [devnull](https://unix.stackexchange.com/users/36502/devnull) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R036 |
| [se-unix-123544](https://unix.stackexchange.com/a/123544) | [cuonglm](https://unix.stackexchange.com/users/38906/cuonglm) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R204 |
| [se-unix-145456](https://unix.stackexchange.com/a/145456) | [terdon](https://unix.stackexchange.com/users/22222/terdon) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R170 |
| [se-unix-149127](https://unix.stackexchange.com/a/149127) | [Braiam](https://unix.stackexchange.com/users/41104/braiam) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R082 |
| [se-unix-150179](https://unix.stackexchange.com/a/150179) | [Stéphane Chazelas](https://unix.stackexchange.com/users/22565/st%c3%a9phane-chazelas) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R193 |
| [se-unix-178956](https://unix.stackexchange.com/a/178956) | [aliteralmind](https://unix.stackexchange.com/users/80154/aliteralmind) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R067 |
| [se-unix-184488](https://unix.stackexchange.com/q/184488) | [DiogoSaraiva](https://unix.stackexchange.com/users/99659/diogosaraiva) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R021, CAT-6.3-R022 |
| [se-unix-184492](https://unix.stackexchange.com/a/184492) | [aguslr](https://unix.stackexchange.com/users/102345/aguslr) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R064 |
| [se-unix-243828](https://unix.stackexchange.com/q/243828) | [Miroslav Franc](https://unix.stackexchange.com/users/27687/miroslav-franc) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R218 |
| [se-unix-272662](https://unix.stackexchange.com/q/272662) | [Tal](https://unix.stackexchange.com/users/91667/tal) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R061 |
| [se-unix-275101](https://unix.stackexchange.com/a/275101) | [user2982704](https://unix.stackexchange.com/users/164859/user2982704) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R085 |
| [se-unix-312528](https://unix.stackexchange.com/q/312528) | [Martin Vegter](https://unix.stackexchange.com/users/43007/martin-vegter) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R155 |
| [se-unix-314017](https://unix.stackexchange.com/q/314017) | [Vicky Dev](https://unix.stackexchange.com/users/128523/vicky-dev) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R249 |
| [se-unix-328153](https://unix.stackexchange.com/a/328153) | [Wissam Roujoulah](https://unix.stackexchange.com/users/200853/wissam-roujoulah) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R171 |
| [se-unix-330511](https://unix.stackexchange.com/a/330511) | [ANTHONY](https://unix.stackexchange.com/users/205588/anthony) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R039 |
| [se-unix-350640](https://unix.stackexchange.com/a/350640) | [Mathias Rav](https://unix.stackexchange.com/users/220010/mathias-rav) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R194, CAT-6.3-R195 |
| [se-unix-369425](https://unix.stackexchange.com/a/369425) | [LiveWireBT](https://unix.stackexchange.com/users/49853/livewirebt) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R019 |
| [se-unix-370682](https://unix.stackexchange.com/a/370682) | [Akira Cleber Nakandakare](https://unix.stackexchange.com/users/234293/akira-cleber-nakandakare) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R086 |
| [se-unix-386852](https://unix.stackexchange.com/q/386852) | [LoranceChen](https://unix.stackexchange.com/users/217155/lorancechen) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R166 |
| [se-unix-405550](https://unix.stackexchange.com/q/405550) | [scrapy](https://unix.stackexchange.com/users/243284/scrapy) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R167 |
| [se-unix-435719](https://unix.stackexchange.com/q/435719) | [sourcejedi](https://unix.stackexchange.com/users/29483/sourcejedi) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R176 |
| [se-unix-462266](https://unix.stackexchange.com/q/462266) | [humanityANDpeace](https://unix.stackexchange.com/users/24394/humanityandpeace) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R143 |
| [se-unix-467856](https://unix.stackexchange.com/a/467856) | [RalfFriedl](https://unix.stackexchange.com/users/301065/ralffriedl) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R047, CAT-6.3-R048 |
| [se-unix-496588](https://unix.stackexchange.com/q/496588) | [244boy](https://unix.stackexchange.com/users/239154/244boy) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R219 |
| [se-unix-503059](https://unix.stackexchange.com/q/503059) | [TheMeaningfulEngineer](https://unix.stackexchange.com/users/29436/themeaningfulengineer) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R164 |
| [se-unix-555971](https://unix.stackexchange.com/a/555971) | [Jeff Schaller](https://unix.stackexchange.com/users/117549/jeff-schaller) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R198 |
| [se-unix-573267](https://unix.stackexchange.com/a/573267) | user373503 | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R189 |
| [se-unix-604769](https://unix.stackexchange.com/q/604769) | [Chris](https://unix.stackexchange.com/users/266125/chris) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R154 |
| [se-unix-607279](https://unix.stackexchange.com/a/607279) | [Stephen Harris](https://unix.stackexchange.com/users/168757/stephen-harris) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R197 |
| [se-unix-616732](https://unix.stackexchange.com/a/616732) | [Rob W](https://unix.stackexchange.com/users/27177/rob-w) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R196 |
| [se-unix-62412](https://unix.stackexchange.com/q/62412) | [Claudio](https://unix.stackexchange.com/users/20102/claudio) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R221 |
| [se-unix-644305](https://unix.stackexchange.com/q/644305) | [daikabocha](https://unix.stackexchange.com/users/465653/daikabocha) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R183 |
| [se-unix-669707](https://unix.stackexchange.com/a/669707) | [serax](https://unix.stackexchange.com/users/480681/serax) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R054 |
| [se-unix-680906](https://unix.stackexchange.com/a/680906) | [FelixJN](https://unix.stackexchange.com/users/123460/felixjn) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R199 |
| [se-unix-690567](https://unix.stackexchange.com/q/690567) | [networkz](https://unix.stackexchange.com/users/514365/networkz) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R220 |
| [se-unix-715296](https://unix.stackexchange.com/a/715296) | [gabrielgbs97](https://unix.stackexchange.com/users/433364/gabrielgbs97) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R087 |
| [se-unix-718902](https://unix.stackexchange.com/q/718902) | [Erik](https://unix.stackexchange.com/users/81870/erik) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R184 |
| [se-unix-721538](https://unix.stackexchange.com/q/721538) | [Sunlight](https://unix.stackexchange.com/users/514288/sunlight) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R084 |
| [se-unix-721846](https://unix.stackexchange.com/a/721846) | [Arif Kara](https://unix.stackexchange.com/users/546067/arif-kara) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R192 |
| [se-unix-743063](https://unix.stackexchange.com/a/743063) | [duise](https://unix.stackexchange.com/users/568388/duise) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R201 |
| [se-unix-755616](https://unix.stackexchange.com/q/755616) | [likelyq](https://unix.stackexchange.com/users/584579/likelyq) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R169 |
| [se-unix-766558](https://unix.stackexchange.com/a/766558) | [jpaugh](https://unix.stackexchange.com/users/8503/jpaugh) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R111 |
| [se-unix-766875](https://unix.stackexchange.com/a/766875) | [Alex Martian](https://unix.stackexchange.com/users/266260/alex-martian) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R248 |
| [se-unix-774531](https://unix.stackexchange.com/q/774531) | [Radoslav Ivanov](https://unix.stackexchange.com/users/559539/radoslav-ivanov) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R163 |
| [se-unix-796754](https://unix.stackexchange.com/q/796754) | [Karol Król](https://unix.stackexchange.com/users/751119/karol-kr%c3%b3l) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R077, CAT-6.3-R174 |
| [se-unix-797704](https://unix.stackexchange.com/q/797704) | [hlooo](https://unix.stackexchange.com/users/758799/hlooo) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R151 |
| [se-unix-801911](https://unix.stackexchange.com/q/801911) | [Seamus](https://unix.stackexchange.com/users/286615/seamus) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R076, CAT-6.3-R142, CAT-6.3-R160 |
| [se-unix-806257](https://unix.stackexchange.com/q/806257) | [anthony](https://unix.stackexchange.com/users/68648/anthony) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.3-R175 |
| [se-unix-89006](https://unix.stackexchange.com/q/89006) | [Braiam](https://unix.stackexchange.com/users/41104/braiam) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.3-R159 |

### TEST adaptations — 12.11.2026

Twenty published maintenance bodies are retained inside a newly authored, guarded mktemp fixture. These rows are synthetic derivatives, not unchanged real excerpts. Original excerpts, source URLs, licenses/authors and the complete transformation remain in sources.csv and CSV seed. Each derivative retains its base license; the four original TEST examples remain separate.
