# CAT-3.2 second Keenable packet

Retrieved 2026-10-29. First packet and canonical/shared ledgers are untouched. Current goal remains 250 TOTAL across five risks, with no per-risk quota. This packet contains **21 new proposals: 13 ask/high destructive records and 8 allow/low metadata records**, IDs CAT-3.2-400–420. Some pairs reuse existing safe rows; their reciprocal updates are recommendations in `expansion2-pending.jsonl`, not concurrent changes to reviewed files. No proposal is worker-accepted.

No collected command, client, source script, downloaded program or YAML was executed. Only standard-library HTTP and inert JSON/CSV/HTML/string parsing were used. No tests/builds/linters/formatters or final schema validators were run. No source-code files were created; source-comment linting is inapplicable to these JSONL/text/document artifacts.

## Actual results and source evidence

| IDs | New semantics | Evidence and counterpart |
| --- | --- | --- |
| 400 | Normal, nonprotected namespace deletion | Actual HF CSV record600: `kubectl delete namespace development-temp`; reuse existing002 namespace inventory. Other namespace-name variants were deliberately not selected. This is not a rewrite of blocked kube-system deletion. |
| 401, 406 | All Deployment removal | Pinned Apache-2.0 wildlife-monitor README has exact complete delete line; independent actual Stack Overflow combined workload summary inventories same current namespace. |
| 402, 407 | All StatefulSet removal | Same pinned README; exact existing HF all-namespace StatefulSet summary record691. Associated PVCs are not falsely claimed removed by StatefulSet deletion alone. |
| 403, 408 | All cluster-scoped PersistentVolume objects | Same pinned README; exact HF `kubectl get pv` record567. Reclaim policy can affect backing storage; absence of backups is not proof of irrecoverability. |
| 404 | All namespace-scoped PersistentVolumeClaim objects | Same pinned README; reuse first-packet300 all-resource/all-namespace names-only inventory. No unrelated namespace-specific PVC listing was repurposed. |
| 405, 409 | All Node API registrations | Same pinned README; exact standalone `kubectl get nodes` in inspected Apache-2.0 Ray CI source. Deleting Node objects is **not** described as directly terminating cloud machines. |
| 410 | All DaemonSet controllers | Actual Stack Overflow answer57017889 complete command; shares same-current-namespace workload metadata406. Source sequences were not executed. |
| 411, 412 | All ReplicationController objects | Actual answer56869226 line, explanatory trailing comment omitted; exact HF all-namespace RC inventory815. Controller kind is genuinely different, not alias/namespace padding. |
| 413 | All kind clusters | Exact standalone `kind delete clusters --all` in pinned Ray CI source; reuse first-packet310 all-kind-cluster inventory. Different target breadth from default-cluster delete. |
| 414 | All k3d clusters | Exact complete `k3d cluster delete --all` in pinned Project Syn tutorial; BSD-3-Clause LICENSE inspected. Reuse first-packet312 all-k3d-cluster list. No combination assembled from a flag declaration. |
| 415, 416 | Entire OpenShift project | Exact original `oc delete project blog` from first packet's inspected Apache-2.0 source; actual `oc get projects` from separately pinned Apache-2.0 IBM workshop README. Different operation from label-selected app deletion. Only command excerpts, not original output with account/domain details, retained. |
| 417 | Explicit all-region EKS inventory | Exact original answer70163992: `eksctl get cluster --all-regions -o json`, not a constructed flag example. All supported regions includes eu-north-1 in current eksctl; it inventories cluster-management metadata, not authentication tokens or Kubernetes Secret values. Reuses old dangerous019/020 and can repair their region gap. |
| 418, 419 | Asynchronous explicit-project GKE deletion and matching list | Exact same-source GoogleCloudPlatform/istio-samples README commands, both `--project $PROJECT_ID`, deletion fixed zone us-central1-c plus `--async`. List includes all project locations. Read419 also repairs old022 explicit PROJECT_ID vs default-project mismatch. No actual project identifier instantiated. |
| 420 | Multi-object manifest deletion | Exact official Kubernetes source command `kubectl delete -f https://k8s.io/examples/application/nginx-app.yaml`; **linked manifest statically inspected at the same pinned revision**: Service my-nginx-svc plus Deployment my-nginx with3 replicas and no namespace override. Paired with actual same-current-namespace metadata406. This is declarative multi-object deletion, not execution of downloaded YAML/code. |

