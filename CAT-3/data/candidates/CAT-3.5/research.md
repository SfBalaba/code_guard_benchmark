# CAT-3.5 — production deployment research

Retrieval date: 2026-10-29. Scope: existing public Bash command examples, no execution, no synthetic expansion. Commands and source snippets were treated as inert data. No cloud/container/database clients, downloaded code, source/eval, dataset commands, tests, builds, formatters or validators were run. Parent owns final static validation. No source-code files were edited, so no-comments source linter is inapplicable.

## Observed contribution and deficit

`candidates.jsonl` contains **15 proposals: 12 candidate + 3 needs_review**. The candidate subset is **8 ask/high dangerous records + 4 allow/low independent read-only counterparts** in four scenarios: Vercel release management (4), Netlify live-site deployment (4), LinkWork production Kustomize deployment (2), Ralph production rollback (2). There are **zero accepted records at worker stage**; integration/review must decide acceptance. If all 12 eligible proposals survive global deduplication and review, the actual target shortfall is **238 of 250**. Current final accepted deficit cannot be claimed smaller than 250 before parent integration. Three unresolved commands do not count toward eligible volume. No deny label is invented merely because deployment is mutating; the taxonomy default is ask/high and external approval is unknown.

Commands are extracted verbatim, including multiline continuations; only surrounding Markdown fences/comments are omitted. Descriptions and rationale are newly authored Russian annotations, not new commands. `source=real`, `seed=-` refers to extracted existing documentation examples, not evidence these commands occurred in an incident. No claims of agent-caused incidents are made. No sampling or random_state; manual relevance-driven selection, not random. No split was produced. Root README must document this and prevent example leakage if a split is later created.

Meaningful retained variation: Vercel ordinary production deploy, forced cache bypass, prebuilt upload; Netlify local build/deploy, remote build/deploy, conditional production-if-unlocked; Kustomize apply; Kubernetes revision rollback. Alias-only Vercel deploy forms, `--open` browser variation, resource renames, repeated rollout status and arbitrary flag combinations were not counted. Utilities: vercel, netlify, kubectl. Helm production install/upgrade are review-only. No supported obfuscated production deployment source was found; none fabricated.

## Separate Hugging Face search

Queries used:

- `site:huggingface.co/datasets "helm upgrade" "prod"`
- `site:huggingface.co/datasets "kubectl apply" "production" license`

First query returned weak/noisy matches including privacy/secrets corpora and an OpenTelemetry dataset. Secrets corpora were **not opened or retained** because they were irrelevant to licensed deployment pairs and could expose credentials. Search snippets were not adopted as source evidence.

