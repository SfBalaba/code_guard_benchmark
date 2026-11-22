# CAT-7.3: Qwen14B S075 — validation and review publication

Full generated batch for this category: **1295 pairs**, 2590 real model responses, 0 explicit copied sides. This directory is separate from the existing 250-row test dataset.

| Pair outcome | Count |
|---|---:|
| pass (agent static conformance) | 0 |
| reject (documented defect) | 271 |
| needs_review (not accepted) | 1024 |

`accepted/pairs.jsonl` and `accepted/commands.jsonl` contain only explicitly read, statically accepted pairs and their two sides. Empty files are intentional when no pair was accepted. `review/rejected_pairs.jsonl` and `review/needs_review_pairs.jsonl` preserve the rest. These are disjoint partitions, not extra generated data.

All pairs received fresh outer Bash parsing, ShellCheck and conservative AST checks. Literal interpreter `-c` bodies and quoted interpreter heredocs were additionally parsed where extractable; dynamic evaluation, generated files, encoded programs, reachability and resource lifetimes are not fully solved. Lint and nested syntax findings are diagnostics, not automatic semantic verdicts. Missing necessary form constructs and absence of a required signal/host action are rejected only in the restricted visible-code checks documented in `validation_tools/conformance.py`.

Both complete outputs were read by the assistant for **36 pairs in this category**. Across the three packages: all 108 B01 scenarios plus ten selected C513 forms (118 pairs total). This is purposive review, not random sampling and not a full manual review of all 3886 pairs. Unresolved pairs remain `needs_review`; no pass is inferred from clean syntax or absence of lint warnings. No overall model accuracy is claimed.

`validation/pairs.jsonl` provides each pair's status, reasons, exact command/output hashes, external contexts and static findings. `validation/agent_reviews.jsonl` contains the explicitly read decisions. `validation/command_analysis.jsonl` retains AST, nested parsing and lint evidence. Exact duplicate occurrences are retained in `validation/exact_duplicates.json`; copied C533 sides are not additional model calls. No near-duplicate/family independence is certified.

Original synthetic `model_records.jsonl`, `model_requests.jsonl`, `model_raw.jsonl` lines are preserved byte-for-byte within this category. `pair_inputs.jsonl`, `planned_requests.jsonl`, `copy_tasks.jsonl`, `scenarios.json` and `forms.json` retain the tasks and required contexts. Always evaluate command + external context together when `evaluation_mode=command_and_context`. Embedded comments are not authoritative context. The original seed `split=train` is historical intent, **not admission to training**.

No allow/ask/deny labels were assigned. `human_gold=false`, `semantic_validation=false`, full manual semantic review incomplete, train/validation admission and test-family independence not established. Even `pass` means assistant static conformance only. This user-authorized review publication does not certify gold data or safe execution. Model programs were never executed, repaired or regenerated during validation.

Run `python3 validate_package.py` from any location to verify all payload SHA, request/raw joins, complete partition, copied contexts, and replay decisions using cached evidence. It needs only Python 3.9+. `validation_tools/audit.py` is the original workspace audit source (workspace paths, pinned Bash and venv required), supplied for provenance; they do not form a standalone model runner. Pinned parser dependencies are in `validation_tools/requirements.txt`. The original S075 run and archive remain unchanged.

Sources: [Bash manual](https://www.gnu.org/software/bash/manual/bash.html), [ShellCheck directives](https://github.com/koalaman/shellcheck/wiki/Directive), [Python os](https://docs.python.org/3/library/os.html), [Python tempfile](https://docs.python.org/3/library/tempfile.html). Local source and guideline hashes, generation settings, model revision and archive SHA are in `source_run.json`. Synthetic model output provenance does not imply a new blanket license grant over the repository's independently sourced test data.
