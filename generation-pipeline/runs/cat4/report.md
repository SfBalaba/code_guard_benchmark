# Отчёт: cat4
Вызовов модели: 891 (ok: 891). Итоговых строк: **1072**.
## Отсев по шагам
| шаг | отброшено |
|---|---|
| `clean` | 32 |
| `dedup` | 94 |
| `neardup` | 340 |
| `validate` | 212 |

**Причины, clean:**

| причина | кол-во |
|---|---|
| `model_refused` | 12 |
| `pair_identical_commands` | 7 |
| `invalid_json` | 6 |
| `pair_rejected:risky:empty_command;safe:empty_command` | 4 |
| `pair_util_mismatch` | 2 |
| `pair_rejected:risky:missing_fields:description;safe:missing_fields:description` | 1 |

**Причины, dedup:**

| причина | кол-во |
|---|---|
| `duplicate_in_run` | 78 |
| `overlaps_external` | 16 |

**Причины, neardup:**

| причина | кол-во |
|---|---|
| `near_duplicate` | 260 |
| `near_duplicate_test` | 80 |

**Причины, validate:**

| причина | кол-во |
|---|---|
| `pair_partner_rejected` | 66 |
| `bash_syntax_error` | 60 |
| `contamination:fs_listing` | 29 |
| `held_for_review` | 26 |
| `contamination:model_reasoning` | 8 |
| `contamination:prompt_prefix` | 6 |
| `contamination:fs_listing;contamination:model_reasoning` | 4 |
| `contamination:fs_listing;contamination:prose_line` | 4 |
| `unknown_flag:set:-c` | 2 |
| `possible_secret_in_command;contamination:fs_listing` | 2 |
| `unknown_flag:id:-e` | 1 |
| `contamination:model_reasoning;bash_syntax_error` | 1 |
| `contamination:prose_line;bash_syntax_error` | 1 |
| `contamination:prose_line` | 1 |
| `contamination:user_prefix` | 1 |

## Баланс

**class**

| значение | кол-во |
|---|---|
| `allow` | 536 |
| `deny` | 513 |
| `ask` | 23 |

**severity**

| значение | кол-во |
|---|---|
| `low` | 536 |
| `critical` | 513 |
| `medium` | 23 |

**risk**

| значение | кол-во |
|---|---|
| `CAT-4.3` | 254 |
| `CAT-4.2` | 252 |
| `CAT-4.5` | 214 |
| `CAT-4.1` | 178 |
| `CAT-4.4` | 174 |

## Разнообразие утилит

Уникальных утилит: 92.

| util | кол-во |
|---|---|
| `chmod` | 48 |
| `sed` | 48 |
| `tar` | 34 |
| `awk` | 32 |
| `rsync` | 28 |
| `sqlite3` | 28 |
| `chown` | 26 |
| `openssl` | 22 |
| `tee` | 22 |
| `find` | 20 |
| `chgrp` | 18 |
| `install` | 18 |
| `bash` | 16 |
| `docker` | 16 |
| `gcc` | 16 |

## Покрытие конструкций

Сколько итоговых команд содержит конструкцию.

| конструкция | команд |
|---|---|
| `pipeline` | 51 |
| `chain` | 201 |
| `nested_shell_c` | 112 |
| `command_substitution` | 16 |
| `variable_expansion` | 19 |
| `heredoc` | 25 |
| `process_substitution` | 1 |
| `loop` | 4 |
| `function_def` | 0 |
| `xargs_or_exec` | 18 |
| `eval` | 0 |

## Выход по seed

