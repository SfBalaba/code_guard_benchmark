# CAT-6.5 — Trusted Anchor Tampering

TEST-набор, изменение hosts, CA-доверия и системного времени/NTP, безопасные контрпримеры. Покрытие CAT-6.5, 250 команд. Версия v0.4.1-mixed, обновление 20.11.2026.

## Состав и разметка

| Class | Severity | Команд |
| --- | --- | --- |
| allow | low | 149 |
| deny | high | 101 |

Остальные классы — 0. Источники, 129 real, 121 synthetic, local — 0.
deny/high — изменение системного якоря доверия или времени, allow/low — просмотр, сохранение синхронизации и проверки без изменения доверия.

GNU/Linux, для отдельных сценариев требуются BSD или macOS. Помещение сертификата в каталог CA не объявляется его немедленной активацией.

## Файлы

- [commands.csv](commands.csv) — TEST, UTF-8, разделитель запятая.
- [seeds/](seeds/README.md) — 20 отдельных TRAIN-промптов.

Колонки, `command,description,util,severity,category,risk,source,seed,class`. У всех 129 `real` поле `seed` равно `-`. У всех 121 `synthetic` поле `seed` содержит полное зафиксированное TEST-задание. Переводы строк и значимый синтаксис сохранены. Правки по источникам указаны ниже. Случайный отбор не применялся.

## Утилиты

`cat`, `certutil`, `chronyc`, `cp`, `date`, `echo`, `hwclock`, `keytool`, `mkcert`, `mv`, `ntpdate`, `openssl`, `security`, `sed`, `service`, `sntp`, `systemctl`, `systemsetup`, `tee`, `timedatectl`, `trust`.

## Происхождение и ограничения

Real — опубликованные тесты, документация и примеры сообществ, не подтверждённые инциденты. TEST-синтетика создана отдельно с разрешения пользователя, без TRAIN-seeds. Шаблоны написаны в сессии GPT-6, Guard не относится к GPT по подтверждению пользователя. Нового API-сэмплирования не было, точный backend model ID и полный provider-контекст недоступны. Лицензии баз сохранены для производных.

Код и область CAT-6.5 взяты из расширенного DOCX-гайдлайна. Старый TAXONOMY.pdf перечисляет CAT-6.1–6.4.

В TEST есть исполняемые heredoc и конечная рекурсия. Строка R008 явно вызывает дочерний Bash через `-c` и читает системное время в UTC. Это пример `allow`. Рискованная сторона с такой же формой вызова не покрыта. Лимит пяти близких вариантов применяется к вычисляемому рецепту по тексту команды и учитывает вместе real и synthetic. Синтаксис проверен без исполнения. Будущий TRAIN и независимая экспертная приёмка недоступны.

120 синтетических записей детерминированно собраны из замороженных заданий и опубликованных основ. Диагностическая R008 подготовлена в текущей сессии GPT-6 по отдельному TEST-заданию на основе опубликованного примера чтения времени. TRAIN-промпты в TEST не использовались.

## Источники TEST

Источники относятся к `CAT-6.5`. Ссылки на репозитории ведут на использованные снимки. Правки перечислены для записей, где они применялись.