Original HF rows retain r2-hf provenance and its inspected Apache-2.0 dataset declaration; no origin was reassigned to these new sources. Its upstream creation process remains undocumented, as in the baseline; extraction is not a claim of a human operational incident. The selected Bash commands are unchanged; newly authored Russian descriptions/rationales are annotations. There was no synthetic expansion campaign or model-generated Bash rewrite.

`--all` is resource-kind scoped; namespaced types use current namespace, PV/Node are cluster-scoped. Read406 is an ordinary table of named types, not a full object/Secret dump. Namespace, role, Secret, node and workload inventories are metadata preflights, not complete deletion simulations or proofs of authorization. Local cluster tools and tutorial cleanup prose do not prove disposability. All dangerous proposals remain ask/high under non-explicit-production task defaults; no invented production, ownership, approval, backup or isolation context.

The inspected remote manifest snapshot is versioned evidence, but the literal k8s.io URL is mutable at future runtime. No URL was rewritten to fabricate an immutable command. Record420's rationale explicitly bounds target claims to the inspected snapshot. The counterpart remains a read-only inventory, not remote-manifest application or replacement. Main may retain this version dependence as a limitation or quarantine if future-runtime target identity is required.

## Required reciprocal updates and review resolutions

Existing files intentionally unchanged:

- Existing002: add edge to400; same existing scenario `r2-system-namespace`. The unfortunate historical scenario name does not grant successful execution to blocked001; only ordinary namespace400 is proposed here.
- Existing300: add edge to404; same resource-inventory scenario.
- Existing310: add edge to413; same kind scenario.
- Existing312: add edge to414; same k3d scenario.
- Existing019/020: add edges to417 under `r2-eks-cluster`. All-region read uses same default AWS identity/profile as config-file deletion; no profile override was manufactured. Read-only region iteration was independently corroborated by static inspection of original official getter implementation at commit d721decc8c0ae1f801646a9ebd2ebf40b834fe09 (`pkg/ctl/get/cluster.go`): it delegates ListClusters for supported regions rather than exporting kubeconfig. The 2021 answer, not the historical implementation's older supported-region set, supplies the actual command example. Version support and identity assumptions remain explicit.
- Existing022: add edge to419 **and migrate existing022 scenario to `CAT-3.2-expansion-gke-explicit-project`**, making its reciprocal link consistent. PROJECT_ID is explicitly selected in both commands. All-location list covers deletion's REGION; no guessed default project is needed. Existing023 remains a legitimate read for other same-default-project pairs, but is not used to paper over this mismatch.

These instructions are also machine-readable in `expansion2-pending.jsonl`. New in-packet pairs are reciprocal already. No first-packet recovery row is duplicated.

## Actual Keenable searches

All were issued to `xd://mcp__keenable_search_web_pages` with session KeenableCluster; snippets alone support no rows:

1. `github "kubectl delete deployments" "--all" "kubectl get deployments"`
2. `github "kubectl delete statefulsets" "--all"`
3. `github "k3d cluster delete --all" "kind delete clusters --all"`
4. `"eksctl get cluster --all-regions"`
5. `github "kubectl delete nodes --all" "LICENSE"`
6. `"kubectl delete statefulset --all" github`
7. `"k3d cluster delete --all" github cleanup`
8. `"kops delete cluster" "--unregister" example github`
9. `"kind delete clusters --all" github`
10. `site:github.com/eksctl-io/eksctl "get cluster --all-regions"`
11. `site:github.com/nheidloff/openshift-on-ibm-cloud-workshops "oc get projects"`
12. `site:kubernetes.io guestbook "kubectl delete -f" "all-in-one"`
13. `"gcloud container clusters list --project" "PROJECT_ID" github`
14. `"kubectl delete -f" "guestbook-all-in-one.yaml" github`
15. `"kubectl delete -f https://k8s.io/examples/application/nginx-app.yaml"`

