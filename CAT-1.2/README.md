# CAT-1.2 — Spacing & Globbing Syntax Faults

TEST-набор Bash-команд для GNU/Linux: ошибки пробелов, кавычек и масок, расширяющие удаление или перезапись.
Версия: **v1.2-real-synthetic**, **05.11.2026**. Покрытие: **CAT-1 / CAT-1.2 — 250/250**.

## Состав и разметка

| Class | Severity | Команд |
| --- | --- | --- |
| modify | critical | 113 |
| allow | low | 137 |

`deny/ask/defer`: 0. Жёлтая зона: 0. **105 real + 145 synthetic**, local: 0.
`modify` — исправить границы цели; `allow` — ограниченная операция или неисполняемый вывод.
Для каждой modify-строки указан allow-контрпример той же утилитой.

Предпосылки: Bash 5.2, GNU-утилиты, extglob включён, `cwd=/workspace/project`. Примеры независимы; узкая задача разрешена. TASK/FS задают существующие имена и сохраняемые соседние данные; новые backup-назначения свободны. `<LF>`/`<TAB>` — символы в имени, `␠` — пробел. Скрытые aliases, symlink, mounts и неявные позиционные аргументы не предполагаются.

## Файлы

- [commands.csv](commands.csv) — 250 команд, UTF-8, разделитель — запятая.
- [sources.csv](sources.csv) — источники, обработка, авторство, SHA-256 и контрпримеры; `record_id` — номер записи данных в commands.csv.
- [seeds/](seeds/README.md) — 20 TEST-промптов для синтетики.

`command,description,util,severity,category,risk,source,seed,class`

`category=CAT-1`, `risk=CAT-1.2`. Для real: `seed=-`; для synthetic: полный промпт со сценарием. Другие подкатегории в пакет не входят.

## Утилиты

`bash`, `cp`, `echo`, `find`, `mv`, `rm`, `sh`, `truncate`, `xargs`.

## Источники и обработка

Real: 83 публикации — документация, Q&A и тесты. Из 105 строк восемь взяты из сообщений участников об ошибках, пять — из регрессионных тестов. Исполнение каждой команды независимо не подтверждено.
Убраны разметка и prompt, декодированы исходные литералы; пути, аргументы и значимые переносы сохранены. Секреты/PII не обнаружены. Построчная атрибуция — в sources.csv.

Synthetic: **Codex (GPT-6)**, рабочая сессия; точный API ID и параметры семплирования недоступны. Обычная модель вместо abliterated согласована; кандидаты Guard — CodeBERT/UniXcoder. Для synthetic `source_url=-`, SHA-256 относится к авторскому случаю.
Случайного отбора нет (`random_state` не применялся). Подстановка путей для размножения и публичные примеры как few-shot не использовались.

<details>
<summary>Источники CAT-1.2, включая контрпримеры</summary>

