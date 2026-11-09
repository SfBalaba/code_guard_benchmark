# CAT-5.2 — Interactive Reverse Shell

TEST-набор Bash-команд для GNU/Linux: исходящий канал управления локальной оболочкой или исполнителем команд.
Версия: **v0.3**. Сбор: **07.11.2026**; обновление карточки: **08.11.2026**.
Покрытие: **CAT-5 / CAT-5.2 — 250/250 команд**. Другие подкатегории в этот пакет не входят.

## Состав и разметка

| Class | Severity | Команд |
| --- | --- | --- |
| allow | low | 189 |
| deny | critical | 61 |

`ask`, `modify`, `defer`: 0. Жёлтая зона (`ask`): 0.
`source=real`: 250; `synthetic`: 0; local: 0.
`deny` — внешняя сторона получает исполнение команд; `allow` — чтение или обмен данными без исполнения входящего текста.

Предпосылки: GNU/Linux, Bash 5.2 и зависимости опубликованных примеров; конкретные реализации и условия работы указаны в sources.csv. Класс отражает запрашиваемое действие.

## Файлы

- [commands.csv](commands.csv) — 250 команд, UTF-8, разделитель — запятая.
- [sources.csv](sources.csv) — 60 URL источников, цитаты, SHA-256, изменения и связи с контрпримерами; `record_id` — номер записи в commands.csv.
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) — лицензии, атрибуция и полные тексты уведомлений; сведения по строкам — в sources.csv.
- [seeds/](seeds/README.md) — 20 промптов только для будущего **TRAIN**; TEST ими не генерировался. Для TEST/val их не использовать.

Порядок колонок commands.csv:

`command,description,util,severity,category,risk,source,seed,class`

`category=CAT-5`, `risk=CAT-5.2`, `source=real`, `seed=-`.

## Утилиты

`awk` (3), `bash` (16), `curl` (20), `lua` (3), `nc` (31), `ncat` (23), `node` (2), `openssl` (8), `perl` (6), `php` (8), `pwncat` (14), `python` (7), `python3` (7), `ruby` (6), `socat` (62), `telnet` (7), `websocat` (25), `zsh` (2).

## Источники и обработка

203 строки из опубликованной документации и шаблонов, 26 из Q&A, 21 из регрессионных тестов защитных инструментов. Это не нативные логи и не подтверждённая инцидентная телеметрия.
Извлечены опубликованные строки и строковые поля JSON/JSONL/Python, сняты разметка, prompt и поясняющие аннотации. Параметры документации связаны и необязательные аргументы выбраны однократно на фрагмент; новые вариации из шаблонов не генерировались.
Случайный sampling не применялся; `random_state` не использовался.
Генерация TEST не проводилась; модель не использовалась.

Все источники ниже используются для риска **CAT-5.2**, включая безопасные контрпримеры. Построчная привязка и точные изменения — в [sources.csv](sources.csv).

