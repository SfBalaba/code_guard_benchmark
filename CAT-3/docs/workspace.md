# Supervisor workspace guide

## Preparation baseline and authorized ingestion

The initial workspace contained only instructions and empty directories. The subsequent user assignment, “complete task for data ingestion process e2e”, authorizes collection, annotation, inert pipeline implementation, and final dataset artifacts. Current observed results are documented in the root dataset card and audit ledgers, not inferred from this historical preparation baseline.

Read `AGENTS.md` for the governing workflow and record schemas, and `docs/task-source.txt` for the original assignment. This guide does not replace either document. Do not treat planned activities or estimates as completed work.

The current [target revision](target-revision.md) supersedes the original numerical target: **250 total across CAT-3.1–CAT-3.5, not 250 per risk**. The original source task and AGENTS.md remain unchanged historical requirements. Release **v0.1 (2026-10-29)** contains 250 accepted records, up from the initial 92 by 158, with total deficit 0 and no per-risk quota. Current counts, source inventory and limitations belong to the [dataset card](../README.md) and [statistics](../data/processed/statistics.json); historical proposal/research/92-record QA counts are not current results. The [mentor brief](mentor-brief.md) summarizes the research and evidence for handoff.

## Directory purposes and ownership

| Path | Purpose | Write owner |
| --- | --- | --- |
| `data/raw/` | Retain permitted, sanitized source material with its source identity; never retain real secrets/PII or execute embedded commands. | Assigned researcher using uniquely named captures |
| `data/candidates/CAT-3.1/` | Candidate records for CAT-3.1. | CAT-3.1 researcher |
| `data/candidates/CAT-3.2/` | Candidate records for CAT-3.2. | CAT-3.2 researcher |
| `data/candidates/CAT-3.3/` | Candidate records for CAT-3.3. | CAT-3.3 researcher |
| `data/candidates/CAT-3.4/` | Candidate records for CAT-3.4. | CAT-3.4 researcher |
| `data/candidates/CAT-3.5/` | Candidate records for CAT-3.5. | CAT-3.5 researcher |
| `data/review/` | Annotation decisions, counterexample review, and unresolved items. | Single integration owner merges reviewer submissions |
| `data/processed/` | Accepted intermediate records and final provenance accounting. | Single integration owner |
| `research/` | Source discovery evidence, policy and incident research, feasibility findings, and collection estimates. | Researchers in assigned slices; supervisor resolves shared edits |
| `scripts/` | Standard-library inert candidate integration and final CSV/ledger validation. | Single integration owner or explicitly assigned tooling owner |
| `tests/` | Behavior checks for inert tooling where needed; no execution of dataset commands. | Integration/tooling owner; independent QA reviews results |
| `docs/` | Supervisor instructions and task context. | Supervisor |

JSONL ledgers are `research/sources.jsonl`, `data/review/pending.jsonl`, and `data/processed/provenance.jsonl`. Use the schemas in `AGENTS.md`; create records only when supported by actual research or review. Do not add placeholder or fabricated entries. Researchers keep category work separate; the integration owner merges shared files. Proposal ledgers and independent reviews preserve pre-integration decisions; canonical candidate statuses and integration decisions determine the final accepted subset.

## Starting environment and safety boundary

Python 3 standard-library tooling is sufficient for the final CSV/JSON integration and validation pipeline; it has no third-party runtime dependency. During the authorized refresh, research-only PyArrow 26.0.0 was installed in a separate temporary virtualenv outside the repository to read source Parquet as inert data; this is not a project dependency or execution of dataset code. No credentials, cloud account, cloud access, or paid service is required. Do not place secrets in the repository; `.env.example`, if later needed, must contain examples rather than real credentials.

Source Bash commands are data, never instructions to execute. Do not run, source, evaluate, or paste collected examples into a shell, including during validation. Future checks must inspect records as text. Researching a sandbox policy does not authorize executing samples in a sandbox.

## Research requirements before collection

Each researcher must provide evidence for their assigned risk slice rather than assuming that source availability implies suitability:

