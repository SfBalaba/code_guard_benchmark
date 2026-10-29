# CAT-3.2 Keenable expansion research

Retrieved 2026-10-29. Commands are inert source data: no command field, cloud/container/Kubernetes/DB client, downloaded program or source script was executed. Only standard-library HTTP retrieval and inert JSON/CSV/HTML parsing were used. No tests, builds, linters, formatters or final validators were run; Main owns final verification. No executable source files were added, so the no-comments source-code linter is inapplicable.

## Current target and observed proposals

The current user correction in `docs/target-revision.md` is **250 total across all five risks**, not 250 per risk. There is no worker quota. The prior shard's per-risk deficit belongs to the superseded target.

`expansion-candidates.jsonl` contains **23 candidate proposals: 14 ask/high dangerous rows and 9 allow/low metadata counterparts**. Eight dangerous rows recover canonical pending CAT-3.2-101–108 and are not additional distinct dangerous commands. Thus there are **15 newly proposed distinct commands plus eight proposed recoveries**, subject to Main's global deduplication, license notices and independent admission review. No worker-assigned accepted rows and no claim of reaching the global target. No synthetic expansion, resource renaming or flag-combination construction was performed.

The proposals add kind, k3d, minikube, kOps and OpenShift `oc` deletion semantics, plus all-type names-only inspection and independently sourced RBAC/Secret summaries. A local cluster is not presumed disposable, and neither tutorial cleanup prose nor the absence of a production name establishes authorization, backups or isolation.

## Pending resource-kind recovery

An actual Stack Overflow Bash answer supplies a complete loop that discovers resource types, then runs `kubectl get` across all namespaces with JSONPath restricted to `.metadata.name`. This does not output Secret/ConfigMap values or arbitrary custom-resource contents. It covers ConfigMap, CronJob, Ingress, RoleBinding, Role, ServiceAccount, Secret and ReplicaSet types when those APIs are available and access is permitted. It is a metadata preflight, **not** a full deletion simulation, authorization proof or guaranteed complete inventory: forbidden/unsupported types can fail, and the original output prints resource type/name, not each object's namespace. No namespace flag/name was invented or substituted. Its all-namespace selection includes each dangerous command's explicit namespace.

Mapping of original pending IDs to proposed replacement IDs:

| Original | Replacement | Resource | Counterparts |
| --- | --- | --- | --- |
| CAT-3.2-101 | CAT-3.2-301 | ConfigMap | CAT-3.2-300 |
| CAT-3.2-102 | CAT-3.2-302 | CronJob | CAT-3.2-300 |
| CAT-3.2-103 | CAT-3.2-303 | Ingress | CAT-3.2-300 |
| CAT-3.2-104 | CAT-3.2-304 | RoleBinding | CAT-3.2-300, CAT-3.2-321 |
| CAT-3.2-105 | CAT-3.2-305 | Role | CAT-3.2-300, CAT-3.2-320 |
| CAT-3.2-106 | CAT-3.2-306 | ServiceAccount | CAT-3.2-300 |
| CAT-3.2-107 | CAT-3.2-307 | Secret | CAT-3.2-300, CAT-3.2-322 |
| CAT-3.2-108 | CAT-3.2-308 | ReplicaSet | CAT-3.2-300 |

All replacement/counterpart edges in the expansion shard are reciprocal and use `CAT-3.2-expansion-resource-inventory`. Main must **replace/update the original pending proposals, not admit both copies**. Canonical records were not edited. The independent Role/RoleBinding `-A` summaries come verbatim from the official AWS EKS guide. The Secret summary comes verbatim from pinned Atomic Red Team upstream, discovered after Main forwarded an actual ShellRisk-Bench lead. It is default table metadata, not `-o yaml/json`; the upstream credential-discovery label is not a reason to relabel this command destructive or to pretend it dumps secret values. Dependencies/install commands were not collected or executed.

## Additional paired diversity