| seed_id | строк |
|---|---|
| `CAT-4.1-TRAIN-S01` | 14 |
| `CAT-4.1-TRAIN-S02` | 2 |
| `CAT-4.1-TRAIN-S03` | 14 |
| `CAT-4.1-TRAIN-S04` | 8 |
| `CAT-4.1-TRAIN-S05` | 2 |
| `CAT-4.1-TRAIN-S06` | 2 |
| `CAT-4.1-TRAIN-S07` | 14 |
| `CAT-4.1-TRAIN-S08` | 6 |
| `CAT-4.1-TRAIN-S09` | 12 |
| `CAT-4.1-TRAIN-S10` | 6 |
| `CAT-4.1-TRAIN-S11` | 2 |
| `CAT-4.1-TRAIN-S12` | 14 |
| `CAT-4.1-TRAIN-S13` | 8 |
| `CAT-4.1-TRAIN-S14` | 14 |
| `CAT-4.1-TRAIN-S15` | 16 |
| `CAT-4.1-TRAIN-S16` | 12 |
| `CAT-4.1-TRAIN-S17` | 4 |
| `CAT-4.1-TRAIN-S18` | 10 |
| `CAT-4.1-TRAIN-S19` | 6 |
| `CAT-4.1-TRAIN-S20` | 12 |
| `CAT-4.2-TRAIN-S01` | 14 |
| `CAT-4.2-TRAIN-S02` | 18 |
| `CAT-4.2-TRAIN-S03` | 16 |
| `CAT-4.2-TRAIN-S04` | 12 |
| `CAT-4.2-TRAIN-S05` | 18 |
| `CAT-4.2-TRAIN-S06` | 14 |
| `CAT-4.2-TRAIN-S07` | 14 |
| `CAT-4.2-TRAIN-S08` | 4 |
| `CAT-4.2-TRAIN-S09` | 16 |
| `CAT-4.2-TRAIN-S10` | 18 |
| `CAT-4.2-TRAIN-S11` | 10 |
| `CAT-4.2-TRAIN-S12` | 2 |
| `CAT-4.2-TRAIN-S13` | 10 |
| `CAT-4.2-TRAIN-S14` | 10 |
| `CAT-4.2-TRAIN-S15` | 10 |
| `CAT-4.2-TRAIN-S16` | 18 |
| `CAT-4.2-TRAIN-S17` | 14 |
| `CAT-4.2-TRAIN-S18` | 14 |
| `CAT-4.2-TRAIN-S19` | 14 |
| `CAT-4.2-TRAIN-S20` | 6 |
| `CAT-4.3-TRAIN-S01` | 10 |
| `CAT-4.3-TRAIN-S02` | 14 |
| `CAT-4.3-TRAIN-S03` | 12 |
| `CAT-4.3-TRAIN-S04` | 16 |
| `CAT-4.3-TRAIN-S05` | 12 |
| `CAT-4.3-TRAIN-S06` | 12 |
| `CAT-4.3-TRAIN-S07` | 10 |
| `CAT-4.3-TRAIN-S08` | 6 |
| `CAT-4.3-TRAIN-S09` | 16 |
| `CAT-4.3-TRAIN-S10` | 14 |
| `CAT-4.3-TRAIN-S11` | 14 |
| `CAT-4.3-TRAIN-S12` | 12 |
| `CAT-4.3-TRAIN-S13` | 18 |
| `CAT-4.3-TRAIN-S14` | 4 |
| `CAT-4.3-TRAIN-S15` | 18 |
| `CAT-4.3-TRAIN-S16` | 10 |
| `CAT-4.3-TRAIN-S17` | 14 |
| `CAT-4.3-TRAIN-S18` | 14 |
| `CAT-4.3-TRAIN-S19` | 12 |
| `CAT-4.3-TRAIN-S20` | 16 |
| `CAT-4.4-TRAIN-S01` | 10 |
| `CAT-4.4-TRAIN-S02` | 14 |
| `CAT-4.4-TRAIN-S03` | 6 |
| `CAT-4.4-TRAIN-S04` | 6 |
| `CAT-4.4-TRAIN-S05` | 12 |
| `CAT-4.4-TRAIN-S06` | 12 |
| `CAT-4.4-TRAIN-S07` | 2 |
| `CAT-4.4-TRAIN-S08` | 12 |
| `CAT-4.4-TRAIN-S09` | 6 |
| `CAT-4.4-TRAIN-S10` | 8 |
| `CAT-4.4-TRAIN-S11` | 12 |
| `CAT-4.4-TRAIN-S12` | 10 |
| `CAT-4.4-TRAIN-S13` | 14 |
| `CAT-4.4-TRAIN-S14` | 16 |
| `CAT-4.4-TRAIN-S15` | 2 |
| `CAT-4.4-TRAIN-S16` | 6 |
| `CAT-4.4-TRAIN-S17` | 4 |
| `CAT-4.4-TRAIN-S18` | 10 |
| `CAT-4.4-TRAIN-S20` | 12 |
| `CAT-4.5-TRAIN-S01` | 8 |
| `CAT-4.5-TRAIN-S02` | 10 |
| `CAT-4.5-TRAIN-S03` | 14 |
| `CAT-4.5-TRAIN-S04` | 12 |
| `CAT-4.5-TRAIN-S05` | 4 |
| `CAT-4.5-TRAIN-S06` | 12 |
| `CAT-4.5-TRAIN-S07` | 0 |
| `CAT-4.5-TRAIN-S08` | 8 |
| `CAT-4.5-TRAIN-S09` | 12 |
| `CAT-4.5-TRAIN-S10` | 14 |
| `CAT-4.5-TRAIN-S11` | 16 |
| `CAT-4.5-TRAIN-S12` | 16 |
| `CAT-4.5-TRAIN-S13` | 10 |
| `CAT-4.5-TRAIN-S14` | 10 |
| `CAT-4.5-TRAIN-S15` | 8 |
| `CAT-4.5-TRAIN-S16` | 10 |
| `CAT-4.5-TRAIN-S17` | 16 |
| `CAT-4.5-TRAIN-S18` | 14 |
| `CAT-4.5-TRAIN-S19` | 14 |
| `CAT-4.5-TRAIN-S20` | 6 |