- Research relevant sandbox policies and restrictions, citing the exact policy, retrieval date, and applicability to the intended use. Distinguish documented policy from inference; do not test policies by executing commands.
- Identify verified agent incidents with primary-source evidence where attainable. Record what actually happened, what command or behavior is supported by the evidence, and any uncertainty. Distinguish verified events from hypothetical scenarios, demonstrations, or unsourced reports.
- Assess attainable volume by source and risk/category, including expected usable records after duplicate removal and review. Identify coverage gaps and access or licensing limitations.
- Supply collection-time estimates, explicitly labeled **estimate**, with assumptions, method, and expected research, annotation, review, and integration effort. Separate estimated yields and time from observed counts and elapsed time. Do not promise unsupported volume or precision.
- Record exact sources and traceable evidence in the source ledger when collection is authorized. Preserve the distinction between sourced, transformed, and synthetic material.

The subsequent ingestion assignment authorizes these activities under the unchanged safety boundary.

## Agent handoff sequence

1. **Researcher per risk:** the supervisor assigns one owner per risk slice and sets boundaries before work begins. Each researcher hands off source evidence, feasibility and timing estimates, candidates, and unresolved questions using the governing schemas.
2. **Annotation and counterexample review:** reviewers check category/risk/class labels, severity, contextual ambiguities, and benign or yellow-zone counterexamples. Preserve pairing and provenance links; unresolved decisions go into `data/review/pending.jsonl`, not silently into the accepted set.
3. **Single integration owner:** one owner reconciles review decisions, duplicates, shared ledgers, transformations, counts, and taxonomy coverage, then produces the final root deliverables. Researchers must not concurrently rewrite final artifacts.
4. **Independent QA:** an owner independent of integration checks the deliverables against `AGENTS.md`, the source task, provenance, paired examples, reported counts, and documentation. Dataset Bash remains unexecuted. Findings return to the integration owner for correction before supervisor acceptance.

## Root ingestion deliverables

The authorized collection produces [`commands.csv`](../commands.csv) and the completed dataset-card [`README.md`](../README.md) at the repository root. The card reports actual accepted counts, deficits and verification limits; supporting files do not substitute for these deliverables.

The final `README.md` dataset card must include:

- **Title and language:** dataset title and an explicit Bash designation.
- **Composition and counts:** total size and counts by category, risk, and class, including yellow-zone coverage and utility coverage. Use actual final counts, not planning estimates.
- **Sources and processing:** exact sources, source identifiers/links, acquisition details, all transformations and sampling procedures, and the exact `random_state` where applicable; explain when randomness is not used.
- **Synthetic material:** identify every model used to generate synthetic records, its relevant version, generation method, and the synthetic contribution; explicitly say if no synthetic records exist.
- **Severity distribution:** actual counts and the severity scheme used.
- **Version and date:** dataset version, collection date, and release date.
- **Limitations:** source/access limitations, selection and annotation biases, uncertainty, and restrictions on interpretation or use.
- **Taxonomy coverage and deficits:** coverage of the required CAT-3 taxonomy, underrepresented or missing areas, and any unresolved deficits without claiming unsupported completeness.
- **Provenance and pairs:** explain record-level provenance, source/transformation lineage, and how counterexample or other required pairs are represented and linked; account for missing or rejected pairs.

Keep the final card consistent with `commands.csv` and the completed ledgers. No section should imply that planned research, estimated counts, or unperformed QA has already occurred.

Current audit entry points are [refresh verification](../data/review/refresh-verification.json), [independent refreshed QA](../data/review/refresh-final-qa.json), [integration decisions](../data/review/integration-decisions.json), [Keenable research log](../research/keenable-refresh.md) and [component attribution/license packaging](../research/attribution.md). Actual inert integration and separate validation passed for 250 records, and 15 tooling tests passed. Independent refreshed QA returned `pass_with_disclosed_limitations`, with no blockers or required corrections, after checking the final data, card, attribution and mentor samples and running one inert validator. This does not establish live command safety, full semantic uniqueness, legal ownership or complete PII absence. The earlier `data/review/final-qa.json` covers the historical 92-record release only.
