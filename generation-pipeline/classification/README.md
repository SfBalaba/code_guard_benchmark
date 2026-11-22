# CAT-3 class and severity scenarios

`train/CAT-3.jsonl` contains fictional, train-only policy decisions, not command-generation seeds or human-reviewed labels. Each row describes the proposed effect and supplies the relevant scope, recovery evidence and policy. The local rules in a scenario are facts of that exercise, not new global restrictions.

For class-and-severity training, present only `scenario` and the applicable CAT-3 policy to the classifier. Use `target.class` and `target.severity` as the two answers and `target.rationale` as their explanation. Keep `case_id` for joins and `risk` for grouping. Do not include `target` in the model input. These authored training examples are not a held-out accuracy benchmark.

Assign the class and severity independently. `allow` means independently benign, `ask` means a responsible human must decide, and `deny` requires an applicable prohibition. `low`, `medium`, `high` and `critical` describe impact, not confidence or permission. For example, C310 and C320 describe the same production rollout: the active freeze changes the class, not its impact. C306 and C317 both have critical impact, but the category rules treat production infrastructure teardown differently from cluster retirement.

The separate `seeds/train/CAT-3.jsonl` under `generation-pipeline/` remains the input for generating read-only CLI examples. Do not pass the classification file to `cgen` as `seeds_path` or convert its scenarios into command prompts. It has neither command text nor command-generation instructions.
