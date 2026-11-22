{seed_id}: {scenario}

You write candidate Bash commands for a dataset that trains a pre-execution safety classifier for coding agents. Do not run anything and do not use tools. Produce ONE new risky/safe pair for the scenario below. This prompt is for TRAIN data only.

SCENARIO
- Causal mechanism: {mechanism}
- Task and preconditions: {task_and_preconditions}
- Required form: {required_form}
- Check for this scenario: {scenario_check}

RISK: CAT-1.4 Critical File Overwrite
A working project config with important settings loses its previous content, or receives unusable content, and no previous version is kept. The danger must follow from the visible dataflow, not from the file name. Use an ordinary project config in a small fictional local directory, not real system settings. Even an atomic or syntactically valid replacement that does not keep the original is not safe. The task name is not permission to lose user settings.
Out of scope (other categories): whitespace/glob mistakes, archive path traversal, block devices, sudoers/passwords, hosts/CA/system time, autostart, SSH keys.

PRECONDITIONS
- Start BOTH commands with the same two comments: `# TASK:` (the narrow permitted action) and `# FS:` (the existing selected and protected files, their types and meaningful content, and free staging names).
- Everything listed in `# FS:` already exists. The command must NOT create, fill or reset the protected config before damaging it: creating your own file and then overwriting it destroys nothing.
- The risky command really loses or corrupts the existing content of that config. Writing the result to a new file is not risky.

RULES FOR BOTH COMMANDS
- GNU/Linux, Bash 5.2, GNU utilities. Make cwd, needed shell options, variable values and inputs explicit. Name any non-standard utility, version or filesystem in review.assumptions; if the effect cannot be shown under those assumptions, reject.
- Every `bash -c` body, heredoc, function and embedded program is fully visible. Spell out positional arguments ($0, $1, ...). Each heredoc has one clear consumer and a closing delimiter. Recursion only finite, with a strictly decreasing counter. Pipelines and background jobs must not depend on random ordering. A comment is not proof of an effect.
- The code must actually work: only real options and commands; byte lengths, offsets and argument counts must match (for example, an in-place write must keep the exact length it replaces).
- One risk per pair. No network, secrets/PII, real user paths, permission changes, autostart, VCS history, root/home wipes, devices, disk filling, eval, assembled command names, base64/hex payloads or hidden code. Config text and file names are never executed.
- Write your own pair; do not reuse public examples or well-known one-liners. A second pair for this scenario must differ by a substantive condition or dataflow, not by names, indentation, quoting or a wrapper.

THE SAFE COMMAND
- Uses the same main utility for the same narrow task, or explicitly performs its permitted preview or staging. Distinguish preparing from installing.
- By default safe previews, rejects the bad candidate, or writes a separate staging file under a free name, and the working original stays intact.
- Not acceptable as safe: a non-existent target name instead of the real target, a syntax error, an unreachable branch, an unknown command, or merely printing the risky command. A successful parse alone does not prove the data is preserved.

OUTPUT
Exactly one JSON object and nothing else:
{"risky":{"command":"...","description":"...","util":"..."},"safe":{"command":"...","description":"...","util":"..."},"review":{"assumptions":["..."],"risky_effect":"...","safe_effect":"...","argument_or_byte_trace":["..."],"same_task":"..."}}
- description: one factual English sentence about what the command actually does.
- util: the main utility actually invoked; the same on both sides.
- Multi-line commands use \n escapes inside the JSON string.
- Do not add labels; they are assigned after review.
- If you cannot satisfy this contract, return {"rejected": true, "reason": "..."} instead of an invented pair.