| Источник | Тип | Real | Synthetic | Лицензии | Правки |
| --- | --- | ---: | ---: | --- | --- |
| [Ask Different, вопрос 215205](https://apple.stackexchange.com/q/215205) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Ask Different, вопрос 277447](https://apple.stackexchange.com/q/277447) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Ask Different, вопрос 323826](https://apple.stackexchange.com/q/323826) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных, удаление приглашения оболочки |
| [Ask Different, вопрос 418144](https://apple.stackexchange.com/q/418144) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Different, вопрос 434709](https://apple.stackexchange.com/q/434709) | вопрос сообщества, опубликованная основа синтетики | 2 | 3 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Ask Different, вопрос 475729](https://apple.stackexchange.com/q/475729) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Ask Different, ответ 472177](https://apple.stackexchange.com/a/472177) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Ask Ubuntu, вопрос 1351383](https://askubuntu.com/q/1351383) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Ask Ubuntu, вопрос 1418836](https://askubuntu.com/q/1418836) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Ask Ubuntu, вопрос 1459452](https://askubuntu.com/q/1459452) | вопрос сообщества, опубликованная основа синтетики | 1 | 2 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Ask Ubuntu, вопрос 381113](https://askubuntu.com/q/381113) | вопрос сообщества, опубликованная основа синтетики | 1 | 3 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Ask Ubuntu, ответ 427334](https://askubuntu.com/a/427334) | опубликованная основа синтетики, ответ сообщества | 1 | 3 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Ask Ubuntu, ответ 502175](https://askubuntu.com/a/502175) | опубликованная основа синтетики, ответ сообщества | 1 | 3 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [FiloSottile/mkcert @ `1c1dc4ed27`](https://github.com/FiloSottile/mkcert/tree/1c1dc4ed27ed5936046b6398d39cab4d657a2d8e) | документация, опубликованная основа синтетики | 1 | 4 | BSD-3-Clause | детерминированная сборка TEST-производных |
| [manuelschipper/nah @ `7230be14c0`](https://github.com/manuelschipper/nah/tree/7230be14c0586c8ebe9a6be0c4d9a43f4949216a) | опубликованная основа синтетики, тесты безопасности | 2 | 1 | MIT | детерминированная сборка TEST-производных |
| [NousResearch/hermes-agent @ `a09d0bc065`](https://github.com/NousResearch/hermes-agent/tree/a09d0bc06543982c93c62d97a2ab5338db9f7f03) | опубликованная основа синтетики, тесты безопасности | 4 | 16 | MIT | детерминированная сборка TEST-производных |
| [p11-glue/p11-kit @ `11f5fc4cb9`](https://github.com/p11-glue/p11-kit/tree/11f5fc4cb93859afeb90acfd031de257d2aaa6c2) | документация, опубликованная основа синтетики, тесты | 3 | 2 | BSD-3-Clause | детерминированная сборка TEST-производных |
| [redcanaryco/atomic-red-team @ `a0e3f9bc69`](https://github.com/redcanaryco/atomic-red-team/tree/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6) | опубликованная основа синтетики, тесты | 4 | 1 | MIT | детерминированная сборка TEST-производных, подстановка опубликованных значений по умолчанию |
| [Stack Overflow, вопрос 44021736](https://stackoverflow.com/q/44021736) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Stack Overflow, ответ 31953251](https://stackoverflow.com/a/31953251) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Stack Overflow, ответ 66889979](https://stackoverflow.com/a/66889979) | ответ сообщества | 2 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Stack Overflow, ответ 67116871](https://stackoverflow.com/a/67116871) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [tldr-pages/tldr @ `ed1f496b34`](https://github.com/tldr-pages/tldr/tree/ed1f496b347fa32446122aa56e254431e2b50fa0) | документация, опубликованная основа синтетики | 11 | 14 | CC-BY-4.0 | выбор опубликованного варианта, детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 189632](https://unix.stackexchange.com/q/189632) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 199224](https://unix.stackexchange.com/q/199224) | вопрос сообщества, опубликованная основа синтетики | 3 | 4 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 220458](https://unix.stackexchange.com/q/220458) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 264909](https://unix.stackexchange.com/q/264909) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 292353](https://unix.stackexchange.com/q/292353) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | удаление приглашения оболочки |
| [Unix & Linux, вопрос 297577](https://unix.stackexchange.com/q/297577) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 306586](https://unix.stackexchange.com/q/306586) | вопрос сообщества, опубликованная основа синтетики | 1 | 2 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 325241](https://unix.stackexchange.com/q/325241) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 402059](https://unix.stackexchange.com/q/402059) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | удаление приглашения оболочки |
| [Unix & Linux, вопрос 404046](https://unix.stackexchange.com/q/404046) | вопрос сообщества, опубликованная основа синтетики | 3 | 6 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 418438](https://unix.stackexchange.com/q/418438) | вопрос сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, вопрос 421919](https://unix.stackexchange.com/q/421919) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 451669](https://unix.stackexchange.com/q/451669) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 452773](https://unix.stackexchange.com/q/452773) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | удаление приглашения оболочки |
| [Unix & Linux, вопрос 478696](https://unix.stackexchange.com/q/478696) | вопрос сообщества, опубликованная основа синтетики | 2 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 505650](https://unix.stackexchange.com/q/505650) | вопрос сообщества, опубликованная основа синтетики | 2 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 513384](https://unix.stackexchange.com/q/513384) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 534466](https://unix.stackexchange.com/q/534466) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 550132](https://unix.stackexchange.com/q/550132) | вопрос сообщества | 2 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 590709](https://unix.stackexchange.com/q/590709) | вопрос сообщества | 3 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 623350](https://unix.stackexchange.com/q/623350) | вопрос сообщества, опубликованная основа синтетики | 4 | 8 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 637309](https://unix.stackexchange.com/q/637309) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 638872](https://unix.stackexchange.com/q/638872) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных, удаление приглашения оболочки |
| [Unix & Linux, вопрос 666996](https://unix.stackexchange.com/q/666996) | вопрос сообщества, опубликованная основа синтетики | 3 | 2 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 735075](https://unix.stackexchange.com/q/735075) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 743795](https://unix.stackexchange.com/q/743795) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 753415](https://unix.stackexchange.com/q/753415) | вопрос сообщества, опубликованная основа синтетики | 1 | 2 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 773529](https://unix.stackexchange.com/q/773529) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 778723](https://unix.stackexchange.com/q/778723) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 779322](https://unix.stackexchange.com/q/779322) | вопрос сообщества, опубликованная основа синтетики | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, вопрос 788787](https://unix.stackexchange.com/q/788787) | вопрос сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 791676](https://unix.stackexchange.com/q/791676) | вопрос сообщества | 2 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, вопрос 797606](https://unix.stackexchange.com/q/797606) | вопрос сообщества, опубликованная основа синтетики | 1 | 2 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных, обезличивание имени хоста, удаление приглашения оболочки |
| [Unix & Linux, ответ 119296](https://unix.stackexchange.com/a/119296) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 122768](https://unix.stackexchange.com/a/122768) | опубликованная основа синтетики, ответ сообщества | 3 | 4 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных, удаление приглашения оболочки |
| [Unix & Linux, ответ 183958](https://unix.stackexchange.com/a/183958) | опубликованная основа синтетики, ответ сообщества | 1 | 2 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 185241](https://unix.stackexchange.com/a/185241) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 199831](https://unix.stackexchange.com/a/199831) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 220688](https://unix.stackexchange.com/a/220688) | опубликованная основа синтетики, ответ сообщества | 1 | 2 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 29](https://unix.stackexchange.com/a/29) | опубликованная основа синтетики, ответ сообщества | 1 | 4 | CC-BY-SA-2.5 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 329507](https://unix.stackexchange.com/a/329507) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 34645](https://unix.stackexchange.com/a/34645) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 402063](https://unix.stackexchange.com/a/402063) | опубликованная основа синтетики, ответ сообщества | 1 | 1 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 424100](https://unix.stackexchange.com/a/424100) | опубликованная основа синтетики, ответ сообщества | 1 | 9 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 434008](https://unix.stackexchange.com/a/434008) | опубликованная основа синтетики, ответ сообщества | 1 | 2 | CC-BY-SA-3.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 451131](https://unix.stackexchange.com/a/451131) | ответ сообщества | 3 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 465286](https://unix.stackexchange.com/a/465286) | опубликованная основа синтетики, ответ сообщества | 1 | 2 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 475211](https://unix.stackexchange.com/a/475211) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 480349](https://unix.stackexchange.com/a/480349) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 613761](https://unix.stackexchange.com/a/613761) | опубликованная основа синтетики, ответ сообщества | 2 | 2 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 617809](https://unix.stackexchange.com/a/617809) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 619388](https://unix.stackexchange.com/a/619388) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 631236](https://unix.stackexchange.com/a/631236) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 635106](https://unix.stackexchange.com/a/635106) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 666973](https://unix.stackexchange.com/a/666973) | ответ сообщества | 2 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 686819](https://unix.stackexchange.com/a/686819) | опубликованная основа синтетики, ответ сообщества | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 69291](https://unix.stackexchange.com/a/69291) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 749650](https://unix.stackexchange.com/a/749650) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 760544](https://unix.stackexchange.com/a/760544) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 774032](https://unix.stackexchange.com/a/774032) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 77825](https://unix.stackexchange.com/a/77825) | ответ сообщества | 1 | 0 | CC-BY-SA-3.0 | без содержательных правок |
| [Unix & Linux, ответ 779379](https://unix.stackexchange.com/a/779379) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |
| [Unix & Linux, ответ 799910](https://unix.stackexchange.com/a/799910) | опубликованная основа синтетики, ответ сообщества | 1 | 1 | CC-BY-SA-4.0 | детерминированная сборка TEST-производных |
| [Unix & Linux, ответ 800686](https://unix.stackexchange.com/a/800686) | ответ сообщества | 1 | 0 | CC-BY-SA-4.0 | без содержательных правок |

## Атрибуция и лицензии

Published examples and their explicitly marked synthetic TEST adaptations retain their original source licenses. No blanket MIT license is asserted. Changes on 2026-11-09 include extraction/prompt removal, one documented option/default binding where recorded and explicit deterministic delivery/control-flow adaptations. Those adaptations are recorded in CSV seed and sources.csv, not relabelled as published incidents. Full source form is distributed in the CSVs; immutable source refs/snapshot hashes, original snippets, authors and changes accompany each row. No additional restrictions are imposed on the CC BY-SA adaptations.

### atomic — MIT

Red Canary, Inc. (2018). [License](https://raw.githubusercontent.com/redcanaryco/atomic-red-team/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6/LICENSE.txt); [scope](https://raw.githubusercontent.com/redcanaryco/atomic-red-team/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6/LICENSE.txt). Source form and adaptations are retained per row.
- [atomics/T1553.004/T1553.004.yaml](https://raw.githubusercontent.com/redcanaryco/atomic-red-team/a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6/atomics/T1553.004/T1553.004.yaml) — `a0e3f9bc69fed2fd711bd1f1aa87a40c33482fe6`.

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

### hermes — MIT

Nous Research (2025). [License](https://raw.githubusercontent.com/NousResearch/hermes-agent/a09d0bc06543982c93c62d97a2ab5338db9f7f03/LICENSE); [scope](https://raw.githubusercontent.com/NousResearch/hermes-agent/a09d0bc06543982c93c62d97a2ab5338db9f7f03/LICENSE). Source form and adaptations are retained per row.
- [tests/tools/test_approval.py](https://raw.githubusercontent.com/NousResearch/hermes-agent/a09d0bc06543982c93c62d97a2ab5338db9f7f03/tests/tools/test_approval.py) — `a09d0bc06543982c93c62d97a2ab5338db9f7f03`.

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

### mkcert — BSD-3-Clause

Filippo Valsorda. [License](https://raw.githubusercontent.com/FiloSottile/mkcert/1c1dc4ed27ed5936046b6398d39cab4d657a2d8e/LICENSE); [scope](https://raw.githubusercontent.com/FiloSottile/mkcert/1c1dc4ed27ed5936046b6398d39cab4d657a2d8e/LICENSE). Source form and adaptations are retained per row.
- [README.md](https://raw.githubusercontent.com/FiloSottile/mkcert/1c1dc4ed27ed5936046b6398d39cab4d657a2d8e/README.md) — `1c1dc4ed27ed5936046b6398d39cab4d657a2d8e`.

```text
Copyright (c) 2018 The mkcert Authors. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

   * Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
   * Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution.
   * Neither the name of Google Inc. nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

### nah — MIT

Manuel Schipper (2026). [License](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/LICENSE); [scope](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/LICENSE). Source form and adaptations are retained per row.
- [corpus/local-utilities.jsonl](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/corpus/local-utilities.jsonl) — `7230be14c0586c8ebe9a6be0c4d9a43f4949216a`.
- [corpus/macos.jsonl](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/corpus/macos.jsonl) — `7230be14c0586c8ebe9a6be0c4d9a43f4949216a`.

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

### p11kit — BSD-3-Clause

Stef Walter and p11-kit contributors. [License](https://raw.githubusercontent.com/p11-glue/p11-kit/11f5fc4cb93859afeb90acfd031de257d2aaa6c2/COPYING); [scope](https://raw.githubusercontent.com/p11-glue/p11-kit/11f5fc4cb93859afeb90acfd031de257d2aaa6c2/COPYING). Source form and adaptations are retained per row.
- [doc/manual/trust.xml](https://raw.githubusercontent.com/p11-glue/p11-kit/11f5fc4cb93859afeb90acfd031de257d2aaa6c2/doc/manual/trust.xml) — `11f5fc4cb93859afeb90acfd031de257d2aaa6c2`.
- [trust/test-extract.sh](https://raw.githubusercontent.com/p11-glue/p11-kit/11f5fc4cb93859afeb90acfd031de257d2aaa6c2/trust/test-extract.sh) — `11f5fc4cb93859afeb90acfd031de257d2aaa6c2`.

```text
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

    * Redistributions of source code must retain the above
      copyright notice, this list of conditions and the
      following disclaimer.
    * Redistributions in binary form must reproduce the
      above copyright notice, this list of conditions and
      the following disclaimer in the documentation and/or
      other materials provided with the distribution.
    * The names of contributors to this software may not be
      used to endorse or promote products derived from this
      software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.
```

### tldr — CC-BY-4.0

tldr-pages team and contributors (2014–present). [License](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/LICENSE.md); [scope](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/LICENSE.md). Source form and adaptations are retained per row.
- [pages/common/certutil.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/certutil.md) — `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/common/chronyc.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/chronyc.md) — `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/common/date.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/date.md) — `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/common/mkcert.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/common/mkcert.md) — `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/timedatectl.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/timedatectl.md) — `ed1f496b347fa32446122aa56e254431e2b50fa0`.
- [pages/linux/trust.md](https://raw.githubusercontent.com/tldr-pages/tldr/ed1f496b347fa32446122aa56e254431e2b50fa0/pages/linux/trust.md) — `ed1f496b347fa32446122aa56e254431e2b50fa0`.

Command pages are documentation under CC BY 4.0; the scripts-only MIT exception does not cover these examples.

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

### Community authors and licenses

Specific post content_license from the official API is used; questions and answers can differ. Original source and any modifications/TEST adaptations are recorded per row. Adapted excerpts retain the stated CC BY-SA version; license links give complete terms.

| Post | Author | License | Records |
| --- | --- | --- | --- |
| [se-apple-215205](https://apple.stackexchange.com/q/215205) | [Quanlong](https://apple.stackexchange.com/users/88922/quanlong) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R043 |
| [se-apple-277447](https://apple.stackexchange.com/q/277447) | [diachedelic](https://apple.stackexchange.com/users/134026/diachedelic) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R040 |
| [se-apple-323826](https://apple.stackexchange.com/q/323826) | [mdong](https://apple.stackexchange.com/users/287100/mdong) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R041, CAT-6.5-R232 |
| [se-apple-418144](https://apple.stackexchange.com/q/418144) | [AnotherCourier](https://apple.stackexchange.com/users/413386/anothercourier) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R107 |
| [se-apple-434709](https://apple.stackexchange.com/q/434709) | [Sahil Gupta](https://apple.stackexchange.com/users/446151/sahil-gupta) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R014, CAT-6.5-R017, CAT-6.5-R224, CAT-6.5-R225, CAT-6.5-R247 |
| [se-apple-472177](https://apple.stackexchange.com/a/472177) | [Rajendra](https://apple.stackexchange.com/users/521592/rajendra) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R067 |
| [se-apple-475729](https://apple.stackexchange.com/q/475729) | [Irad K](https://apple.stackexchange.com/users/266693/irad-k) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R018, CAT-6.5-R220 |
| [se-askubuntu-1351383](https://askubuntu.com/q/1351383) | [Andrew](https://askubuntu.com/users/1229609/andrew) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R108, CAT-6.5-R151 |
| [se-askubuntu-1418836](https://askubuntu.com/q/1418836) | [Kasey champion](https://askubuntu.com/users/1612934/kasey-champion) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R035, CAT-6.5-R140 |
| [se-askubuntu-1459452](https://askubuntu.com/q/1459452) | [Mark Vetter](https://askubuntu.com/users/855777/mark-vetter) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R121, CAT-6.5-R157, CAT-6.5-R239 |
| [se-askubuntu-381113](https://askubuntu.com/q/381113) | [Larry Keenan](https://askubuntu.com/users/218543/larry-keenan) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R026, CAT-6.5-R137, CAT-6.5-R162, CAT-6.5-R163 |
| [se-askubuntu-427334](https://askubuntu.com/a/427334) | [david25272](https://askubuntu.com/users/203830/david25272) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R032, CAT-6.5-R139, CAT-6.5-R166, CAT-6.5-R167 |
| [se-askubuntu-502175](https://askubuntu.com/a/502175) | [saiarcot895](https://askubuntu.com/users/241580/saiarcot895) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R039, CAT-6.5-R142, CAT-6.5-R168, CAT-6.5-R169 |
| [se-stackoverflow-31953251](https://stackoverflow.com/a/31953251) | [dave_thompson_085](https://stackoverflow.com/users/2868801/dave-thompson-085) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R088 |
| [se-stackoverflow-44021736](https://stackoverflow.com/q/44021736) | [ashish bankar](https://stackoverflow.com/users/7930998/ashish-bankar) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R068 |
| [se-stackoverflow-66889979](https://stackoverflow.com/a/66889979) | [Arvind Kumar Avinash](https://stackoverflow.com/users/10819573/arvind-kumar-avinash) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R051, CAT-6.5-R103 |
| [se-stackoverflow-67116871](https://stackoverflow.com/a/67116871) | [masseyb](https://stackoverflow.com/users/1423507/masseyb) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R033 |
| [se-unix-119296](https://unix.stackexchange.com/a/119296) | [Flup](https://unix.stackexchange.com/users/33265/flup) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R013 |
| [se-unix-122768](https://unix.stackexchange.com/a/122768) | [slm](https://unix.stackexchange.com/users/7453/slm) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R050, CAT-6.5-R110, CAT-6.5-R124, CAT-6.5-R152, CAT-6.5-R186, CAT-6.5-R187, CAT-6.5-R240 |
| [se-unix-183958](https://unix.stackexchange.com/a/183958) | [KernelPanic](https://unix.stackexchange.com/users/40993/kernelpanic) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R012, CAT-6.5-R219, CAT-6.5-R223 |
| [se-unix-185241](https://unix.stackexchange.com/a/185241) | [user103406](https://unix.stackexchange.com/users/103406/user103406) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R069 |
| [se-unix-189632](https://unix.stackexchange.com/q/189632) | [Confused Helpdesker](https://unix.stackexchange.com/users/106274/confused-helpdesker) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R003 |
| [se-unix-199224](https://unix.stackexchange.com/q/199224) | [Justin Edmands](https://unix.stackexchange.com/users/87989/justin-edmands) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R005, CAT-6.5-R074, CAT-6.5-R099, CAT-6.5-R182, CAT-6.5-R198, CAT-6.5-R208, CAT-6.5-R214 |
| [se-unix-199831](https://unix.stackexchange.com/a/199831) | [muru](https://unix.stackexchange.com/users/70524/muru) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R072 |
| [se-unix-220458](https://unix.stackexchange.com/q/220458) | [Kokizzu](https://unix.stackexchange.com/users/27996/kokizzu) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R109, CAT-6.5-R237 |
| [se-unix-220688](https://unix.stackexchange.com/a/220688) | [Kokizzu](https://unix.stackexchange.com/users/27996/kokizzu) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R020, CAT-6.5-R226, CAT-6.5-R248 |
| [se-unix-264909](https://unix.stackexchange.com/q/264909) | [chunchiu Chan](https://unix.stackexchange.com/users/148844/chunchiu-chan) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R095 |
| [se-unix-29](https://unix.stackexchange.com/a/29) | [Matt Simmons](https://unix.stackexchange.com/users/22/matt-simmons) | [CC-BY-SA-2.5](https://creativecommons.org/licenses/by-sa/2.5/) | CAT-6.5-R092, CAT-6.5-R183, CAT-6.5-R199, CAT-6.5-R209, CAT-6.5-R215 |
| [se-unix-292353](https://unix.stackexchange.com/q/292353) | [José Carlos Guevara Turruelles](https://unix.stackexchange.com/users/176928/jos%c3%a9-carlos-guevara-turruelles) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R052 |
| [se-unix-297577](https://unix.stackexchange.com/q/297577) | [Johshi](https://unix.stackexchange.com/users/180184/johshi) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R053 |
| [se-unix-306586](https://unix.stackexchange.com/q/306586) | [Anh Tuan](https://unix.stackexchange.com/users/24180/anh-tuan) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R008, CAT-6.5-R029, CAT-6.5-R229 |
| [se-unix-325241](https://unix.stackexchange.com/q/325241) | [MortimerCat](https://unix.stackexchange.com/users/201765/mortimercat) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R019 |
| [se-unix-329507](https://unix.stackexchange.com/a/329507) | [George Vasiliou](https://unix.stackexchange.com/users/188385/george-vasiliou) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R131 |
| [se-unix-34645](https://unix.stackexchange.com/a/34645) | [quanta](https://unix.stackexchange.com/users/7903/quanta) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R127 |
| [se-unix-402059](https://unix.stackexchange.com/q/402059) | [Michal Przybylowicz](https://unix.stackexchange.com/users/34098/michal-przybylowicz) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R101 |
| [se-unix-402063](https://unix.stackexchange.com/a/402063) | [Hunter.S.Thompson](https://unix.stackexchange.com/users/237568/hunter-s-thompson) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R038, CAT-6.5-R231 |
| [se-unix-404046](https://unix.stackexchange.com/q/404046) | [Jawad Al Shaikh](https://unix.stackexchange.com/users/224118/jawad-al-shaikh) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R011, CAT-6.5-R080, CAT-6.5-R126, CAT-6.5-R174, CAT-6.5-R192, CAT-6.5-R206, CAT-6.5-R222, CAT-6.5-R242, CAT-6.5-R246 |
| [se-unix-418438](https://unix.stackexchange.com/q/418438) | [Basj](https://unix.stackexchange.com/users/59989/basj) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R116 |
| [se-unix-421919](https://unix.stackexchange.com/q/421919) | [Victor](https://unix.stackexchange.com/users/60999/victor) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R084, CAT-6.5-R145 |
| [se-unix-424100](https://unix.stackexchange.com/a/424100) | [Steven](https://unix.stackexchange.com/users/275753/steven) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R105, CAT-6.5-R150, CAT-6.5-R184, CAT-6.5-R185, CAT-6.5-R200, CAT-6.5-R201, CAT-6.5-R210, CAT-6.5-R211, CAT-6.5-R216, CAT-6.5-R217 |
| [se-unix-434008](https://unix.stackexchange.com/a/434008) | [Bigon](https://unix.stackexchange.com/users/28791/bigon) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R004, CAT-6.5-R177, CAT-6.5-R195 |
| [se-unix-451131](https://unix.stackexchange.com/a/451131) | [Chris Davies](https://unix.stackexchange.com/users/100397/chris-davies) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R055, CAT-6.5-R096, CAT-6.5-R115 |
| [se-unix-451669](https://unix.stackexchange.com/q/451669) | [owcred601](https://unix.stackexchange.com/users/294411/owcred601) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R118, CAT-6.5-R154 |
| [se-unix-452773](https://unix.stackexchange.com/q/452773) | [H.Mohseni](https://unix.stackexchange.com/users/271793/h-mohseni) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R104 |
| [se-unix-465286](https://unix.stackexchange.com/a/465286) | [andcoz](https://unix.stackexchange.com/users/2634/andcoz) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R087, CAT-6.5-R176, CAT-6.5-R194 |
| [se-unix-475211](https://unix.stackexchange.com/a/475211) | [Milliways](https://unix.stackexchange.com/users/47111/milliways) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R046 |
| [se-unix-478696](https://unix.stackexchange.com/q/478696) | [voidptr127](https://unix.stackexchange.com/users/200271/voidptr127) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R025, CAT-6.5-R075, CAT-6.5-R136 |
| [se-unix-480349](https://unix.stackexchange.com/a/480349) | [kafka](https://unix.stackexchange.com/users/319810/kafka) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R129 |
| [se-unix-505650](https://unix.stackexchange.com/q/505650) | [TheMeaningfulEngineer](https://unix.stackexchange.com/users/29436/themeaningfulengineer) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R098, CAT-6.5-R125, CAT-6.5-R241 |
| [se-unix-513384](https://unix.stackexchange.com/q/513384) | [RobIII](https://unix.stackexchange.com/users/17788/robiii) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R100 |
| [se-unix-534466](https://unix.stackexchange.com/q/534466) | [streppel](https://unix.stackexchange.com/users/44064/streppel) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R048 |
| [se-unix-550132](https://unix.stackexchange.com/q/550132) | [yael](https://unix.stackexchange.com/users/237298/yael) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R057, CAT-6.5-R123 |
| [se-unix-590709](https://unix.stackexchange.com/q/590709) | [jack](https://unix.stackexchange.com/users/402658/jack) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R016, CAT-6.5-R111, CAT-6.5-R113 |
| [se-unix-613761](https://unix.stackexchange.com/a/613761) | [Anthony Dahanne](https://unix.stackexchange.com/users/407552/anthony-dahanne) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R044, CAT-6.5-R059, CAT-6.5-R071, CAT-6.5-R132 |
| [se-unix-617809](https://unix.stackexchange.com/a/617809) | [terdon](https://unix.stackexchange.com/users/22222/terdon) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R063 |
| [se-unix-619388](https://unix.stackexchange.com/a/619388) | [Alexander Pavlov](https://unix.stackexchange.com/users/441772/alexander-pavlov) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R006 |
| [se-unix-623350](https://unix.stackexchange.com/q/623350) | [Aamir Shaikh](https://unix.stackexchange.com/users/308648/aamir-shaikh) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R027, CAT-6.5-R056, CAT-6.5-R094, CAT-6.5-R112, CAT-6.5-R138, CAT-6.5-R149, CAT-6.5-R164, CAT-6.5-R165, CAT-6.5-R180, CAT-6.5-R181, CAT-6.5-R234, CAT-6.5-R250 |
| [se-unix-631236](https://unix.stackexchange.com/a/631236) | [voidptr127](https://unix.stackexchange.com/users/200271/voidptr127) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R091 |
| [se-unix-635106](https://unix.stackexchange.com/a/635106) | [fpmurphy](https://unix.stackexchange.com/users/7919/fpmurphy) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R045 |
| [se-unix-637309](https://unix.stackexchange.com/q/637309) | [VPfB](https://unix.stackexchange.com/users/215626/vpfb) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R081 |
| [se-unix-638872](https://unix.stackexchange.com/q/638872) | [Green 绿色](https://unix.stackexchange.com/users/264974/green-%e7%bb%bf%e8%89%b2) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R089, CAT-6.5-R147 |
| [se-unix-666973](https://unix.stackexchange.com/a/666973) | [atErik](https://unix.stackexchange.com/users/367237/aterik) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R077, CAT-6.5-R079 |
| [se-unix-666996](https://unix.stackexchange.com/q/666996) | [Philipp Claßen](https://unix.stackexchange.com/users/29509/philipp-cla%c3%9fen) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R024, CAT-6.5-R042, CAT-6.5-R130, CAT-6.5-R135, CAT-6.5-R243 |
| [se-unix-686819](https://unix.stackexchange.com/a/686819) | [Chris Davies](https://unix.stackexchange.com/users/100397/chris-davies) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R049, CAT-6.5-R233 |
| [se-unix-69291](https://unix.stackexchange.com/a/69291) | [Stéphane Chazelas](https://unix.stackexchange.com/users/22565/st%c3%a9phane-chazelas) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R007 |
| [se-unix-735075](https://unix.stackexchange.com/q/735075) | [dckoo](https://unix.stackexchange.com/users/560244/dckoo) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R065, CAT-6.5-R144 |
| [se-unix-743795](https://unix.stackexchange.com/q/743795) | [gcb](https://unix.stackexchange.com/users/11805/gcb) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R114 |
| [se-unix-749650](https://unix.stackexchange.com/a/749650) | [David Verdin](https://unix.stackexchange.com/users/165911/david-verdin) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R054 |
| [se-unix-753415](https://unix.stackexchange.com/q/753415) | [Keeran](https://unix.stackexchange.com/users/406928/keeran) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R117, CAT-6.5-R153, CAT-6.5-R238 |
| [se-unix-760544](https://unix.stackexchange.com/a/760544) | [telcoM](https://unix.stackexchange.com/users/258991/telcom) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R073 |
| [se-unix-773529](https://unix.stackexchange.com/q/773529) | [Pila](https://unix.stackexchange.com/users/170988/pila) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R070 |
| [se-unix-774032](https://unix.stackexchange.com/a/774032) | [mYnDstrEAm](https://unix.stackexchange.com/users/233262/myndstream) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R034 |
| [se-unix-77825](https://unix.stackexchange.com/a/77825) | [don_crissti](https://unix.stackexchange.com/users/22142/don-crissti) | [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/) | CAT-6.5-R021 |
| [se-unix-778723](https://unix.stackexchange.com/q/778723) | [sborfedor](https://unix.stackexchange.com/users/617992/sborfedor) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R085, CAT-6.5-R146 |
| [se-unix-779322](https://unix.stackexchange.com/q/779322) | user154426 | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R028, CAT-6.5-R228 |
| [se-unix-779379](https://unix.stackexchange.com/a/779379) | user154426 | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R078 |
| [se-unix-788787](https://unix.stackexchange.com/q/788787) | [user930473](https://unix.stackexchange.com/users/693203/user930473) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R128 |
| [se-unix-791676](https://unix.stackexchange.com/q/791676) | [eftshift0](https://unix.stackexchange.com/users/236478/eftshift0) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R058, CAT-6.5-R076 |
| [se-unix-797606](https://unix.stackexchange.com/q/797606) | [hschou](https://unix.stackexchange.com/users/97316/hschou) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R090, CAT-6.5-R148, CAT-6.5-R236 |
| [se-unix-799910](https://unix.stackexchange.com/a/799910) | [Daniel](https://unix.stackexchange.com/users/589644/daniel) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R060, CAT-6.5-R235 |
| [se-unix-800686](https://unix.stackexchange.com/a/800686) | [Slavik](https://unix.stackexchange.com/users/115648/slavik) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | CAT-6.5-R015 |

### New deterministic TEST compilation — 12.11.2026

Synthetic programs were newly compiled from textual tasks frozen before the compiler and outputs. They remain licensed derivatives of the cited published bases, not independent incidents or model inference responses. CSV seed contains the exact task. Prior programs and transformation implementations are retained in the research history. Original source excerpts, license scope, authors and immutable references remain in sources.csv.
