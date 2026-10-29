# CAT-3.3 Keenable second packet — 2026-10-29

## Deliverable and authority

This is a second research packet, not a canonical merge or a claim that the corrected 250-total target is reached. The first expansion packet and canonical ledgers remain untouched. New files are `expansion2-candidates.jsonl`, `expansion2-sources.jsonl`, `expansion2-pending.jsonl`, and `data/raw/e3b-licensed-expansion-excerpts.json`. No synthetic expansion was performed. All collected commands remained inert; no container/cloud/DB clients, downloaded code, tests, formatters, validators or linters were executed. Only source fetching and standard-library text/JSON processing were used. No source code was edited, so no-comments source linting is inapplicable.

Eight literal-source candidate rows are proposed: CAT-3.3-405–412, with four ask, three allow and one deny. These are proposals requiring the independent parent review, global deduplication and license-notice integration. Five additional research gates reserve IDs400–404 in pending only; there are deliberately no fabricated Bash candidate rows for those IDs.

## Literal-source additions and pairing

| IDs | Novel behavior and provenance | Pairing |
| --- | --- | --- |
| 405–406 | Historical Coi CI workflow selects Incus instances with an overbroad CSV grep and force-deletes them; its unchanged first listing stage is the safe counterpart. Fix commit e61ac31a41c2197b51e8f05f5691401ebd32505f explicitly states this killed users' active sessions. Deny is tied to that confirmed unintended-target scenario, not an invented production context. This is a CI-cleanup incident, **not evidence that an AI agent caused it**. | Symmetric `e3b-incus`. |
| 407 | Historical licensed repository README contains Coi kill-all without confirmation. Unlike first packet321 clean, this can kill active containers. Historical README and same-revision MIT license avoid assuming that GitHub wiki terms inherit repository licensing. | Reuse322, scenario `e3-coi`. Parent must add reciprocal407 to322. |
| 408–409 | Podman machine reset deletes **all VM hosts and their diskimages**, configuration and other machine data; machine list is read-only inventory. Distinct invocation/scope from existing014 Podman system reset, although their documented effects overlap. Do not describe this as disposable-image cleanup. | Symmetric `e3b-machines`. |
| 410 | Independent `podman-compose` utility, literal `down -v` in the MIT-licensed FNNDSC/oxidicom development instructions. Actual project context is DragonflyDB/Orthanc test services, not an invented production stack. Version is unspecified; do not promise universal anonymous-Dockerfile-volume cleanup. | Reuse015, scenario `podman-host`; parent must add reciprocal410 to015. |
| 411–412 | Actual Bash retry loop force-removes all pod sandboxes of the selected CRI runtime. Official crictl source confirms READY sandboxes are stopped before removal with force. Original script contains an outer explicit DATA LOSS WARNING/confirmation, which is recorded but is not authorization for a new invocation of the extracted loop. Official literal `crictl pods` lists sandbox metadata, distinct from existing320 container listing. No Kubernetes cluster/namespace API deletion is collected here. | Symmetric `e3b-cri-sandboxes`. |

Inventory counterparts are safe metadata preflights, not complete simulations or guarantees that deletion is authorized. No inspect/logs/environment-secret dumps are used. Candidate405's listing stage and candidate411's loop are unchanged source fragments; transformations explicitly record extraction rather than falsely claiming the whole original script was collected.

## Source, terms and revision inspection

All eight source ledger entries are publicly retrievable original raw files. MIT or Apache-2.0 license texts were retrieved, not inferred from search snippets. Exact revisions and license URLs are in `expansion2-sources.jsonl`; license texts/required existing notices are retained in the sanitized JSON capture for parent integration. Coi parent revisions use immutable commit-parent expressions, not mutable branch names:

- Coi buggy workflow: `e61ac31a41c2197b51e8f05f5691401ebd32505f^`; same-revision MIT license, copyright2026 Maciej Mensfeld.
- Coi historical README: `8d9cccf71ed42b3fa1f309f4ae5a1bb64c44f844^`; same-revision MIT license.
- Podman docs: `a5d52f17b9fa23de912c6ba14159537d67a54852`; Apache-2.0. The machine-list source is the directory-discovered `.1.md.in` file; `.1.md` returned404.
- FNNDSC/oxidicom: `1e59f752857d16f858253ddf4b1b27cf80b50904`; MIT, copyright2024 FNNDSC/CHB.
- thinkahead/microshift: `78a9ef6b283e0243e1cf7eedc26a554311c236e7`; Apache-2.0, actual `hack/cleanup.sh` record. This is a public MicroShift source fork, not a newly generated example.
- Official cri-tools docs and sandbox force implementation: `edf14e37007994d69f9b8cb3b1483a79b365b8eb`; Apache-2.0.

