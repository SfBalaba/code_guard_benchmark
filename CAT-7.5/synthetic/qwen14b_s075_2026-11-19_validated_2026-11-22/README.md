# CAT-7.5: Qwen14B S075 — validation and review publication

Full generated batch for this category: **1295 pairs**, 2554 real model responses, 36 explicit copied sides. This directory is separate from the existing 250-row test dataset.

| Pair outcome | Count |
|---|---:|
| pass | 2 |
| reject | 610 |
| needs_review | 683 |

`accepted/pairs.jsonl` and `accepted/commands.jsonl` contain only explicitly read, statically accepted pairs and their two sides. Empty files are intentional when no pair was accepted. `review/rejected_pairs.jsonl` and `review/needs_review_pairs.jsonl` preserve the rest. These are disjoint partitions, not extra generated data.

All pairs received fresh outer Bash parsing, ShellCheck and conservative AST checks. Literal interpreter `-c` bodies and quoted interpreter heredocs were additionally parsed where extractable; dynamic evaluation, generated files, encoded programs, reachability and resource lifetimes are not fully solved. Lint and nested syntax findings are diagnostics, not automatic semantic verdicts. Missing necessary form constructs and absence of a required signal/host action are rejected only in the restricted visible-code checks documented in `validation_tools/conformance.py`.

The assistant has read both complete extracted commands and external contexts for **68 distinct pairs in this category**, cumulatively across S079/S080. This is targeted review, not random sampling and not a complete individual review. Across all categories, S080 adds 57 newly read pairs and revisits 3 earlier decisions (60 records). It applies additional conservative, replayable necessary-condition checks to the previous 2750-pair open queue. Machine-assessed pairs are not counted as agent-read. Remaining individual review is tracked explicitly; no model accuracy or semantic gold is claimed.

`validation/pairs.jsonl` provides each pair's status, reasons, exact command/output hashes, external contexts and static findings. `validation/agent_reviews.jsonl` contains the explicitly read decisions. `validation/command_analysis.jsonl` retains AST, nested parsing and lint evidence. Exact duplicate occurrences are retained in `validation/exact_duplicates.json`; copied C533 sides are not additional model calls. No near-duplicate/family independence is certified.

Original synthetic `model_records.jsonl`, `model_requests.jsonl`, `model_raw.jsonl` lines are preserved byte-for-byte within this category. `pair_inputs.jsonl`, `planned_requests.jsonl`, `copy_tasks.jsonl`, `scenarios.json` and `forms.json` retain the tasks and required contexts. Always evaluate command + external context together when `evaluation_mode=command_and_context`. Embedded comments are not authoritative context. The original seed `split=train` is historical intent, **not admission to training**.

No allow/ask/deny labels were assigned. `human_gold=false`, `semantic_validation=false`, full manual semantic review incomplete, train/validation admission and test-family independence not established. Even `pass` means assistant static conformance only. This user-authorized review publication does not certify gold data or safe execution. Model programs were never executed, repaired or regenerated during validation.

Run `python3 validate_package.py` from any location to verify all payload SHA, request/raw joins, complete partition, copied contexts, and replay decisions using cached evidence. It needs only Python 3.9+. `validation_tools/audit.py` is the original workspace audit source (workspace paths, pinned Bash and venv required), supplied for provenance; it is not a standalone model runner. Pinned parser dependencies are in `validation_tools/requirements.txt`. The original S075 run and archive remain unchanged.

Sources: [Bash manual](https://www.gnu.org/software/bash/manual/bash.html), [ShellCheck directives](https://github.com/koalaman/shellcheck/wiki/Directive), [Python os](https://docs.python.org/3/library/os.html), [Python tempfile](https://docs.python.org/3/library/tempfile.html). Local source and guideline hashes, generation settings, model revision and archive SHA are in `source_run.json`. Synthetic model output provenance does not imply a new blanket license grant over the repository's independently sourced test data.


## S080 review update, 2026-11-22

`validation/rule_reviews_s080.jsonl` records the additional checks and exact evidence for every assessed pair in this category. Rules only reject when a narrowly admitted visible-code condition fails; otherwise they make no acceptance decision. Setup proof symbolically follows only a restricted top-level prefix and the first iteration of a literal loop. It never runs a program. Arithmetic/subscript evaluation, opaque/deferred code, alias payloads and uncertain declarations block relevant absence proofs. See `validation_tools/review_rules.py` and `setup_proof.py`.

`validation/new_agent_reviews_s080.jsonl` contains this session's individual readings; `agent_reviews_s079_history.jsonl` preserves prior decisions, including superseded ones. `changes_s080.jsonl` is the status delta; `remaining_review_queue.jsonl` lists unresolved checks for every remaining pair. These files describe the same pairs, not extra generated examples. S080 revoked the former C512/B01 acceptance because changing sleep duration between the two sides violates its fixed-fixture contrast; the same criterion was applied to the newly read C512 variants. Existing model outputs and test CSVs were not edited.

Full individual semantic review remains incomplete. Accepted means limited assistant static conformance, not a human safety label, independent family admission or an execution guarantee. No inference or corpus execution occurred. The portable validator replays S079 checks and S080 rules using cached parsing, checks status partitions and all SHA-bound original joins. Parser-level rule tests were run in the workspace using the pinned S079 tools; tests supplied here require that toolchain.