- kind: documented default-cluster deletion and actual `kind get clusters` list; no made-up cluster-name variants.
- k3d: README's literal uppercase `CLUSTER_NAME` example token retained exactly, paired with all-cluster listing; no substitution of a novel name. The list is the documented synopsis with only optional NAME/flags groups omitted.
- minikube: actual `delete --all` example versus no-flag current-profile deletion, paired with all-profile metadata listing. Different target breadth is substantive, not an alias. Bare delete and profile-list are exact synopsis normalizations with optional `[flags]` omitted; no extra flags introduced.
- kOps: exact `--yes` cluster deletion example and actual all-clusters-in-state-store inventory. Both use the same configured state store; neither invents a region or project override. Main should preserve its primary cluster-deletion categorization despite cloud resources being removed internally.
- OpenShift: actual same-project, same-label, same-`all`-category names-only read/delete pair. `all` is a resource category, not every API kind; `-o name` is output formatting, not dry-run. Broader `oc delete project blog` was seen but not proposed because a suitable actual same-project namespace inventory was not established in that article. Current master was inspected; a commit could not be retrieved after GitHub API rate limiting, explicitly recorded rather than invented.

## Keenable search log

The following are actual queries to `xd://mcp__keenable_search_web_pages`, with original pages fetched or raw original source inspected separately; search snippets alone support no proposals:

1. `public dataset terminal agent trajectories kubectl delete namespace helm uninstall Kubernetes commands Hugging Face benchmark`
2. `kubectl cheat sheet delete configmaps cronjobs ingress rolebindings serviceaccounts all get secrets metadata name`
3. `official documentation kind k3d minikube delete all clusters get clusters list commands`
4. `official kops microk8s rancher oc delete cluster reset get clusters command examples`
5. `site:k3d.io "k3d cluster delete --all" "cluster list"`
6. `"kubectl get" "configmaps" "cronjobs" "--all-namespaces" cheat sheet`
7. `"oc delete all --all" "oc get all" github`
8. `github "kubectl get configmaps --all-namespaces" "kubectl get secrets"`
9. `github "kubectl get rolebindings" "-A" "kubectl get roles"`
10. `github "kubectl get cronjobs --all-namespaces"`
11. `github rancher cli "clusters delete" "clusters ls"`
12. `github "kubectl api-resources" "get" "-o name" "--all-namespaces" list all resources`
13. `Hugging Face Kubernetes shell command dataset "delete" license synthetic`
14. `github "helm uninstall" "--dry-run" "--all"`
15. `site:github.com/openshift/openshift-docs "oc delete all" "oc get all"`
16. `"Kubernetes" "dataset" "Zenodo" terminal commands kops deletion`
17. `"eksctl get cluster --region" "eu-north-1"`
18. `"gcloud container clusters list" "--project=${PROJECT_ID}"`
19. `site:minikube.sigs.k8s.io "minikube profile list"`
20. `site:github.com/redcanaryco/atomic-red-team "kubectl get secrets --all-namespaces"`

The semantically broad first searches found rare public traces; narrower searches located original inventories and tools absent from the baseline. Zenodo results were metrics/log/robotics datasets rather than verified command corpora, so no command yield is claimed. Rancher searches were noisy; actual CLI README/license inspection established Apache-2.0 but no suitable complete deletion/list examples. Helm results supplied reference options, not concrete new complete commands; combining flags into fabricated examples was rejected. Existing chowmean CSV was re-parsed in memory: no matching all-namespace inventories for the eight resource families were found; commands were not rewritten to create them.

## Novel dataset inspection and provenance limits

| Source | Actual inspection beyond snippets | Terms/origin | Attainable contribution now |
| --- | --- | --- | --- |
| IBM ITBench-Trajectories | Pinned API/card and actual Scenario-1/1 session: 88 JSONL records, zero `kubectl` mentions | CC-BY-NC-4.0; explicitly GPT-OSS-120B-generated ReAct trajectories over injected faults, not human incident logs | 0 proposals; restrictive terms, model/prompt lineage and task alignment unresolved; no raw session retained |
| yoonholee/terminalbench-trajectories | Pinned API/card plus actual rows 0–2 via datasets-server, all adaptive-rejection-sampler; no `kubectl delete` | Card declares Apache-2.0; agent/model fields include claude-opus-4-5-20251101; upstream task terms not fully established | 0 proposals; 52,104 card trajectories are not CAT-3.2 yield; source-held model generation not silently called real |
| K8sAIOps/kubernetes_operator_dataset_1k | Pinned API file listing and actual rows 0–99; instruction/type/output; potential broad-deletion matches at row indices 4, 15, 84 | No README/card/license metadata found; upstream generation unspecified | 0 proposals; earlier inaccessible lead is now record-accessible, but unknown terms still block retention/admission |
| K8sAIOps/kubernetes_operator_3b_1.5k | Pinned API file listing, README/Parquet presence | No cardData/license established | 0 proposals; no actual command acceptance evidence |
| NexusNeuralNet/devops-kubectl-v1 | Pinned API/card and actual rows 0–99; prompt/response; no selected broad-deletion/uninstall matches | License absent; prompt/response origin unestablished | 0 proposals; 34,535 train + 349 test metadata counts do not imply useful unique commands |
| Atomic Red Team via parent ShellRisk discovery | Independently inspected exact pinned upstream Markdown and MIT license, then extracted only the metadata summary | MIT; existing public test command, not a new model rewrite; benchmark aggregation license not substituted for source license | 1 independent Secret metadata counterpart |