Seed без единой строки: CAT-4.5-TRAIN-S07

## Флаги и метки

Выдуманные флаги и неверные значения флагов (по словарю `flags/`):

| проблема | кол-во |
|---|---|
| `unknown_flag:set:-c` | 2 |
| `unknown_flag:id:-e` | 1 |

Конфликты меток с правилами-якорями — строк на ревью: **13** (`review_queue.jsonl`).

_нет_

Утилиты без словаря флагов (флаги не проверены):

| util | команд |
|---|---|
| `sqlite3` | 28 |
| `chgrp` | 18 |
| `zip` | 18 |
| `gcc` | 16 |
| `jq` | 14 |
| `systemd-run` | 14 |
| `tmux` | 14 |
| `socat` | 14 |
| `setfacl` | 14 |
| `setcap` | 14 |
| `umask` | 14 |
| `dpkg-statoverride` | 14 |
| `setfattr` | 14 |
| `gdb` | 14 |
| `tcpdump` | 14 |
| `fzf` | 14 |
| `flock` | 14 |
| `systemd-sysusers` | 14 |
| `terraform` | 14 |
| `gpg` | 14 |
| `pass` | 14 |
| `nsenter` | 12 |
| `systemd-nspawn` | 12 |
| `script` | 12 |
| `strace` | 12 |
| `chpasswd` | 12 |
| `gpasswd` | 12 |
| `sshd` | 12 |
| `newusers` | 12 |
| `keyctl` | 12 |
| `apparmor_parser` | 10 |
| `vim` | 10 |
| `pandoc` | 10 |
| `visudo` | 10 |
| `chage` | 10 |
| `nft` | 10 |
| `sysctl` | 10 |
| `su` | 8 |
| `expect` | 8 |
| `mount` | 8 |
| `soelim` | 8 |
| `machinectl` | 6 |
| `unshare` | 6 |
| `gitleaks` | 6 |
| `nginx` | 4 |
| `runuser` | 4 |
| `busctl` | 4 |
| `rsyslogd` | 2 |
| `validate_bench.sh` | 2 |
| `(
` | 2 |
| `pkexec` | 2 |
| `remount` | 2 |
| `semanage` | 2 |
| `sysusers` | 2 |
| `faillock` | 2 |
| `systemd-analyze` | 2 |
| `#` | 2 |
| `privileged_bin` | 2 |
| `ssh` | 2 |
| `init_check.sh -i` | 1 |
| `init_check.sh` | 1 |
| `check_env.sh` | 1 |
| `megatest.conf` | 1 |
| `sensor_ctl` | 1 |
| `` | 1 |
| `sandbox` | 1 |
| `prowl` | 1 |
| `app_proc` | 1 |
| `servicebin` | 1 |
| `(<` | 1 |
| `check.sh` | 1 |
| `-exec` | 1 |
| `secret_key.pem` | 1 |

## Исправления при очистке

| исправление | кол-во |
|---|---|
| `removed_header_comment_lines` | 1070 |
| `label_from_seed_contract` | 1072 |
| `unescaped_quotes` | 3 |
| `util_normalized` | 16 |

## Прочие предупреждения

| предупреждение | кол-во |
|---|---|
| `util_not_literal_in_command` | 18 |
