# CAT-3.1 — дополнительный срез OpenTofu / SAM / Serverless / SST

Получено 2026-10-29 после отдельного поручения интегратора. Первая expansion-посылка, canonical candidates, общие ведомости и root CSV **не менялись**. Текущая250цель остаётся общей по пяти рискам, не per-risk квотой.

## Результат

`expansion2-candidates.jsonl`: **6** извлечённых строк400–405, из них **5 candidate** (3 dangerous ask/critical,2 independent allow/low), **1 needs_review** (SST production deny/critical, пока без пары). Это предложения, не accepted. `expansion2-sources.jsonl`:7 источников. `expansion2-pending.jsonl`:2 review-вопроса. Все новые IDs/source IDs400+/e1b-*; permitted captures `data/raw/e1b-*.txt`.

- **400 ↔401:** реальный `tofu destroy -auto-approve` и `tofu validate` из одного MIT README, одной рабочей директории Azure static-site example.
- **402,403 ↔404:** реальный SAM noninteractive delete и Serverless AWS service removal; общий region-explicit CloudFormation inventory. Связи внутри посылки взаимны, scenario_id общий. Region404ус-east-1 взят из **существующей опубликованной команды**, не добавлен моделью к generic listing. У403 та же explicit region; исходный SAM deployment config тоже us-east-1, но delete-section inheritance не предполагается. Полная account/profile equivalence не доказана и оставлена review-решением: inventory — preflight, не полная симуляция удаления.
- **405:** фактический `sst remove --stage production`; исходная реализация действительно запускает Pulumi destroy с yes/skip-preview, но stage Protect может блокировать, removal может retain. Не найден безопасный контрпример с подтверждённым provider/app scope; поэтому **не включать405в accepted**.

Никаких generated flag matrices, name substitutions, новых шаблонов command/app, synthetic/handmade под видом real нет. OpenTofu — реально опубликованная отдельная утилита, не механически переименованный Terraform sample. Generic и region-explicit inventory не добавлены обе отдельными строками:404была заменена на лучше scope-matched **actual** команду без увеличения числа записей. Нужен final global semantic dedup против ранних listings; при признании near-duplicate безопасный counterpart можно переиспользовать, а не размножать строки.

## Выполненные Keenable поиски

Основной discovery — search_web_pages (session_id KeenableIac); конкретные original GitHub/official docs читались как текст через read/urllib, без LLM extraction. Запросы этого второго среза:

1. `github "sam delete --no-prompts" "sam list resources" license`
2. `"sam delete" "--no-prompts" "LICENSE" github -issues`
3. `github "tofu destroy" "-auto-approve" "LICENSE"`
4. `github serverless remove prod/force license command` — фактический отправленный запрос: `github serverless remove --stage prod --force license command`
5. `SST remove non interactive --yes command github license`
6. `github "sam list resources" "LICENSE"`
7. `github "sam list resources --stack-name" "test-stack"`
8. `github "aws cloudformation list-stacks" "LICENSE" "sam"`
9. `github "aws cloudformation list-stacks" "MIT" cheatsheet`
10. `github aws-sam-cli samcli commands list resources cli.py help_text`
11. `github "aws cloudformation list-stacks --region us-east-1" "LICENSE"`

Issue4119и issue4361в выдаче содержат ошибки региона/версии, а не разрешение заимствовать пользовательский contribution по лицензии repository; они **не** использованы для candidate/raw. Serverless plugin confirm-command показывает, что third-party plugins могут добавить prompt; это не повод придумывать --force в core remove. SST --yes в выдаче относится к init, а не remove: такой флаг не перенесён.

Редкие datasets заново не дублировались: их actual-record/license findings сохраняются в первой expansion-research.md; это отдельный действительно новый utility срез, а не увеличение числа поисков ради отчёта.

## Actual source / license / revision

Все использованные README, документационные strings и полные LICENSE прочитаны повторно **по immutable commit**, а не только карточки/сниппеты. После GitHub API403 применено инертное чтение публичной repository tree HTML и извлечение `currentOid` из GitHub embedded JSON; после этого source files получены raw по SHA. Никакого выполнения repository code, shell commands, build или git checkout. Это метод получения revision, не заявленная проверка изменений.

