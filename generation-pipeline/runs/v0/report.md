# Отчёт: v0
Вызовов модели: 690 (ok: 690). Итоговых строк: **886**.
## Отсев по шагам
| шаг | отброшено |
|---|---|
| `clean` | 43 |
| `dedup` | 12 |
| `neardup` | 297 |
| `validate` | 99 |

**Причины, clean:**

| причина | кол-во |
|---|---|
| `pair_label_conflict` | 10 |
| `invalid_json` | 7 |
| `pair_rejected:risky:missing_fields:description,util;safe:missing_fields:description,util` | 4 |
| `pair_rejected:risky:non_ascii_command;safe:non_ascii_command` | 4 |
| `pair_rejected:risky:command_too_long` | 4 |
| `pair_util_mismatch` | 3 |
| `pair_rejected:risky:empty_command;safe:empty_command` | 2 |
| `model_refused` | 2 |
| `pair_rejected:risky:missing_fields:description,util;safe:candidate_not_object` | 2 |
| `pair_rejected:safe:non_ascii_command` | 1 |
| `pair_identical_commands` | 1 |
| `pair_rejected:safe:missing_fields:description` | 1 |
| `pair_rejected:risky:non_ascii_command` | 1 |
| `pair_rejected:risky:foreign_script_in_command;safe:foreign_script_in_command` | 1 |

**Причины, dedup:**

| причина | кол-во |
|---|---|
| `duplicate_in_run` | 12 |

**Причины, neardup:**

| причина | кол-во |
|---|---|
| `near_duplicate` | 141 |
| `family_cap:3` | 64 |
| `family_cap:5` | 47 |
| `near_duplicate_test` | 45 |

**Причины, validate:**

| причина | кол-во |
|---|---|
| `pair_partner_rejected` | 32 |
| `bash_syntax_error` | 30 |
| `contamination:model_reasoning` | 12 |
| `possible_secret_in_command` | 9 |
| `trailing_list_artifact` | 4 |
| `contamination:model_reasoning;bash_syntax_error` | 3 |
| `contamination:fs_listing` | 2 |
| `unknown_flag:rsync:--itemized-changes` | 2 |
| `unknown_flag:cat:-c` | 2 |
| `unknown_flag:cat:-X;unknown_flag:cat:-H;unknown_flag:cat:-d` | 1 |
| `unknown_flag:cat:--name` | 1 |
| `unknown_flag:cat:-r` | 1 |

## Баланс

**class**

| значение | кол-во |
|---|---|
| `allow` | 443 |
| `deny` | 272 |
| `ask` | 171 |

**severity**

| значение | кол-во |
|---|---|
| `low` | 443 |
| `critical` | 272 |
| `high` | 171 |

**risk**

| значение | кол-во |
|---|---|
| `CAT-1.4` | 274 |
| `CAT-5.3` | 172 |
| `CAT-5.2` | 162 |
| `CAT-5.4` | 160 |
| `CAT-5.1` | 118 |

## Разнообразие утилит

Уникальных утилит: 84.

| util | кол-во |
|---|---|
| `python3` | 110 |
| `curl` | 108 |
| `node` | 56 |
| `bash` | 38 |
| `socat` | 34 |
| `ssh` | 32 |
| `wget` | 28 |
| `tar` | 24 |
| `patch` | 20 |
| `envsubst` | 20 |
| `chisel` | 20 |
| `ln` | 18 |
| `rsync` | 16 |
| `fallocate` | 16 |
| `sort` | 16 |

## Покрытие конструкций

Сколько итоговых команд содержит конструкцию.

| конструкция | команд |
|---|---|
| `pipeline` | 145 |
| `chain` | 393 |
| `nested_shell_c` | 123 |
| `command_substitution` | 88 |
| `variable_expansion` | 146 |
| `heredoc` | 135 |
| `process_substitution` | 42 |
| `loop` | 15 |
| `function_def` | 42 |
| `xargs_or_exec` | 6 |
| `eval` | 7 |

## Выход по seed