- [Ask Ubuntu: In short i accidentally typed sudo rm /* and now my system doesnt boot as something is deleted in / (ответ)](https://askubuntu.com/a/1354842)
- [Ask Ubuntu: How do you delete a folder that contains spaces? (ответ)](https://askubuntu.com/a/140022)
- [Bumblebee: исходный отчёт](https://github.com/MrMEEE/bumblebee-Old-and-abbandoned/issues/123)
- [BashFAQ 020: списки имён](https://mywiki.wooledge.org/BashFAQ/020)
- [BashFAQ 030: переименование](https://mywiki.wooledge.org/BashFAQ/030)
- [BashGuide: Commands and Arguments](https://mywiki.wooledge.org/BashGuide/CommandsAndArguments)
- [ShellCheck: регрессионные тесты](https://raw.githubusercontent.com/koalaman/shellcheck/master/src/ShellCheck/Analytics.hs)
- [nah: регрессионные тесты shell resolution](https://raw.githubusercontent.com/manuelschipper/nah/main/corpus/shell-resolution.jsonl)
- [Server Fault: Bash find command verbose output (ответ)](https://serverfault.com/a/932883)
- [Stack Overflow: Problems with variables with spaces (ответ)](https://stackoverflow.com/a/12945102)
- [Stack Overflow: how to delete a file with quote in file name (ответ)](https://stackoverflow.com/a/28504870)
- [Stack Overflow: how to delete a file with quote in file name (ответ)](https://stackoverflow.com/a/28510922)
- [Stack Overflow: how to delete a file with quote in file name (ответ)](https://stackoverflow.com/a/28527368)
- [Stack Overflow: rm -f won't handle all arguments in bash script (ответ)](https://stackoverflow.com/a/32479781)
- [Stack Overflow: Linux bash script to find and delete oldest file with special characters and whitespaces in a directory tree if condtion is met (ответ)](https://stackoverflow.com/a/41004647)
- [Stack Overflow: Why can ''rm *(1)*'' delete files which do not contain the string "(1)" in their names? (ответ)](https://stackoverflow.com/a/54618321)
- [Stack Overflow: Bash: find | sed | xargs rm not working, but rm does (ответ)](https://stackoverflow.com/a/56993619)
- [Stack Overflow: why does command line rm not accept quotation marks for directories with spaces? (ответ)](https://stackoverflow.com/a/62021819)
- [Stack Overflow: Problems with variables with spaces](https://stackoverflow.com/questions/12945070/problems-with-variables-with-spaces)
- [Stack Overflow: Bash rm command not working from inside loop](https://stackoverflow.com/questions/30465089/bash-rm-command-not-working-from-inside-loop)
- [Stack Overflow: Linux bash script to find and delete oldest file with special characters and whitespaces in a directory tree if condtion is met](https://stackoverflow.com/questions/40985701/linux-bash-script-to-find-and-delete-oldest-file-with-special-characters-and-whi)
- [Stack Overflow: BASH - Safe check before running "rm -fr $FOLDER"](https://stackoverflow.com/questions/42127702/bash-safe-check-before-running-rm-fr-folder)
- [Stack Overflow: Different rm -f behavior between bash and oh-my-zsh](https://stackoverflow.com/questions/45798113/different-rm-f-behavior-between-bash-and-oh-my-zsh)
- [Stack Overflow: Deleting the contents of folder with rm -r folder_name/* in npm script gives 'no such folder or directory' error](https://stackoverflow.com/questions/49859421/deleting-the-contents-of-folder-with-rm-r-folder-name-in-npm-script-gives-no)
- [Stack Overflow: Deleting filenames that have space and special characters](https://stackoverflow.com/questions/50618130/deleting-filenames-that-have-space-and-special-characters)
- [Stack Overflow: Why can ''rm *(1)*'' delete files which do not contain the string "(1)" in their names?](https://stackoverflow.com/questions/54618294/why-can-rm-1-delete-files-which-do-not-contain-the-string-1-in-their)
- [Stack Overflow: Bash script to delete oldest file causes error - but used to work before](https://stackoverflow.com/questions/79777579/bash-script-to-delete-oldest-file-causes-error-but-used-to-work-before)
- [Super User: How to write more than one line in a launcher (ответ)](https://superuser.com/a/441465)
- [Super User: Delete all file except some in bash, without cd to the directory? (ответ)](https://superuser.com/a/647424)
- [Super User: Delete all file except some in bash, without cd to the directory?](https://superuser.com/questions/647421/delete-all-file-except-some-in-bash-without-cd-to-the-directory)
- [Unix & Linux: Mass mv on files and changing filenames (ответ)](https://unix.stackexchange.com/a/122957)
- [Unix & Linux: xargs line too long (ответ)](https://unix.stackexchange.com/a/150841)
- [Unix & Linux: What does `mv ./*` without specifying destination do? (ответ)](https://unix.stackexchange.com/a/151499)
- [Unix & Linux: Remove all files/directories except for one file (ответ)](https://unix.stackexchange.com/a/154067)
- [Unix & Linux: How to quote arguments with xargs (ответ)](https://unix.stackexchange.com/a/172482)
- [Unix & Linux: What are your favorite *painful* Unix moments (ответ)](https://unix.stackexchange.com/a/20768)
- [Unix & Linux: Deleting files with spaces in their names (ответ)](https://unix.stackexchange.com/a/208141)
- [Unix & Linux: Deleting files with spaces in their names (ответ)](https://unix.stackexchange.com/a/208144)
- [Unix & Linux: Deleting files with spaces in their names (ответ)](https://unix.stackexchange.com/a/208162)
- [Unix & Linux: Deleting files with spaces in their names (ответ)](https://unix.stackexchange.com/a/208193)
- [Unix & Linux: How to delete directories based on `find` output? (ответ)](https://unix.stackexchange.com/a/234582)
- [Unix & Linux: Is using xargs faster than not using it? (ответ)](https://unix.stackexchange.com/a/24526)
- [Unix & Linux: Why did mv delete a file with mv id_rsa *.old? (ответ)](https://unix.stackexchange.com/a/269596)
- [Unix & Linux: Rename all the files with a specific extension in all the subdirectory (ответ)](https://unix.stackexchange.com/a/279673)
- [Unix & Linux: How to replace the spaces in filenames with underscore (ответ)](https://unix.stackexchange.com/a/321456)
- [Unix & Linux: rm command in bash script does not work with variable (ответ)](https://unix.stackexchange.com/a/326586)
- [Unix & Linux: using xargs to grep multiple patterns (ответ)](https://unix.stackexchange.com/a/33072)
- [Unix & Linux: Remove directories interactively using xargs (ответ)](https://unix.stackexchange.com/a/372507)
- [Unix & Linux: What are your favorite *painful* Unix moments (ответ)](https://unix.stackexchange.com/a/4113)
- [Unix & Linux: xargs with rm + filename containing spaces (ответ)](https://unix.stackexchange.com/a/435765)
- [Unix & Linux: Deleting files using pattern matching for files containing spaces and asterisks (ответ)](https://unix.stackexchange.com/a/451811)
- [Unix & Linux: Deleting files using pattern matching for files containing spaces and asterisks (ответ)](https://unix.stackexchange.com/a/451823)
- [Unix & Linux: quote files matched by grep (ответ)](https://unix.stackexchange.com/a/460144)
- [Unix & Linux: Sort and mv files based on filename (with spaces), recursively (ответ)](https://unix.stackexchange.com/a/522380)
- [Unix & Linux: Xargs and rm with a * (ответ)](https://unix.stackexchange.com/a/5250)
- [Unix & Linux: find xargs rm with filename pattern in variable (ответ)](https://unix.stackexchange.com/a/577948)
- [Unix & Linux: Too many files to delete (rm) with wildcard in a shell script? (ответ)](https://unix.stackexchange.com/a/591947)
- [Unix & Linux: Using wildcard to remove similar named files suffixed with number of multiple digits (ответ)](https://unix.stackexchange.com/a/594310)
- [Unix & Linux: Removing directories with spaces in their directory paths (ответ)](https://unix.stackexchange.com/a/728752)
- [Unix & Linux: Deleting files using find/awk/rm pipe: problem with spaces in file names (ответ)](https://unix.stackexchange.com/a/729916)
- [Unix & Linux: How do I delete files with the same names in multiple sub-folders from the command line? (ответ)](https://unix.stackexchange.com/a/741563)
- [Unix & Linux: Accidently deleted entire home directory with rm-rf due to stray space, how can I recover my files (ответ)](https://unix.stackexchange.com/a/806953)
- [Unix & Linux: Mass mv on files and changing filenames](https://unix.stackexchange.com/questions/122954/mass-mv-on-files-and-changing-filenames)
- [Unix & Linux: Remove files and directories even if not empty, except some directories](https://unix.stackexchange.com/questions/140533/remove-files-and-directories-even-if-not-empty-except-some-directories)
- [Unix & Linux: Why does the input to xargs is 1 string but without is strings in separate line?](https://unix.stackexchange.com/questions/187288/why-does-the-input-to-xargs-is-1-string-but-without-is-strings-in-separate-line)
- [Unix & Linux: Deleting files with spaces in their names](https://unix.stackexchange.com/questions/208140/deleting-files-with-spaces-in-their-names)
- [Unix & Linux: How to replace spaces in all file names with underscore in Linux using shell script?](https://unix.stackexchange.com/questions/223182/how-to-replace-spaces-in-all-file-names-with-underscore-in-linux-using-shell-scr)
- [Unix & Linux: How can I turn `file` tool into a predicate for `find`?](https://unix.stackexchange.com/questions/223962/how-can-i-turn-file-tool-into-a-predicate-for-find)
- [Unix & Linux: Why did mv delete a file with mv id_rsa *.old?](https://unix.stackexchange.com/questions/269593/why-did-mv-delete-a-file-with-mv-id-rsa-old)
- [Unix & Linux: Interactive remove files listed with paths in text file](https://unix.stackexchange.com/questions/273402/interactive-remove-files-listed-with-paths-in-text-file)
- [Unix & Linux: All my files have been erased after I tried to make my audio better](https://unix.stackexchange.com/questions/306731/all-my-files-have-been-erased-after-i-tried-to-make-my-audio-better)
- [Unix & Linux: Dealing with spaces of variables for `mv`](https://unix.stackexchange.com/questions/385384/dealing-with-spaces-of-variables-for-mv)
- [Unix & Linux: Find and remove many files by specific content](https://unix.stackexchange.com/questions/46749/find-and-remove-many-files-by-specific-content)
- [Unix & Linux: xargs: 'ls' terminated by signal 13](https://unix.stackexchange.com/questions/468093/xargs-ls-terminated-by-signal-13)
- [Unix & Linux: Xargs rm doesn't work when running it in a script as part of a core_pattern](https://unix.stackexchange.com/questions/470591/xargs-rm-doesnt-work-when-running-it-in-a-script-as-part-of-a-core-pattern)
- [Unix & Linux: cp and mv using wildcards and forgetting to specify a destination directory](https://unix.stackexchange.com/questions/557827/cp-and-mv-using-wildcards-and-forgetting-to-specify-a-destination-directory)
- [Unix & Linux: Why is zsh ignoring my -f switch when removing files?](https://unix.stackexchange.com/questions/562415/why-is-zsh-ignoring-my-f-switch-when-removing-files)
- [Unix & Linux: xargs command is running on local machine but results in an "invalid command" error when run on remote host](https://unix.stackexchange.com/questions/570334/xargs-command-is-running-on-local-machine-but-results-in-an-invalid-command-er)
- [Unix & Linux: find xargs rm with filename pattern in variable](https://unix.stackexchange.com/questions/577946/find-xargs-rm-with-filename-pattern-in-variable)
- [Unix & Linux: Deleting files using find/awk/rm pipe: problem with spaces in file names](https://unix.stackexchange.com/questions/729913/deleting-files-using-find-awk-rm-pipe-problem-with-spaces-in-file-names)
- [Unix & Linux: Untar an archive without creating missing directories](https://unix.stackexchange.com/questions/734559/untar-an-archive-without-creating-missing-directories)
- [Unix & Linux: Accidently deleted entire home directory with rm-rf due to stray space, how can I recover my files](https://unix.stackexchange.com/questions/806952/accidently-deleted-entire-home-directory-with-rm-rf-due-to-stray-space-how-can)
- [ShellCheck SC2114: исправление Bumblebee](https://www.shellcheck.net/wiki/SC2114)

</details>

## Особые случаи и контрпримеры

- `read`: склейка строк через backslash-LF; исправление — `read -r`.
- `xargs`: потеря границ имён; контрпример — NUL на всём конвейере.
- `bash -c`: повторный разбор пути; контрпример — quoted позиционные аргументы.
- Extglob/globstar: активная маска вместо буквального компонента; исправление — кавычки.
- GNU-режимы: simple-backup в mv заменяет предыдущую копию; --parents в cp сохраняет компоненты исходного пути.

Есть вложенные функции, два уровня `bash -c`, многоуровневое кавычение, heredoc и конечная рекурсия.

## Проверки и ограничения

Проверены схема, источники, разметка, синтаксис, контрпримеры и exact/near-дубли. Пересечений с доступными train/README-индексами и CAT-1.1/1.3/1.4 не найдено. Исторический train доступен частично; проверка ограничена сохранёнными индексами и пятью CSV. Пять real-конструкций проверены отдельно из-за ограничений AST-парсера. Команды не исполнялись; полного GNU/Linux runtime-теста нет.

Команды, seed-промпты и близкие производные закреплены за **TEST**; не использовать в train или few-shot Guard.

<details>
<summary>nah — MIT License</summary>

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

</details>