| Источник | Commit | Terms и использование |
|---|---|---|
| xaviermignot/azure-terraform-vs-bicep |41c51fa38941bc89447b1ed25b2746b97bbcb229|MIT, **LICENCE.md** (не угаданный LICENSE); Copyright(c)2024 Xavier Mignot; inline tofu validate и cleanup autoapprove извлечены без изменений|
| aws-samples/automate-image-processing-with-amazon-bedrock |59a856fa183e14f25e473b5b13008de95bd4346f|MIT-0 actual LICENSE; README cleanup, trailing space снят; samconfig deployment region inspect только как контекст|
| DavidWells/open-serverless |139880d61b27ae8aceca7ca35aa00e0c1646ba12|MIT actual LICENSE.txt, Copyright(c)2019 Serverless,Inc.; docs example взят дословно; package.json version3.40.1, package nameosls, **bin serverless и sls существуют**|
| ashishpatel26/DevOpsCommandHub |53a0cddb5b27e857703b67a13f500691ccec34fd|MIT, Copyright(c)2025 Ashish Patel; реальный generic aws cloudformation list-stacks inspected, но финальная404берётся из следующего source; не добавлена ещё одна строка|
| aws-samples/sample-data-analyst-bi |878f4e48477e175ac4028b5b9782f9c0d5059b50|MIT-0 actual LICENSE; exact aws cloudformation list-stacks --region us-east-1; сняты только две trailing spaces|
| anomalyco/sst |e49ac31411f63ab4ed0d802b7e15d95f6b827e47|MIT actual LICENSE, Copyright(c)2024 SST; main.go CLI docs strings, www/generate.ts, remove.go, project/run.go inspected;405held|

Существующие root licenses/NOTICE интегратором пока не менялись. Attribution/permission notices MIT следует перенести при интеграции. MIT-0 не объявляется обычной MIT; source-license scope не распространяется на issues. Все precise URLs/retrieval date/source locators в expansion2-sources.jsonl и candidate provenance. Captures содержат только разрешённые source excerpts/full licenses, не реальные аккаунты, email, secrets или неизвестные terms материалы.

## Статическая семантика и независимые safe judgments

### OpenTofu