| seed_id | строк |
|---|---|
| `CAT-1.4-TRAIN-S01` | 18 |
| `CAT-1.4-TRAIN-S02` | 18 |
| `CAT-1.4-TRAIN-S03` | 10 |
| `CAT-1.4-TRAIN-S04` | 18 |
| `CAT-1.4-TRAIN-S05` | 14 |
| `CAT-1.4-TRAIN-S07` | 20 |
| `CAT-1.4-TRAIN-S08` | 20 |
| `CAT-1.4-TRAIN-S09` | 8 |
| `CAT-1.4-TRAIN-S10` | 18 |
| `CAT-1.4-TRAIN-S11` | 16 |
| `CAT-1.4-TRAIN-S12` | 16 |
| `CAT-1.4-TRAIN-S13` | 20 |
| `CAT-1.4-TRAIN-S14` | 12 |
| `CAT-1.4-TRAIN-S15` | 8 |
| `CAT-1.4-TRAIN-S16` | 20 |
| `CAT-1.4-TRAIN-S17` | 16 |
| `CAT-1.4-TRAIN-S18` | 6 |
| `CAT-1.4-TRAIN-S20` | 16 |
| `CAT-5.1-TRAIN-S01` | 6 |
| `CAT-5.1-TRAIN-S02` | 6 |
| `CAT-5.1-TRAIN-S03` | 6 |
| `CAT-5.1-TRAIN-S04` | 6 |
| `CAT-5.1-TRAIN-S05` | 6 |
| `CAT-5.1-TRAIN-S06` | 6 |
| `CAT-5.1-TRAIN-S07` | 6 |
| `CAT-5.1-TRAIN-S08` | 6 |
| `CAT-5.1-TRAIN-S09` | 6 |
| `CAT-5.1-TRAIN-S10` | 6 |
| `CAT-5.1-TRAIN-S11` | 6 |
| `CAT-5.1-TRAIN-S12` | 6 |
| `CAT-5.1-TRAIN-S13` | 6 |
| `CAT-5.1-TRAIN-S14` | 6 |
| `CAT-5.1-TRAIN-S15` | 6 |
| `CAT-5.1-TRAIN-S16` | 6 |
| `CAT-5.1-TRAIN-S17` | 6 |
| `CAT-5.1-TRAIN-S18` | 6 |
| `CAT-5.1-TRAIN-S19` | 6 |
| `CAT-5.1-TRAIN-S20` | 4 |
| `CAT-5.2-TRAIN-S01` | 10 |
| `CAT-5.2-TRAIN-S02` | 10 |
| `CAT-5.2-TRAIN-S03` | 8 |
| `CAT-5.2-TRAIN-S04` | 8 |
| `CAT-5.2-TRAIN-S05` | 8 |
| `CAT-5.2-TRAIN-S06` | 8 |
| `CAT-5.2-TRAIN-S07` | 10 |
| `CAT-5.2-TRAIN-S08` | 4 |
| `CAT-5.2-TRAIN-S09` | 8 |
| `CAT-5.2-TRAIN-S10` | 10 |
| `CAT-5.2-TRAIN-S11` | 6 |
| `CAT-5.2-TRAIN-S12` | 6 |
| `CAT-5.2-TRAIN-S13` | 10 |
| `CAT-5.2-TRAIN-S14` | 8 |
| `CAT-5.2-TRAIN-S15` | 10 |
| `CAT-5.2-TRAIN-S16` | 8 |
| `CAT-5.2-TRAIN-S17` | 10 |
| `CAT-5.2-TRAIN-S18` | 8 |
| `CAT-5.2-TRAIN-S19` | 8 |
| `CAT-5.2-TRAIN-S20` | 4 |
| `CAT-5.3-TRAIN-S01` | 8 |
| `CAT-5.3-TRAIN-S02` | 10 |
| `CAT-5.3-TRAIN-S03` | 6 |
| `CAT-5.3-TRAIN-S04` | 10 |
| `CAT-5.3-TRAIN-S05` | 4 |
| `CAT-5.3-TRAIN-S06` | 8 |
| `CAT-5.3-TRAIN-S07` | 8 |
| `CAT-5.3-TRAIN-S08` | 10 |
| `CAT-5.3-TRAIN-S09` | 8 |
| `CAT-5.3-TRAIN-S10` | 10 |
| `CAT-5.3-TRAIN-S11` | 6 |
| `CAT-5.3-TRAIN-S12` | 10 |
| `CAT-5.3-TRAIN-S13` | 8 |
| `CAT-5.3-TRAIN-S14` | 10 |
| `CAT-5.3-TRAIN-S15` | 10 |
| `CAT-5.3-TRAIN-S16` | 10 |
| `CAT-5.3-TRAIN-S17` | 10 |
| `CAT-5.3-TRAIN-S18` | 8 |
| `CAT-5.3-TRAIN-S19` | 10 |
| `CAT-5.3-TRAIN-S20` | 8 |
| `CAT-5.4-TRAIN-S01` | 8 |
| `CAT-5.4-TRAIN-S02` | 8 |
| `CAT-5.4-TRAIN-S03` | 6 |
| `CAT-5.4-TRAIN-S04` | 10 |
| `CAT-5.4-TRAIN-S05` | 8 |
| `CAT-5.4-TRAIN-S07` | 10 |
| `CAT-5.4-TRAIN-S08` | 4 |
| `CAT-5.4-TRAIN-S09` | 4 |
| `CAT-5.4-TRAIN-S10` | 10 |
| `CAT-5.4-TRAIN-S11` | 10 |
| `CAT-5.4-TRAIN-S12` | 8 |
| `CAT-5.4-TRAIN-S13` | 8 |
| `CAT-5.4-TRAIN-S14` | 8 |
| `CAT-5.4-TRAIN-S15` | 10 |
| `CAT-5.4-TRAIN-S16` | 10 |
| `CAT-5.4-TRAIN-S17` | 10 |
| `CAT-5.4-TRAIN-S18` | 10 |
| `CAT-5.4-TRAIN-S19` | 8 |
| `CAT-5.4-TRAIN-S20` | 10 |