| Источник | Строк | Обработка |
| --- | --- | --- |
| [openssl-sclient — docs.openssl.org](https://docs.openssl.org/master/man1/openssl-s_client/) | 2 | Извлечение литералов/команд; без изменения команды |
| [gtfo-bash-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/bash/) | 3 | Извлечение литералов/команд; без изменения команды |
| [gtfo-gawk-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/gawk/) | 1 | Извлечение литералов/команд; без изменения команды |
| [gtfo-lua-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/lua/) | 2 | Извлечение литералов/команд; без изменения команды |
| [gtfo-nc-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/nc/) | 1 | Извлечение литералов/команд; без изменения команды |
| [gtfo-node-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/node/) | 2 | Извлечение литералов/команд; без изменения команды |
| [gtfo-perl-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/perl/) | 2 | Извлечение литералов/команд; без изменения команды |
| [gtfo-php-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/php/) | 1 | Извлечение литералов/команд; без изменения команды |
| [gtfo-python-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/python/) | 2 | Извлечение литералов/команд; без изменения команды |
| [gtfo-ruby-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/ruby/) | 2 | Извлечение литералов/команд; без изменения команды |
| [gtfo-socat-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/socat/) | 1 | Извлечение литералов/команд; без изменения команды |
| [gtfo-telnet-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/telnet/) | 1 | Извлечение литералов/команд; без изменения команды |
| [gtfo-zsh-page — gtfobins.github.io](https://gtfobins.github.io/gtfobins/zsh/) | 2 | Извлечение литералов/команд; без изменения команды |
| [ncat-reference — nmap.org](https://nmap.org/book/ncat-man.html) | 6 | Извлечение литералов/команд; без изменения команды |
| [0dayCTF/reverse-shell-generator: js/data.js](https://raw.githubusercontent.com/0dayCTF/reverse-shell-generator/main/js/data.js) | 30 | Извлечение литералов/команд; однократное связывание параметров |
| [3ndG4me/socat: doc/socat.html](https://raw.githubusercontent.com/3ndG4me/socat/master/doc/socat.html) | 6 | Извлечение литералов/команд; без изменения команды |
| [D4Vinci/One-Lin3r: one_lin3r/core/liners/linux/awk/reverse_udp.py](https://raw.githubusercontent.com/D4Vinci/One-Lin3r/711a040205f27255cb59c356c8a90f3978f7f902/one_lin3r/core/liners/linux/awk/reverse_udp.py) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [D4Vinci/One-Lin3r: one_lin3r/core/liners/linux/nc/reverse_tcp_mkfifo.py](https://raw.githubusercontent.com/D4Vinci/One-Lin3r/711a040205f27255cb59c356c8a90f3978f7f902/one_lin3r/core/liners/linux/nc/reverse_tcp_mkfifo.py) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [D4Vinci/One-Lin3r: one_lin3r/core/liners/linux/nc/reverse_tcp_mknod.py](https://raw.githubusercontent.com/D4Vinci/One-Lin3r/711a040205f27255cb59c356c8a90f3978f7f902/one_lin3r/core/liners/linux/nc/reverse_tcp_mknod.py) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [D4Vinci/One-Lin3r: one_lin3r/core/liners/linux/ncat/reverse_tcp_ssl.py](https://raw.githubusercontent.com/D4Vinci/One-Lin3r/711a040205f27255cb59c356c8a90f3978f7f902/one_lin3r/core/liners/linux/ncat/reverse_tcp_ssl.py) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [D4Vinci/One-Lin3r: one_lin3r/core/liners/linux/perl/reverse_udp_miosocket.py](https://raw.githubusercontent.com/D4Vinci/One-Lin3r/711a040205f27255cb59c356c8a90f3978f7f902/one_lin3r/core/liners/linux/perl/reverse_udp_miosocket.py) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [D4Vinci/One-Lin3r: one_lin3r/core/liners/linux/ruby/reverse_tcp.py](https://raw.githubusercontent.com/D4Vinci/One-Lin3r/711a040205f27255cb59c356c8a90f3978f7f902/one_lin3r/core/liners/linux/ruby/reverse_tcp.py) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [D4Vinci/One-Lin3r: one_lin3r/core/liners/linux/telnet/reverse_tcp_mkfifo.py](https://raw.githubusercontent.com/D4Vinci/One-Lin3r/711a040205f27255cb59c356c8a90f3978f7f902/one_lin3r/core/liners/linux/telnet/reverse_tcp_mkfifo.py) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [cheat/cheatsheets: curl](https://raw.githubusercontent.com/cheat/cheatsheets/master/curl) | 1 | Извлечение литералов/команд; однократное связывание параметров/выбор опций, однократный выбор опций |
| [cheat/cheatsheets: ncat](https://raw.githubusercontent.com/cheat/cheatsheets/master/ncat) | 9 | Извлечение литералов/команд; однократное связывание параметров/выбор опций, однократный выбор опций |
| [curl/curl: docs/MANUAL.md](https://raw.githubusercontent.com/curl/curl/master/docs/MANUAL.md) | 15 | Извлечение литералов/команд; без изменения команды |
| [cytopia/pwncat: README.md](https://raw.githubusercontent.com/cytopia/pwncat/master/README.md) | 14 | Извлечение литералов/команд; без изменения команды |
| [d3m3t3r/socat: EXAMPLES](https://raw.githubusercontent.com/d3m3t3r/socat/master/EXAMPLES) | 34 | Извлечение литералов/команд; снятие аннотаций |
| [manuelschipper/nah: corpus/execution-flows.jsonl](https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/corpus/execution-flows.jsonl) | 21 | Извлечение литералов/команд; без изменения команды |
| [openbsd/src: usr.bin/nc/nc.1](https://raw.githubusercontent.com/openbsd/src/master/usr.bin/nc/nc.1) | 9 | Извлечение литералов/команд; восстановление escape-последовательности |
| [swisskyrepo/PayloadsAllTheThings: Methodology and Resources/Reverse Shell Cheatsheet.md](https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/3.0/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) | 9 | Извлечение литералов/команд; однократное связывание параметров |
| [tldr-pages/tldr: pages/common/curl.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/curl.md) | 3 | Извлечение литералов/команд; однократное связывание параметров/выбор опций, однократный выбор опций |
| [tldr-pages/tldr: pages/common/nc.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/nc.md) | 3 | Извлечение литералов/команд; однократное связывание параметров/выбор опций, однократный выбор опций |
| [tldr-pages/tldr: pages/common/openssl-s_client.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/openssl-s_client.md) | 4 | Извлечение литералов/команд; однократное связывание параметров/выбор опций, однократный выбор опций |
| [tldr-pages/tldr: pages/common/socat.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/socat.md) | 2 | Извлечение литералов/команд; однократное связывание параметров/выбор опций, однократный выбор опций |
| [tldr-pages/tldr: pages/common/telnet.md](https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/telnet.md) | 3 | Извлечение литералов/команд; однократное связывание параметров/выбор опций, однократный выбор опций |
| [uditrajput03/ws-terminal: README.md](https://raw.githubusercontent.com/uditrajput03/ws-terminal/b8e1e85439c9d859de6d582aad51db3069cb44b2/README.md) | 1 | Извлечение литералов/команд; без изменения команды |
| [vi/websocat: doc.md](https://raw.githubusercontent.com/vi/websocat/master/doc.md) | 25 | Извлечение литералов/команд; без изменения команды |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/a/14701003) | 2 | Извлечение литералов/команд; однократное связывание параметров |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/a/19866239) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-python-nslookup — stackoverflow.com](https://stackoverflow.com/a/21850623) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/a/30031062) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-stackoverflow-com-32913262 — stackoverflow.com](https://stackoverflow.com/a/32913534) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/a/35338529) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/a/36726211) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/a/43286683) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/a/44869350) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/a/5730826) | 2 | Извлечение литералов/команд; без изменения команды |
| [se-stackoverflow-com-67724055 — stackoverflow.com](https://stackoverflow.com/a/67724747) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [se-python-dns — stackoverflow.com](https://stackoverflow.com/questions/18544514) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-python3-connect — stackoverflow.com](https://stackoverflow.com/questions/24855168) | 2 | Извлечение литералов/команд; без изменения команды |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/questions/35338529#comment67480905_35338529) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-stackoverflow-com-4922943 — stackoverflow.com](https://stackoverflow.com/questions/5730826#comment81646800_5730826) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-unix-stackexchange-com-213073 — unix.stackexchange.com](https://unix.stackexchange.com/a/213083) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-unix-stackexchange-com-405217 — unix.stackexchange.com](https://unix.stackexchange.com/a/405228) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-unix-stackexchange-com-272971 — unix.stackexchange.com](https://unix.stackexchange.com/a/479296) | 2 | Извлечение литералов/команд; однократное связывание параметров |
| [se-heredoc — unix.stackexchange.com](https://unix.stackexchange.com/a/624378) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-php-one — unix.stackexchange.com](https://unix.stackexchange.com/a/766065) | 1 | Извлечение литералов/команд; однократное связывание параметров |
| [se-php-one — unix.stackexchange.com](https://unix.stackexchange.com/a/781586) | 1 | Извлечение литералов/команд; без изменения команды |
| [se-unix-stackexchange-com-6809 — unix.stackexchange.com](https://unix.stackexchange.com/questions/317142#comment926529_317142) | 1 | Извлечение литералов/команд; без изменения команды |

## Особые случаи и контрпримеры

Реализации netcat, GNU Awk, файловые дескрипторы, наследование сокетов и PTY существенны для разметки. Bind-shell, туннели, сканирование и скрытый payload относятся к другим подкатегориям. Предпосылки файлов, сертификатов и реализаций указаны построчно в sources.csv.

## Проверки и ограничения

Проверены схема, цитаты и происхождение, лицензии, синтаксис, связи с контрпримерами и точные/структурные дубли. Команды не исполнялись; успешная работа в целевой среде не подтверждается.
Набор несбалансирован: always-allow даёт 75,6% accuracy; часть контролей — простые локальные чтения. В D2 найдены 13 близких HEAD-запросов: при использовании D2 для train/val нужно исключить их вхождения и эквиваленты. Три перенаправления `<>` рассмотрены вручную из-за ограничений tree-sitter. Лимит — 5 вариантов на рецепт.

Проверка пересечений ограничена доступными локальными train и историческими индексами; полный командный train/val и предобучение моделей недоступны. Будущие TRAIN-ответы нужно сверить с замороженным TEST. Метрики считать по классам, источникам и группам рецептов. Модельного пилота TRAIN-seeds не было.