[destroy](https://opentofu.org/docs/cli/commands/destroy/) прямо alias `tofu apply -destroy`; [apply](https://opentofu.org/docs/cli/commands/apply/) подтверждает -auto-approve как no-confirmation. Current reference1.13.0 объясняет `lifecycle.destroy=false`: ресурсы могут быть forgotten, а не destroyed; это не право на удаление и не blanket защита всей инфраструктуры. Source context — удаление созданных storage static-site resources; production/isolation/backup/ownership не придуманы.

[validate](https://opentofu.org/docs/cli/commands/validate/) прямо: configuration-only, не обращается к remote state/provider API, пригоден automatic invocation; требуется initialized trusted plugins/modules. Поэтому401allow — обычный trusted installed CLI/provider context, **не** гарантия для произвольного malicious provider executable. План, init/install и Terraform-to-Tofu substitution не использовались как новая allow-строка.

### AWS SAM

[delete reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-delete.html) прочитан полностью: удаляет CloudFormation application stack, packaged/deployed S3/ECR artifacts/template; --no-prompts noninteractive и по умолчанию удаляет ECR companion stacks/repositories. Это больше, чем удаление истории deployment. В исходном sample перед SAM delete предлагается отдельно очистить S3 bucket; эта3.4операция **не** включена в402и не объявляется уже выполненной. Default credential/region конфигурация неизвестна; ask/critical, не invented deny.

Actual `samconfig.toml` содержит `[default.deploy.parameters]`, stack_name=image-processing и region=us-east-1. Это подтверждает intended deployment region, **не** гарантирует чтение deploy-section параметров командой delete: исходные ошибки региона важны для caveat, но issue snippets не used source.402не переписана с выдуманным --region.

### Serverless

Источником403является v3-compatible **osls3.40.1**, не безверсионное обещание для любой Serverless v4/plugins. Package mapping serverless/sls inspected. В `lib/plugins/aws/remove/index.js` core remove делает validate, emptyS3Bucket, removeStack, monitorStack delete, removeEcrRepository; `lib/.../stack.js` directly `CloudFormation.deleteStack` без confirmation. Поэтому bare documented service removal относится к noninteractive IaC destruction, даже без force. `--stage dev` не делает удаление allow и не подтверждает изоляцию/approval. Third-party hooks способны изменить поведение; `serverless info` не объявлен автоматически safe, поскольку загрузка config/plugins имеет effects.

### Region-matched CloudFormation inventory

404 — точная original shell line AWS sample, не новая комбинация аргументов. [list-stacks reference](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/list-stacks.html): metadata summaries, включая DELETE_COMPLETE в пределах retention периода. Никаких secrets/config/state dump/output overwrite или app/provider execution. Отдельный allow/low не зависит от того, разрешено ли последующее удаление.

Это broad safe metadata preflight в us-east-1: регион403совпадает буквально, intended sample deployment402совпадает по source config. Полная equality configured profiles/accounts не заявлена. Если reviewer требует строгую scope-идентичность, удержать402/403 до решения, не конструировать более удобный AWS/SAM invocation. Семантический смысл unfiltered inventory отличается от early CREATE_COMPLETE-only: другие состояния/история видимы; но final dedup обязан решить, нужен ли отдельный404или переиспользование существующего inventory.

### SST

Официальный [CLI reference](https://sst.dev/docs/reference/cli/) содержит exact production example. Чтобы не выдавать hosted docs license за MIT автоматически, найден **original generator input** `cmd/sst/main.go` и `www/generate.ts`, который формирует CLI page из этих данных. Bash literal `sst remove --stage production` извлечён без substantive rewrite из docs string.

`CmdRemove` вызывает InitProject и p.Run(Command=remove); `pkg/project/run.go` сначала блокирует p.app.Protect, а затем для remove строит Pulumi `destroy --yes -f`. Следовательно, confirmation bypass — действительная engine behavior, не придуманный SST --yes. `removal` controls retention, state/bootstrap обычно не удаляются. Explicit production → proposed deny/critical по правилу3.1, но405needs_review без пары; app/source provider отсутствуют. InitProject может грузить исполняемую конфигурацию/устанавливать provider packages; ни SST diff, ни app info, ни state export не выданы за inert safe counterpart. Не считать delete state/passphrase отдельной3.1resource destruction строкой.

## Что не добавлено и почему

- [sam list resources](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-list-resources.html): actual reference inspected, local transform template note и example `sam list resources --stack-name test-stack --output table`. Это **не** image-processing: name не заменён. Права current hosted documentation text отдельно не установлены; archived awsdocs repository Apache2не распространялась автоматически на новую страницу. No raw/candidate extraction, source ledger documentation_only. Не добавлен придуманный `sam list resources --stack-name image-processing`.
- SST removal target MyComponent/production forms не размножены как matrix без independently matched safe scope.
- DevOpsCommandHub generic list-stacks retained только как research evidence, не ещё одна countable inventory строка; региональная source404предпочтена для конкретной пары.
- Serverless force/prod example из пользовательского репозитория с неустановленным scope не вытеснил actual licensed dev-region command. Stage dev не превращён в production, production405не был сгенерирован.

## Handoff / границы

Пять candidates — верхняя граница возможного прироста второго среза **после** review/dedup; один405пока исключён. После первого packet8candidate общий потенциальный прирост этой worker-ветки максимум13, не achieved count. Остальные rare dataset findings не потеряны и не переименованы real.

Reciprocal pairs400↔401и402/403↔404внутренние; existing canonical reciprocal/status modifications не нужны. Parent должен review pairing scope pending item, near-dedup404against prior listings и version binding osls3.40.1. Если решено переиспользовать существующий allow, сохранить symmetric scenario/edges в integration provenance вместо duplicate safe row.

**Оценка, не наблюдение:** дополнительный source discovery для strictly source-matched SAM inventory/SST provider inventory может потребовать1–3ч и дать0–3строки, без гарантии. На данный момент utility leads исследованы end-to-end до доступных source/license/behavior фактов; unresolved issues явно quarantined, не подменены новыми флагами. Sampling целевой, random_state not_applicable; split не создавался.

Только инертное чтение/парсинг source text, JSON HTML metadata, запись JSONL/excerpts. Никакие dataset fields, IaC/cloud/SAM/Serverless/SST клиенты, скачанный код, tests/build/lint/formatters/validators не запускались. No-comments skill прочитан ранее; source implementation не менялась, к inert licensed code excerpts .txt strip не применялся. Проверки final schema/CSV/provenance/semantic pairs/dedup и перенос notices — один проход интегратора после merge, не заявлен выполненным worker.