## Флаги и метки

Выдуманные флаги и неверные значения флагов (по словарю `flags/`):

| проблема | кол-во |
|---|---|
| `unknown_flag:rsync:--itemized-changes` | 2 |
| `unknown_flag:cat:-c` | 2 |
| `unknown_flag:cat:-X` | 1 |
| `unknown_flag:cat:-H` | 1 |
| `unknown_flag:cat:-d` | 1 |
| `unknown_flag:cat:--name` | 1 |
| `unknown_flag:cat:-r` | 1 |

Конфликты меток с правилами-якорями — строк на ревью: **3** (`review_queue.jsonl`).

| конфликт | кол-во |
|---|---|
| `label_conflict:read_only:expected=allow` | 3 |

Утилиты без словаря флагов (флаги не проверены):

| util | команд |
|---|---|
| `#` | 67 |
| `ssh` | 40 |
| `socat` | 36 |
| `chisel` | 20 |
| `envsubst` | 19 |
| `fallocate` | 16 |
| `patch` | 14 |
| `depth` | 14 |
| `frpc` | 13 |
| `vim` | 12 |
| `php` | 12 |
| `import` | 12 |
| `as` | 11 |
| `ncat` | 10 |
| `ngrok` | 10 |
| `gost` | 10 |
| `with` | 10 |
| `mkfifo` | 8 |
| `telnet` | 8 |
| `aws` | 8 |
| `bore` | 8 |
| `wstunnel` | 8 |
| `

` | 7 |
| `f.write` | 7 |
| `lua` | 6 |
| `sftp` | 6 |
| `rclone` | 6 |
| `mailx` | 6 |
| `cloudflared` | 6 |
| `rathole` | 6 |
| `n` | 6 |
| `unzip` | 6 |
| `gpg` | 5 |
| `dig` | 5 |
| `blocks` | 5 |
| `.read` | 5 |
| `gcloud` | 4 |
| `mail` | 4 |
| `relay` | 4 |
| `chisel_server` | 4 |
| `chisel_client` | 4 |
| `frps` | 4 |
| `zrok` | 4 |
| `f` | 4 |
| `;
` | 4 |
| `f_rec` | 4 |
| `ex` | 4 |
| `simulated` | 3 |
| `,` | 3 |
| `ss` | 3 |
| `to` | 3 |
| `\n.join` | 3 |
| `]` | 3 |
| `b` | 3 |
| `sys.argv[1],` | 3 |
| `download_rec` | 2 |
| `fetch_installer` | 2 |
| `zmodload` | 2 |
| `lftp` | 2 |
| `send_layer` | 2 |
| `no` | 2 |
| `check.sh` | 2 |
| `client` | 2 |
| `Loopback` | 2 |
| `ip` | 2 |
| `relay_db` | 2 |
| `and` | 2 |
| `[db]` | 2 |
| `
)` | 2 |
| `f,` | 2 |
| `-exec` | 2 |
| `func_assemble` | 2 |
| `def` | 2 |
| `idx,` | 2 |
| `idx` | 2 |
| `index` | 2 |
| `due` | 2 |
| `pass` | 2 |
| `else:` | 2 |
| `out.append` | 2 |
| `blocks[idx]` | 2 |
| `result` | 2 |
| `assemble` | 2 |
| `0,` | 2 |
| `func_get_socket` | 2 |
| `{fd}` | 2 |
| `rec_send` | 2 |
| `Note:` | 2 |
| `call_recursive` | 2 |
| `c` | 2 |
| `client-side` | 2 |
| `f_relay` | 2 |
| `d` | 2 |
| `free` | 2 |
| `config.cfg` | 2 |
| `shutil.copytree` | 2 |
| `settings,` | 2 |
| `zip` | 2 |
| `block{i}` | 2 |
| `1,4` | 2 |
| `print` | 2 |
| `script.py` | 2 |
| `depth-1` | 2 |
| `util` | 2 |
| `a` | 2 |
| `fetch_and_run` | 1 |
| `fetch_and_save` | 1 |
| `9001` | 1 |
| `recv_shell` | 1 |
| `recv_data` | 1 |
| `profile` | 1 |
| `()
` | 1 |
| `i` | 1 |
| `genuinely` | 1 |
| `non-secret` | 1 |
| `jq` | 1 |
| `listening` | 1 |
| `TEST-NET-3` | 1 |
| `internal` | 1 |
| `external` | 1 |
| `server` | 1 |
| `127.0.0.1:8443` | 1 |
| `-` | 1 |
| `PostgreSQL` | 1 |
| `Exposing` | 1 |
| `Mock` | 1 |
| `lines` | 1 |
| `vi` | 1 |
| `outdated_key` | 1 |
| `}n, end=)
    else:
        print(line, end=)` | 1 |
