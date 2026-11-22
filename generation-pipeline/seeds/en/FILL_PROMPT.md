# Prompt to give another model (with FILL_INPUT.json attached)

You are translating and lightly tightening four category "risk definition" paragraphs from Russian to
English. They are reference text for a **defensive** dataset (CodeGuard-Bench): a pre-execution guard is
trained to classify Bash commands as allow / ask / deny, and these paragraphs tell a generator model what
each risk category means and how its safe counterexample must differ. You are not producing exploit code;
you are translating labeling definitions. Output is pasted verbatim into a generation template.

## Input

`FILL_INPUT.json`: `{ "CAT-5.1": {"ru_risk_block": "..."}, ... }` — four categories, each with the Russian
source paragraph.

## Output

Return ONE JSON object, nothing else:

```json
{
  "CAT-5.1": {"risk_block": "RISK: ...", "safe_block": "- ...\n- ..."},
  "CAT-5.2": {"risk_block": "...", "safe_block": "..."},
  "CAT-5.3": {"risk_block": "...", "safe_block": "..."},
  "CAT-5.4": {"risk_block": "...", "safe_block": "..."}
}
```

For each category produce two English strings from its `ru_risk_block`:

- **`risk_block`** — the risky-side definition. Start with a line `RISK: <CAT-5.N name>`. State, faithfully
  from the source: what makes the command dangerous, the required labels (e.g. "risky = deny/critical";
  keep any ask/high distinction exactly as the source gives it), every exclusion ("out of scope: ..."),
  and the cap on close variants of one recipe ("at most N ...").
- **`safe_block`** — 2–5 bullet lines (each starting `- `) stating what the safe counterexample must do:
  the same utility, the safe transformation named in the source, and the correct **direction / form** where
  the source implies it (e.g. an outgoing connection rather than a listening port; sending the intended
  file rather than fetching; the specific forward direction). End with "Labels: safe = allow/low" if the
  source says so.

## Rules

- Faithful. Keep every condition, label, exclusion and the recipe cap. Do NOT add new constraints,
  example commands, flags, utilities, hosts or file names that are not in the source. Do NOT soften or drop
  an exclusion.
- Clear, direct, imperative English for a 24–27B model. You may split long sentences and drop pure
  boilerplate, but meaning must not change.
- Keep technical terms and category names exactly (reverse shell, bind shell, exfiltration, tunneling, RCE,
  FIFO, fd, relay, `-R`, `put`).
- No markdown inside the strings except the `- ` bullet markers in `safe_block`.
- Output valid UTF-8 JSON with exactly the four keys above.

When you return the JSON, it is loaded with `python3 tools/load_fill.py --in <file>.json`.