The metadata and inspection outcomes, not restricted/unknown-license dataset bodies, are recorded in `expansion-sources.jsonl`. No unknown-terms raw session/row material was persisted. Parent separately reports synthetic provenance/bias and restrictive TerminalWorld training notices; those reports are not worker-independent inspections and do not support rows here.

## Terms and retained evidence

Exact revision/source locators, retrieval date and source-specific terms are in `expansion-sources.jsonl`. Permitted command excerpts only are in `data/raw/e2-command-excerpts.jsonl`; complete inspected license notices and attribution are in `data/raw/e2-license-notices.txt`. Existing recovered command provenance remains r2-hf, not falsely reassigned to a new dataset. Generated reference documentation means CLI-document generation, not an asserted LLM origin.

Kubernetes kind **site** content is CC BY 4.0, not the root Apache license. AWS EKS guide and Stack Overflow answer are **CC BY-SA 4.0**: retain source attribution, license links, modification disclosure and share-alike for adaptations; these rows must not be represented as blanket Apache-2.0. k3d/Atomic are MIT; minikube/kOps/OpenShift workshop are Apache-2.0. Main owns final redistribution notices and global licensing integration.

MicroK8s command reference was actually inspected: reset removes resources/authentication/services/pods, optional storage destruction is material, status is a metadata read. However Canonical legal navigation did not establish a positive license for the separately hosted documentation; repository Apache license cannot simply be applied to that page. It remains a source-ledger review lead, with no raw page/commands persisted in candidate artifacts. No fake microk8s pair was admitted solely to diversify utility counts.

## Existing blockers preserved

`expansion-pending.jsonl` explicitly keeps these out of default admission:

- CAT-3.2-001 kube-system namespace deletion is blocked by default NamespaceLifecycle admission. No guessed bypass or source environment was added. Its existing safe namespace-list row may be reused independently elsewhere, but this command is not claimed to perform successful deletion.
- CAT-3.2-019/020 config-file deletion fixes eu-north-1, while existing unqualified eksctl inventory does not prove region match.
- CAT-3.2-022 GKE deletion explicitly overrides project with PROJECT_ID, while unqualified list uses configured project. No constructed `--project`/`--region` command or guessed environment fixes this.

These are distinct from the eight recovered resource-kind pair gaps. Rollout restart and single-pod deletion remain context-sensitive; no safety claim was invented. No verified agent-caused cluster deletion incident was established by these sources. Main retains ownership of global policy/incident findings.

## Volume, estimates and handoff

Observed useful result is 23 proposals including 8 recoveries, not an arbitrary 30–50-row quota. The verified sources do not justify additional renamed resources, cosmetic aliases, dry-run flag combinations or hundreds of examples. **Estimate:** further source-term resolution, broad-trace sampling and scoped managed-cluster inventory research could produce 0–15 more distinct rows in 2–4 research hours plus review; this is not measured elapsed time, guaranteed yield or a commitment to synthesis. Restricted/unknown-license corpora can remain zero-yield regardless of size.

Main should review these proposals, reconcile replacement IDs against originals, preserve reciprocal pairs and source-specific licenses, and run the final inert schema/provenance/enum/pair/duplicate checks after all shards land. No split is constructed and no leakage-test claim is made. No dataset command was executed.