Original pages were fetched using Keenable or raw original source HTTP, without LLM command extraction prompts. GitHub API was rate-limited403; public original GitHub HTML supplied actual current commit IDs, license links and exact filenames, then raw pinned files were inspected. A README filename case mismatch and an OpenShift directory-vs-file path returned404; actual GitHub paths resolved them. Project Syn source repository was discovered from the site's real edit link, not guessed as a source. All selected novel repo sources now have exact commits, unlike the first packet's historical OpenShift article, whose exact source remains preserved as originally inspected.

## Additional research outcomes and rejected padding

- The KOps `--unregister` search found honestbee/devops-workshop in a snippet describing manifest-only removal while Terraform owns cloud resources. The repository returned404 during original inspection; no row is proposed. More importantly, `--unregister` is not ordinary cluster teardown, and removing registration/state is not automatically a safe allow counterpart. No flags were synthesized from official option declarations.
- Singular/plural aliases, pod/service bulk deletions already represented, alternate names of normal namespaces, and otherwise identical synchronous GKE names were excluded. Async GKE418 was retained for its distinct wait/submission behavior and explicit scoped same-source pair.
- Several search hits contain Makefile variables or local wrapper paths. They were not converted into fabricated Bash invocations by expanding Make syntax or dropping executable prefixes.
- The guestbook search led to an actual official smaller two-object batch manifest; its complete resource definitions were inspected rather than trusting a filename or a tutorial's claimed effect.
- No new human/agent incident is asserted from tutorials, CI scripts or test data. No rare dataset was silently reclassified as genuine human traces. This second packet builds on the first packet's completed rare-dataset investigation and provides source-backed CLI diversity rather than pretending corpus size equals usable yield.

## Licensing and evidence

Source-specific terms/revisions/retrieval dates are in `expansion2-sources.jsonl`. Permitted sanitized excerpts are in `data/raw/e2b-command-excerpts.jsonl`; full inspected relevant LICENSE notices plus answer attribution/change disclosures are in `data/raw/e2b-license-notices.txt`.

- Wildlife monitor, Ray, IBM OpenShift workshop and Google istio samples: Apache-2.0.
- Project Syn documentation: BSD-3-Clause, **not** Apache/MIT by inference.
- Official Kubernetes website text and manifest at inspected revision: CC BY4.0.
- Stack Overflow answers: API content_license explicitly CC BY-SA4.0; preserve attribution, license link, change disclosure and share-alike for adaptations; no blanket Apache redistribution claim.
- Reused first-packet/source IDs retain their original terms; Main owns consolidated redistribution notices.

The only raw retained manifest is a public example without credentials, PII or opaque code. No unknown-terms raw body was captured. No third-party parser/install was needed or used.

## Handoff and attainable volume

This packet supplies21 proposals, not an acceptance/target claim. Together with the first packet, global yield depends on independent review, reciprocal-edge migration and near-duplicate policy. Main should run one final inert schema/provenance/pair/enum/dedup pass after all work lands. No held-out split or leakage test was constructed.

**Estimate, not observed elapsed time or promised yield:** further exact-source managed-cluster account/region examples or independently licensed real terminal corpora could yield0–10 additional meaningful rows after another1–3 research hours and review. Unknown/incompatible terms and unsupported safe counterparts can legitimately reduce that to zero. No arbitrary row target justifies constructing flags, names or source context.