| `the` | 1 |
| `is` | 1 |
| `len` | 1 |
| `==` | 1 |
| `run_socket_exec` | 1 |
| `run_socket_data` | 1 |
| `bash,` | 1 |
| `here` | 1 |
| `SECRET_enc` | 1 |
| `)
` | 1 |
| `target` | 1 |
| `using` | 1 |
| `10.0.0.55:5432` | 1 |
| `0.0.0.0:8080` | 1 |
| `127.0.0.1:3000` | 1 |
| `127.0.0.1:8080` | 1 |
| `path` | 1 |
| `path,` | 1 |
| `f.seek` | 1 |
| `0` | 1 |
| `json.dumps` | 1 |
| `{new_key:new_value}` | 1 |
| `new_config` | 1 |
| `path_new` | 1 |
| `path_new,` | 1 |
| `json.dump` | 1 |
| `new_config,` | 1 |
| `f.fileno` | 1 |
| `fNew config staged at {path_new} with {os.path.getsize(path_new)} bytes` | 1 |
| `diff` | 1 |
| `config,` | 1 |
| `blocks[0]` | 1 |
| `candidate` | 1 |
| `all` | 1 |
| `config.staging,` | 1 |
| `blocks[i]` | 1 |
| `config.txt` | 1 |
| `block` | 1 |
| `new_config.txt` | 1 |
| `content` | 1 |
| `Validation passed. Safe to overwrite.` | 1 |
| `Validation failed. Original config preserved.` | 1 |
| `1` | 1 |
| `[block1]\nkey1=value1\n` | 1 |
| `[block2]\nkey2=value2\n` | 1 |
| `[block3]\nkey3=value3\n` | 1 |
| `chunks` | 1 |
| `sys.argv[i]` | 1 |
| `1,` | 1 |
| `temp_config.txt,` | 1 |
| `Preview:,` | 1 |
| `subprocess.run` | 1 |
| `sys.argv[1:],` | 1 |
| `--exec` | 1 |
| `downloaded_script.py,` | 1 |
| `urllib.request.urlopen` | 1 |
| `--save` | 1 |

## Исправления при очистке

| исправление | кол-во |
|---|---|
| `removed_header_comment_lines` | 407 |
| `label_from_seed_contract` | 274 |
| `label_from_model` | 612 |

## Прочие предупреждения

| предупреждение | кол-во |
|---|---|
| `flags_parse_failed` | 21 |
| `util_not_literal_in_command` | 101 |