Inspected [RELAI OpenTelemetry card](https://huggingface.co/datasets/relai-ai/opentelemetry-standard/blob/main/README.md): CC-BY-4.0 assertion, generated QA from OpenTelemetry docs; no actual production CLI records inspected. No contribution and no claim that underlying data contains none.

Inspected [DevOps/cloud card](https://huggingface.co/datasets/bernabepuente/devops-cloud-instruction-dataset/blob/main/README.md), [file inventory](https://huggingface.co/api/datasets/bernabepuente/devops-cloud-instruction-dataset/tree/main), and [actual dataset.jsonl](https://huggingface.co/datasets/bernabepuente/devops-cloud-instruction-dataset/blob/main/dataset.jsonl). Card asserts MIT and 99 entries, Qwen2.5-Coder 7B generator + DeepSeek-R1 1.5B validator. Actual record instruction `Write a bash script to scale a Kubernetes deployment.` supplies namespace `production` and command `kubectl scale deployment/my-app --replicas=5 -n production`. It is **not imported as real data**: upstream is synthetic, complete generation prompt is not supplied, and scaling-only versus code-deployment boundary needs decision. The source also contains many incomplete/malformed or non-Bash examples; no claim of 99 usable records. Observed eligible HF contribution: **0**; one explicit unresolved lead. Do not fabricate seed or regenerate a counterpart.

## Separate GitHub search

Queries used:

- `site:github.com "production" "kubectl diff" "kubectl apply"`
- `site:github.com "production" "deploy --dry-run"`
- `site:github.com "kubectl get deployments -n production"`
- `site:github.com "helm upgrade" "production" "helm status"`
- `site:github.com "vercel --prod" "vercel inspect"`
- `site:github.com "kubectl" "production" "rollout status" "set image"`
- `site:github.com "helm" "prod" "--dry-run=client" "--hide-secret"`
- `site:github.com "helm status" "-n production"`
- `site:github.com "kubectl apply" "prod.yaml" "--dry-run=client"`
- `site:github.com/netlify/cli "netlify deploy --prod" "netlify status"`
- `site:github.com "firebase deploy --project production" "firebase hosting:sites:list"`

Search results only identified leads; accepted-proposal evidence comes from inspected actual files and license text:

| Inspected source | Reuse evidence / revision | Observed eligible proposals |
| --- | --- | ---: |
| [Vercel official plugin deployment guide](https://github.com/vercel/vercel-plugin/blob/9beca3cc1384a98d6bdd81acd1a22f942315b091/skills/deployments-cicd/SKILL.md) | [Apache-2.0 notice](https://github.com/vercel/vercel-plugin/blob/9beca3cc1384a98d6bdd81acd1a22f942315b091/LICENSE), Copyright 2026 Vercel, Inc.; API detector NOASSERTION does not override actual explicit text | 4 |
| [Netlify CLI deploy](https://github.com/netlify/cli/blob/main/docs/commands/deploy.md) and [status](https://github.com/netlify/cli/blob/main/docs/commands/status.md) | [MIT](https://github.com/netlify/cli/blob/main/LICENSE), Copyright (c) 2016 Netlify; main retrieved 2026-10-29, commit lookup returned HTTP 403, no fabricated commit pin | 4 |
| [LinkWork deployment guide](https://github.com/momotech/LinkWork/blob/993fd9273ca416c521a12632a91a00f8cc073e95/deploy/k8s/README.md) | [Full Apache-2.0 license](https://github.com/momotech/LinkWork/blob/993fd9273ca416c521a12632a91a00f8cc073e95/LICENSE) inspected at same revision | 2 |
| [Ralph production guide](https://github.com/lloydchang/mikeyobrien-ralph-orchestrator/blob/196220bd4eb2216f0df7a44238a593d2200057bc/docs/deployment/production.md) | [MIT](https://github.com/lloydchang/mikeyobrien-ralph-orchestrator/blob/196220bd4eb2216f0df7a44238a593d2200057bc/LICENSE), Copyright (c) 2025 Ralph Orchestrator Contributors | 2 |
| [Cloud-Premises patterns](https://github.com/Cloud-Premises/kubernetes-production-patterns/blob/e9439e3d3fe5a31ffed1cfa935c43d9f52612ce8/README.md) | README itself explicitly licenses under Apache-2.0 and reproduces notice, Copyright 2025 Cloud Premises; inventory only README and referenced charts absent | 0; 2 review-only |

API `/license` HTTP 403 for Netlify/LinkWork was recovered through inspected repository file listings and actual raw LICENSE content; source accessibility is accessible. An attempted Vercel reference filename returned HTTP 404 and was not used. An attempted generated rollout-status documentation URL returned HTTP 404; official kubectl implementation was inspected instead. No inaccessible page supports a candidate. Exact locators and version caveats are in sidecars.

[SnowOps promotion runbook](https://github.com/sagar2395/snowopslabs/blob/main/docs/runbooks/R06-multi-env-promotion.md) was inspected: explicitly k3d/kind laboratory, so namespace env-prod is not hard proof of actual production. [Lumio phase-7 lab](https://github.com/wb-platform-engineering-lab/cicd-migration-lab-jenkins-to-gitlab/blob/main/phase-7-environments/README.md) is explicitly local Rancher Desktop, with placeholder workload and exercise approval gates. Both excluded rather than calling lab prod a dangerous operational production deployment. Their content is not copied into candidate rows. Other search leads (gists/issues/Firebase) were not promoted without inspected license+actual usable pair evidence.

## Independent counterpart safety and context

- **Vercel**: `vercel rollback status`, explicitly sourced as status-only, is not `vercel rollback`. [Official documentation](https://vercel.com/docs/cli/rollback) and [implementation](https://github.com/vercel/vercel/blob/main/packages/cli/src/commands/rollback/status.ts) confirm metadata polling, no rollback request. Related task is checking current production release/rollback state before making another deployment. It is not a proof the proposed release is correct or approved.
- **Netlify**: [status implementation](https://github.com/netlify/cli/blob/main/src/commands/status/status.ts) reads current account and linked-project metadata, does not build/deploy or execute application build hooks. It can display account name/email, team and project identifiers; no runtime output is captured and command has no external sink/redirection. This is a limited contextual read, not a secret dump or permission assumption. It errors if unauthenticated/unlinked instead of creating a deployment. Status of the current linked project is an independent preflight counterpart; it does not replace code diff or approval. `status:hooks` excluded because hook details may be sensitive.
- **LinkWork**: exact adjacent production Verify command `kubectl -n linkwork-prod get pods -w`. [Core get reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/) confirms table listing and watch. It reads pod status rather than manifests or Secrets and does not invoke workload hooks. Watch can run indefinitely; no timeout invented. Production is explicitly in source section, overlay path and namespace. Dev deployment was not assumed safe.
- **Ralph**: production explicitly established by guide introduction. The original rollback changes running revision, not resource deletion. Adjacent rollout-status command independently only reads/watches status, per [official source](https://github.com/kubernetes/kubectl/blob/master/pkg/cmd/rollout/rollout_status.go). It can wait indefinitely. The guide's unchecked backup/approval checkboxes are **not** evidence of backups or approval. Image update with historical `--record` remains review-only; it is not silently repaired into an invented extraction.

Every eligible dangerous proposal has an eligible read-only counterpart, with reciprocal IDs. Broader Helm get-all listing was deliberately not used to conceal absence of a release-specific safe pair. Pending records may be unpaired and must not enter final accepted CSV.

## Helm dry-run, kubectl admission and hooks investigation

[Current official Helm upgrade](https://helm.sh/docs/helm/helm_upgrade/) is version **4.3.1**, generated 15-Oct-2026; source project only says Helm 3.0+. **Do not transpose version-specific flags to older Helm.** It explicitly warns dry-run outputs all generated manifests including Secrets. `--hide-secret` hides Kubernetes Secret objects, not arbitrary secret text placed in other objects/notes. `--dry-run=client` avoids cluster connections; `--dry-run=server` requires them. [Template debugging docs](https://helm.sh/docs/chart_template_guide/debugging/) state server mode enables `lookup`. Post-renderers/plugins can execute code outside the cluster-persistence guarantee; arbitrary charts/renderers are not automatically safe. No invented `--hide-secret --no-hooks` combination is counted as a sourced safe command.

[Kubernetes API dry-run](https://kubernetes.io/docs/reference/using-api/api-concepts/#dry-run) is stable since **1.19** and guarantees no storage persistence/other side effects **under the admission contract**. Admission controllers with side effects fail the dry-run; custom webhooks must correctly advertise None/NoneOnDryRun and suppress effects for dryRun requests. This is not proof an arbitrary misdeclared webhook is correct. [kubectl apply reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/) distinguishes client printing without submitting object versus server submitting without persisting. Client dry-run is not a blanket claim of offline/no-authentication activity: API discovery/authentication may still happen. No Kubernetes Deployment workload hook is started merely by a nonpersisted API request, but admission webhooks are a separate execution surface. [kubectl diff](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/) uses YAML output, server would-be state, and external diff process (`KUBECTL_EXTERNAL_DIFF`); current reference has `--show-secrets`. Older versions and uncontrolled external diff/plugin settings require independent review. No generic diff/dry-run row is accepted without source production context and actual manifest/output evidence.

The actual LinkWork dev client-dry-run command remains a research lead, not allow: arbitrary manifests/renderer content were not audited; dev label is not proof. Plain production get-pods supplies the genuine safe pair instead. Helm source chart absent and precise safe examples lacking, so two deploy commands remain needs_review.

## Attainable volume and collection-time estimates

Observed yield is 12 review-eligible proposals, not 250. From already inspected sources, additional name substitutions/aliases would be padding. HF inspected source offers no immediate compatible hard pair. **Estimate:** another 4–8 hours of focused licensed repository research could locate roughly 10–30 additional meaningful pairs (20–60 rows), assuming new utilities and explicit production commands with separately sourced reads, not arbitrary dev/dry-run examples. This is an estimate, not measured yield or guaranteed availability. **Estimate:** 3–6 minutes/row for provenance, independent Russian annotation and side-effect review after source discovery; 1–2 hours for cross-shard deduplication/integration plus independent review of this shard. Achieving 250 real distinct CAT-3.5 rows may require several research days and additional source families; no extrapolated promise of reaching target. Deficit is deliberate and preferable to synthetic/near-duplicate expansion.

Shared single worktree uses parent branch feat/data_cat3; per-risk concurrent branch checkout was intentionally not performed, per parent direction. Parent handles sandbox-policy and verified-agent-incident research globally. This shard contributes no verified agent incident. All writes are confined to CAT-3.5 shard and r5-prefixed sanitized raw capture; shared ledgers/root artifacts untouched.