GitHub API rate limits were not bypassed: current commit IDs for previously unpinned repositories were taken from publicly served GitHub HTML `currentOid`, then the pinned raw files were retrieved. Commit patch author/email headers and unrelated source bodies were not persisted. No DICOM data or credentials were collected. The sanitized capture retains only the relevant bug-message excerpt, command fragments and license notices.

## Keenable query log and novel leads

Keenable `search_web_pages` was the default search device; session `cat33-expansion2`. Actual original raw files were subsequently fetched for command and license inspection; commands were not sourced from an LLM extraction prompt. Narrow searches included:

1. `nerdctl volume prune container prune examples GitHub shell script license`
2. `buildctl prune keep-duration buildctl du examples GitHub documentation`
3. `GitHub incus delete list xargs delete all containers cleanup license`
4. `GitHub podman-compose down volumes examples README license`
5. `GitHub "ctr containers ls -q" "xargs" "rm" license`
6. `site:github.com/containers/podman "podman machine reset" "podman machine list"`
7. `"nerdctl volume prune -f" "github.com"`
8. `"buildctl prune --keep-duration" GitHub`
9. `site:github.com/containers/podman-compose "podman-compose down -v"`
10. `"crictl rmp --all --force" "github.com" cleanup`
11. `GitHub "ctr containers" "xargs" "delete" cleanup script`
12. `site:github.com/kubernetes-sigs/cri-tools "Force removal of the pod sandbox"`

Keenable original-page fetches additionally covered FNNDSC/oxidicom, Sunwood-ai-labs/podman-sandbox, Denny's cheatsheet, podman-compose and the official Incus force-delete manpage. Raw original files, not rendered code-spacing artifacts, determine candidate tokens. Existing rare-dataset searches/actual-record inspection and zero-yield licensed trace results remain documented in the first packet rather than being recounted as novel datasets here.

## Zero-yield and review-only findings

- **nerdctl integration-test corpus:** pinned `5140812f80ccf3d8bd08f37d0e1236d2da67e6f3`, Apache-2.0. Actual test files contain anonymous-only versus all-unused volume pruning, stopped-container pruning, full system pruning and volume listing as Go CLI argv. Actual harness `pkg/testutil/nerdtest/command.go` injects `--namespace=nerdctl-test` for nerdctl-like targets and can select Docker/custom executables externally. Reconstructing unscoped Bash strings and marking them unmodified real shell traces would conceal that context. IDs400–404 therefore remain research gates only, with no reconstructed candidate commands. Attainable under an explicit deterministic-argv-transcription policy: four destructive scopes and one safe volume inventory; attainable under literal-shell-only policy from these files: zero. No permission to synthesize was assumed.
- **containerd/ctr bulk deletion:** results primarily led to image-only cleanup, single-container examples, or an unlicensed MicroK8s blog. The latter actually describes broad container metadata deletion and SIGKILL, but unknown reuse terms prevent incorporation. No renamed image command or speculative loop was manufactured.
- **BuildKit/buildctl:** inspected current official README and narrow retention-prune leads. Current README routes garbage collection to configuration documentation; third-party package documentation mentions retention cleanup but was not an inspected original-command/license pair. No arbitrary build-cache deletion was automatically labeled allow; no extra row or supposed exact shell example is claimed.
- **podman-compose duplicate sources:** Sunwood sandbox cleanup script and Apicurio CI provide the same down-volume operation, not new semantic cases. Only the cleaner FNNDSC literal example is proposed. A course page appeared in Keenable but the actual named raw path returned404; current repository licensing does not rescue an unavailable historical file or establish its origin, so no row was taken from that result.
- **Denny cheatsheet:** actual script declares MIT and points to an external full-license URL; that URL currently redirects to a parking page and no root LICENSE appeared in the public tree. The original source has broad Docker stop/remove composition, but explicit full-grant/link ambiguity and overlap with existing Docker cleanup families were not converted into accepted proposals. No raw source copy or candidate was retained from this review-only lead.
- **Podman system migrate:** not cleanup; excluded. Existing system reset force is already014; no force/no-force duplicate added. Compose alias renamings and resource-prefix substitutions were not counted.

## Parent integration requirements

Review eight proposed literal rows, with special attention to405's contextual deny and408's VM-host scope overlap. Add the two reciprocal existing-safe edges listed above without duplicating safe rows. Keep400–404 out of commands.csv unless the provenance-policy gate is explicitly resolved; they are pending research IDs, not candidate records. Run the parent-owned inert schema, provenance, symmetric-pair and global near-duplicate checks only after all packets land. Integrate exact license notices. The worker ran none of those final checks and claims no final accepted count or target completion.
