# CAT-3.5 — второй пакет дополнительных утилит, Keenable

Дата: 2026-10-29. Этот пакет создан по отдельному указанию parent: `expansion-*` с IDs300–311 остаётся стабильным для reviewer/integration; новые материалы находятся только в `expansion2-*`, IDs400+, source IDs`e5b-*`. Первую выдачу не редактировал. Цель остаётся250 TOTAL, не250 для одного риска; это исследование, не добивка квоты.

## Результат и готовность к рассмотрению

**8 exact extracted proposals, все `needs_review`**: 5ask/high,3allow/low. **Новых готовых candidate сверх первого пакета —0**, accepted —0. Платформенная история или copyleft не замаскированы как снятые blockers. Все пары симметричны в sidecar, не требуют изменений канонических строк.

| Source | IDs | Что действительно получено | Открытое решение |
|---|---|---|---|
| [Deno official Classic docs](https://github.com/denoland/docs/blob/74beb7585f7e798fe0bc8d867295bff23fc2e38e/deploy/classic/deployctl.md) | 400 direct --prod,401 promote/redeploy existing version,402 production traffic + preview KV,403 deployment history | Прочитан actual original Markdown, rendered official page и полный MIT LICENSE, Copyright2018–2024theDenoauthors; production custom-domain routing/DB semantics описаны прямо; CLI examples не генерировались | Actual page объявляет shutdown Deno Deploy Classic **July20,2026**, раньше даты получения; только явное разрешение исторической platform/version коллекции может снять review, нельзя выдавать за current CLI |
| [PlaceCal](https://github.com/geeksforsocialchange/PlaceCal/blob/5ba2035b2fe319f6edf9e137ad769ace9c073c5c/RELEASING.md) | 410 deploy,411 rollback,412 app details,413 app version | Concrete live placecal.org, staging domain, explicit production destination, полный фактический AGPL3LICENSE и реальные конфиги/CI прочитаны | AGPL3 per-record redistribution/source/share-alike obligations и совместимость aggregate должен независимо решить reviewer; не названо MIT/blanket permissive dataset |

Deno400–402 не являются заменой имён или выдуманными flag combinations: три разных уже опубликованных операции — новая production build/upload, promotion существующей версии, сохранение production traffic с **preview** database. Последняя **не allow**: изоляция базы не делает переключение продуктивного приложения безопасным. Deno403 — read-only history; `show` с большим объёмом конфигурации, env dumps и logs не копировались. Project binding — документированная конфигурация одного project directory, без выдуманного конкретного проекта/UUID. Historical blocker распространяется и на safe counterpart.

PlaceCal410 извлечён буквально из `# Usage: kamal deploy -d production` в [production config](https://github.com/geeksforsocialchange/PlaceCal/blob/5ba2035b2fe319f6edf9e137ad769ace9c073c5c/config/deploy.production.yml). Это **не** самодельная замена `staging` в строке `kamal deploy -d staging # or -d production` из RELEASING. Plain shell command — содержимое уже существующего Usage comment; prefix-comment/prose удалён, команда не переписана. Прочитаны полный base config, production config, `.kamal` inventory и `secrets-common`, весь relevant deploy CI. `.kamal` tree содержит secrets-common и не содержит hooks; secrets-common только перенаправляет значения environment, не вызывает менеджер секретов/произвольную программу. ERB base config читает `.ruby-version` и запускает локальный `git describe` для версии; production config загружает dotenv и читает PRODUCTION_HOST, без source build на metadata reads. [Official app docs](https://kamal-deploy.org/docs/commands/app/) определяют app details/version как container/version metadata; они не exec/log/config. Это ограниченный preflight, не deploy simulation. Deploy и rollback меняют live release и остаются ask; CI tests/release publishing и неизвестные GitHub environment protection policies не объявлены отсутствующими.

Ревизии взяты из **actual GitHub page currentOid**, без догадки API:

- PlaceCal: `5ba2035b2fe319f6edf9e137ad769ace9c073c5c`.
- denoland/docs: `74beb7585f7e798fe0bc8d867295bff23fc2e38e`.
- awsebcli/awsebcli: `d254156cd24df5e31f48f58525e3a07680f4fb47`.
- survos/omeka-bundle: `0fb0c27788e82c79caaaba110e596449a22c2070`.
- ManifoldScholar/manifold-deploy-example: `c2d188e593812a27a503f90c90d49e5a44d400df`.

## Остальные actual sources и основания не добавлять строки

**Dokku / survos Omeka** — [полный actual README](https://github.com/survos/omeka-bundle/blob/0fb0c27788e82c79caaaba110e596449a22c2070/README.md) устанавливает, что kpa-omeka **live and public**, и даёт production image deployment, rebuild, ps/ports/domains report. Это действительно редкий новый operational utility. Actual README и composer.json оба объявляют MIT, но полного собственного LICENSE/notice в inspected root нет. По отдельному решению parent package SPDX сам по себе не снимает coverage вопрос для документа. **Никакого command-containing raw/proposal text из него не сохранял**; только source-level pending. Никаких дефолтных admin passwords, показанных source, emails или secret-dump suggestions не перенёс. Возможный объём после установления прав — около5 содержательно разных строк (image-deploy, rebuild,3metadata reports), это оценка, не принятые строки. MIT самой платформы Dokku не заменяет права на чужой README.

**Kamal / Manifold deploy example** — actual guide полностью описывает pre-build/client-image и post-deploy/client restart hooks, app details/accessory details. Но wrapper repo root без собственной лицензии; Manifold submodule license не переносится автоматически. Это также self-hosted template, не доказанный живой production deployment. Source metadata pending,0 imported.

**Elastic Beanstalk official awsebcli** — actual [README](https://github.com/awsebcli/awsebcli/blob/d254156cd24df5e31f48f58525e3a07680f4fb47/README.rst) и полный Apache2LICENSE прочитаны. Утилита и safe `status`/`list` реальны, но deploy string в Hello World walkthrough generic; production chapter описывает git tag и раздельные `eb use prod`/`eb use dev` для веток. Нельзя склеить новые строки или приписать generic standalone deploy текущую prod branch по предположению. Поэтому0proposals, source-level production-binding review. [Flusshygiene actual README](https://github.com/technologiestiftung/flusshygiene/blob/master/README.md) даёт named profile/deploy/status, но `{ENV}` не устанавливает production, а NODE_ENV=production другого worker population task недостаточно; own license не просмотрен. Blog trinity example имеет concrete sample production output, но reuse terms не просмотрены; snippet не был adopted.

**Supabase / A-Play** — actual полный [production deployment guide](https://github.com/KDR9MGR/a-play-user-app/blob/main/DEPLOYMENT_GUIDE.md) описывает live PayStack keys/domain, edge functions send-email и paystack-webhook и function list. Actual root README объявляет MIT, но его **собственная ссылка LICENSE отвечает404**. Не импортировал команды или private local paths; не исправлял source ошибки (`db reset` как rollback, unsupported log suggestions) в искусственные real rows. После установления прав и CLI semantics возможны2–3 содержательные строки, не функция-название-размножение.

**Supabase official docs** — Keenable нашёл original pinned quickstart-dashboard source и migration backup/restore guide. Последний имеет **разные** source/target project refs у list/deploy: это не same-environment safe pair. CLI hello-world starter сам по себе не устанавливает реальный production target; actual complete file/license дополнительно не просмотрены, в proposals/raw не попал. Не доверял Mintlify-generated mirror pages как первичному CLI reference.

**Current Deno Deploy EA** — после выявления sunset Classic не остановился на obsolete docs: сделал отдельный поиск и прочитал [весь current CLI page](https://docs.deno.com/runtime/reference/cli/deploy/). Он содержит настоящий explicit --prod и --org/--app invocation. Но в inspected page нет чистого same-app deployment/history listing; env list раскрывает значения обычных env vars и не является автоматически безопасным secret-free preflight, logs могут содержать sensitive output. Org database list и sandbox list не доказывают состояние той же app. **Не объединил current deno deploy с Classic deployctl metadata command** и не выдумал отсутствующий status verb. Это перспективный новый utility lead с0admissible pairs в этой выдаче.

**Capistrano** — дополнительные queries нашли capistrano-puma production deploy + puma:status и конкретные app repos, но actual complete app configuration/license/hook chain не просмотрены. Ruby config/plugins и custom status tasks могут исполнять код; не назвал task безопасным по слову status. `deploy:check` может изменять сервер и также не импортирован. **PHP Deployer** config:dump не safe автоматически (секреты + исполняемый PHP), full relevant config/terms не установлены. **Serverless** info загружает config/plugins; **SST** diff строит/исполняет stack program. Никакие dry-run/diff/check не попали в allow без независимой проверки. **Render** дал в основном skills/templates и placeholder service IDs; actual operational production source/terms не получены. Повторные ресурсные/alias варианты не являются дополнительными записями.

## Keenable дополнительные exact queries

Основной search и fetch — Keenable; original pages/raw/лицензии дочитаны статически, без extraction prompt. Ниже строки этой второй волны (не замена rare-dataset coverage из первого отчёта):

1. github production deployment runbook "kamal deploy" "kamal app details"
2. github "cap production deploy" "cap production" "status" "LICENSE"
3. github "dep deploy production" "dep config:dump"
4. github production runbook "dokku ps:rebuild" "dokku ps:report"
5. github production deploy runbook "eb deploy" "eb status"
6. site:kamal-deploy.org hooks pre-connect app details commands
7. github "cap production deploy" "puma:status" "License"
8. github "eb deploy production" "eb status" "MIT"
9. github "git push heroku master" "production" "heroku releases" "License"
10. github production runbook "render deploys create" "render services"
11. "eb deploy" "production" "eb status" -site:stackoverflow.com -site:gist.github.com -site:medium.com -site:dev.to
12. github production deployment "dokku git:from-image" "ps:report" license -survos
13. github "kamal deploy -d production" "kamal app version -d production" "MIT"
14. github production deployment "wrangler versions deploy" "wrangler deployments list" -skills -claude -marketplace
15. github "deployctl deploy --prod" "deployments list"
16. github "production" "supabase functions deploy" "supabase functions list" -skills -claude -tutorial
17. github "serverless deploy --stage prod" "serverless info --stage prod" -skills
18. github "sst deploy --stage production" "sst diff --stage production" -skills -claude
19. site:docs.deno.com "deno deploy" "list" "production" CLI
20. site:github.com/supabase/supabase "supabase functions deploy" "supabase functions list" production

Более редкие corpora из первой волны (TerminalWorld1530actualrows+3solutionmembers,TraceCommons30actualrows) остаются исследованными, с **0 admissible production pairs** и documented terms/synthetic-origin gates. Вторая волна дала новые утилиты/terms evidence, а не выдуманный большой corpus. Не утверждается, что все публичные source leads в интернете исчерпаны; исчерпаны прослеженные в этой выдаче admissible пары без нового permission/context evidence. Честного массового dataset expansion не найдено.

## Артефакты, notices, handoff

- `expansion2-candidates.jsonl`:8needs_review rows400–403,410–413.
- `expansion2-sources.jsonl`:12source/lead records; discovery-only и actual inspected различаются явно.
- `expansion2-pending.jsonl`:15решений (8per-row +7source-level).
- `data/raw/e5b-licensed-review-excerpts.jsonl`:только2лицензированных источника, exact command excerpts, original URLs/revisions, **полные actual MIT/AGPL license text** и явные gates. Unknown-terms README/secret output не сохранялись. Необработанный personal output не сохранялся.

Здесь0new ready candidate,8 review proposals, а не8 принятых. Финальное число после independent review/dedup/notice integration определяет parent. Перенос AGPL требует сохранения per-record source/license obligations; отдельное generic dataset MIT заявление недопустимо. Historical Deno возможно только после отдельного source-version решения, иначе исключить как неподдерживаемую платформу. Оценки для следующих разрешённых operational источников:30–60мин/source и5–10мин/строку с evidence/pair review; это **оценки**, не измеренное время и не гарантированный yield. No random sampling/split; random_state неприменим.

Ни один dataset command, cloud/container/DB/IaC client или скачанный script не исполнялся; Python standard-library urllib/json/re использовались только для получения статических лицензий, revision metadata и сериализации инертных записей. Tests/build/lint/formatters/validator не запускались; code source не редактировался, no-comments skill прочитан. Родителю: один итоговый inert schema/pair/duplicate/provenance/notice review после завершения всех workers; dataset команды не исполнять.
