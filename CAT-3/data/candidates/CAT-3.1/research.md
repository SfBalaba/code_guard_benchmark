# CAT-3.1 — исследование инфраструктурной деструкции

Дата обращения к источникам: 2026-10-29. Выполнено только статическое чтение публичных источников; команды датасета, клиенты IaC/облака, скачанный код, source/eval не исполнялись. Внутренняя обработка JSON и запись текстовых файлов не выполняли поля команд. Автоматические проверки и окончательное принятие записей принадлежат интегратору.

## Наблюдаемый результат

- `candidates.jsonl`: 12 записей, из них 9 имеют статус `candidate`, 3 — `needs_review`.
- Парные предложения: 4 опасные `ask / critical`, 5 контрпримеров `allow / low`, 4 сценария; взаимные ссылки заданы. У Terraform и Pulumi по одной паре, у удаления стека CloudFormation два содержательно различных контрпримера, у многоаккаунтного удаления StackSet один.
- Наблюдаемый объём, предлагаемый к независимому ревью, — 9, не 250; дефицит этого предложения — 241. Итоговое число accepted не определяется исследователем. Даже если все 9 пройдут ревью, дефицит останется 241.
- Все извлечённые команды имеют `source=real`, `seed=-`, `synthetic_model=null`; синтетическое расширение не проводилось. Описания и основания разметки написаны по-русски/английски, текст команд сохранён либо минимально нормализован, как отмечено в каждой записи.
- Нет подтверждённых explicit-production разрушительных примеров, поэтому нет искусственно добавленных `deny`. Правило для действительно явно production IaC остаётся `deny / critical`.
- Не получена принятая CDK-пара: обнаружена действительная forced wildcard-команда в issue, но не установлены независимые права повторного использования текста вклада и гарантированно безопасный контрпример. Не подменяем её придуманной командой.

## Поисковое покрытие

Hugging Face исследован отдельно от GitHub:

1. `site:huggingface.co/datasets "terraform destroy"` — находки AmazonScience/Multi-IaC-Eval, Recursive-Task-Synthesis и набор issues провайдеров. Последние два остались поисковыми зацепками: фактические записи и права для допуска не установлены, поэтому не используются как доказательство строк.
2. `site:huggingface.co/datasets ("pulumi destroy" OR "cdk destroy" OR "cloudformation delete-stack")` — в основном Multi-IaC-Eval и jalpan04/devops-sft-dataset; также нерелевантный Roblox-набор. Сниппеты не считались проверенными командами.
3. Для [Multi-IaC-Eval](https://huggingface.co/datasets/AmazonScience/Multi-IaC-Eval/blob/e3dd91b42c13f20a86fb23a2cf8a5d84126f6fc3/README.md) прочитаны API metadata и полная карточка: synthetic IaC template mutation, заявленные 263 CloudFormation / 446 Terraform / 64+64 CDK шаблонов не являются количеством Bash-команд. CC-BY-NC-4.0 не объявляется безусловно совместимой лицензией. Попытка dataset-server first-rows с default/train вернула HTTP 404; CSV не считался проверенным по карточке.
4. Для [DevOps SFT](https://huggingface.co/datasets/jalpan04/devops-sft-dataset/blob/bd57569ae3424607bf8a404e274429f2182f30ea/README.md) прочитана полная карточка и все 8076 строк train.jsonl как инертный JSON. Наблюдаемые совпадения точных строк `terraform destroy`, `pulumi destroy`, `cdk destroy`, `cloudformation delete-stack`: 0 для каждой. Это не доказывает отсутствие иных записей о IaC, обфускаций или семантических аналогов. Карточка заявляет Apache-2.0, генерацию gemini-2.0-flash и qwen2.5-coder:7b из смешанных документов; точных прав исходных документов/полных промптов нет. Данные набора не сохранялись.

GitHub-запросы:

- `site:github.com "destroy --yes" "validate" pulumi terraform "auto-approve"` — tldr, training, issues, plugin.
- `site:github.com/aws/aws-cdk "cdk destroy --force"` — regression issue 32836 и обсуждения destroy/dry-run.
- `site:github.com "terraform destroy -auto-approve" "LICENSE" "prod"` — training/cheats, actions, tldr; production-контекст нельзя вывести из совпадения разных частей документа.
- `site:github.com "terraform plan -destroy -out" "terraform apply"` — cheatsheet и официальные docs; прочитанный cheatsheet не подтвердил saved destroy plan, поэтому generic `terraform apply tfplan` не выдаётся за destruction-пример.
- `site:github.com/pulumi "pulumi destroy" "--skip-preview"` — implementation/issues/actions; не извлекались модели-комбинации флагов из описания опций.
- `"cdk destroy --all --force" github` и `"cdk destroy" "--force" "LICENSE"` — официальные docs, marketplace, third-party tutorials; marketplace URL вернул HTTP 404. Не используется как доступный источник команд.

В репозитории aws/aws-cli дополнительно прочитан публичный список файлов cloudformation examples: позволил обнаружить не только одиночный delete-stack, но и содержательно отличный multi-account/multi-region delete-stack-instances. Файлы actual examples прочитаны, затем получены повторно по зафиксированному commit для цитируемых captures.

## Доступные извлечённые источники и условия повторного использования

Полная построчная ведомость находится в `proposed-sources.jsonl`.

### tldr-pages/tldr

Commit `93f90c5a6382bbcefb8b072de7c40e5bba3be9d9`. Прочитаны страницы terraform-destroy, terraform-validate, terraform-plan, pulumi-destroy, pulumi-stack, aws-cloudformation, cdk. [Точная лицензия](https://github.com/tldr-pages/tldr/blob/93f90c5a6382bbcefb8b072de7c40e5bba3be9d9/LICENSE.md): документация CC-BY-4.0, отдельная MIT-лицензия scripts здесь не применяется. Атрибуция обязательна: tldr-pages team and contributors; [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Лицензия и соответствующие страницы сохранены в `data/raw/r1-tldr-*.txt`. Нельзя объявлять весь репозиторий MIT.

Из tldr в парные предложения вошли Terraform destroy/validate, Pulumi destroy/list и CloudFormation list. Из вариантов `[-y|--yes]` выбран --yes; маркеры шаблона profile удалены без выдумывания production. Сырые страницы содержат также невыбранные команды — это не принятые строки датасета.

### aws/aws-cli

Commit `2d3e88e0116413754d907a15ec11b02a985ad66e`. [Точная лицензия](https://github.com/aws/aws-cli/blob/2d3e88e0116413754d907a15ec11b02a985ad66e/LICENSE.txt): Apache-2.0; Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. Использованы реальные RST examples delete-stack, delete-stack-instances, describe-stack-resources, describe-stack-instance. Сохранены только вступительный контекст и команды, без ответов API; индентация RST удалена, CRLF преобразованы в LF. Значения account ID являются явно опубликованными фиктивными примерами документации, а не обнаруженными пользовательскими аккаунтами. Исходная лицензия сохранена отдельно.

### Не допущенные источники

- [CDK issue 32836](https://github.com/aws/aws-cdk/issues/32836): actual forced command и диагностический контекст прочитаны, текст не скопирован в кандидаты/captures при неизвестных правах вклада. Это регрессия CDK, не подтверждённый агентный инцидент.
- [ondrejsika/terraform-training](https://github.com/ondrejsika/terraform-training): прочитана карточка/README и перечень файлов, явные условия повторного использования не установлены; нет извлечения, контактные данные автора не сохранялись.
- [dom inatos cheatsheet](https://github.com/dominatos/devtoolbox-cheats/blob/main/cheats.d/dev-tools/terraformcheatsheet.md): фактические команды прочитаны, права не установлены, уникальный noninteractive destruction-контекст не подтверждён; нет извлечения.

## Статическая проверка поведения и независимая безопасность контрпримеров

- [Terraform destroy](https://developer.hashicorp.com/terraform/cli/commands/destroy) — alias `apply -destroy`; [apply](https://developer.hashicorp.com/terraform/cli/commands/apply) подтверждает, что auto-approve снимает запрос, а saved plan применяется без подтверждения. Saved plan может быть destructive, но без соответствующего источника/содержимого плана этот случай здесь не создаётся. `-input=false` само по себе не означает approval: официальная документация говорит, что без подтверждения операция консервативно завершается ошибкой.
- [Terraform validate](https://developer.hashicorp.com/terraform/cli/commands/validate) прямо заявляет отсутствие проверки remote services/backend/provider APIs и безопасность автоматического запуска. Используется только bare validate; это не установка зависимостей и не init. Предполагается обычная доверенная установленная утилита/плагины, не произвольный malicious binary. Это независимый allow, а не просто удаление опасного флага.
- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan) не применяет запланированные изменения, но читает remote objects/provider state. [External provider](https://github.com/hashicorp/terraform-provider-external) прямо описан как интерфейс с внешними программами. Поэтому generic plan и plan -destroy оставлены needs_review: исходная конфигурация/провайдеры/data sources не видны. Ошибка reader при запросе versioned registry data-source URL вернула overview другой версии; это не принято за надёжную версионную документацию и зарегистрировано как tool issue.
- [Pulumi destroy](https://www.pulumi.com/docs/iac/cli/commands/pulumi_destroy/) — generally irreversible, --yes automatically approves after preview, selected stack resources removed; --remove дополнительно удаляет stack/config. Нет предположения, что preview или отсутствие --skip-preview означает ручной approval. [Stack list](https://www.pulumi.com/docs/iac/cli/commands/pulumi_stack_list/) — read-only inventory metadata текущего проекта, не вывод секретов и не export состояния. Preview-программа не предлагается как безусловно безопасная.
- [CloudFormation delete-stack](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/delete-stack.html) запускает удаление асинхронно; DeletionPolicy/retain могут сохранить часть ресурсов, но это не гарантированные резервные копии или разрешение. [List-stacks](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/list-stacks.html) возвращает summaries; [describe-stack-resources](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/describe-stack-resources.html) возвращает metadata первых 100 ресурсов. Это два разных полезных шага инспекции перед удалением, без redirection/секретных output-флагов.
- [DeleteStackInstances](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/delete-stack-instances.html) с --no-retain-stacks удаляет сами стеки, а не только регистрацию в StackSet. [DescribeStackInstance](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/describe-stack-instance.html) возвращает сведения, не меняя инфраструктуру. Парный инспекционный пример относится к тому же имени StackSet, но не заявлен полным перечислением той же двухрегиональной области удаления. В опубликованном контексте ParameterOverrides пуст, никаких секретных значений не сохраняется.
- [CDK destroy](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-destroy.html) документирует --force как no-confirmation, Retain как исключение, --all и concurrency как широкую область/параллельность. [CDK list](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-list.html) показывает --app='node bin/main.js'; без исходного app/assembly generic ls нельзя автоматически объявлять инертным. Source issue различает 2.175.0 failing и 2.174.1/2.175.1 working — не переносим working семантику на failing версию.

Все dangerous имеют ask/critical по политике: фактическая широта разрушения видна, production/approval/backups/isolation не выдумываются. Наличие только слова prod в другой части README не основание deny. Counterexample severity low назначена независимо от critical у пары; review-only plan/CDK имеют medium как локальный/контекстный риск, а не обещание безопасности.

## Незавершённые вопросы и ограничения

`proposed-pending.jsonl` содержит шесть вопросов: два Terraform plan, CDK ls, forced CDK provenance/version/pair, несовместимые примеры terraform validate и HF источники. У tldr validate позиционный directory/-no-tests/-test-directory не подтверждены текущей официальной Usage; их не добавляли ради объёма. Интерактивный bare destroy, --target без подтверждённого bypass, name-only варианты и форматные варианты JSON не увеличивают принятый объём. Обфусцированные формы не обнаружены как лицензированные полностью понятные парные реальные примеры; не синтезировались.

Проверенные sandbox-политики и подтверждённые агентные инциденты исследуются интегратором глобально. В этом срезе не найдено первичного доказательства именно агентного IaC-destruction инцидента; failure issue нельзя выдавать за такое событие. Ничего не запускалось для испытания sandbox.

Нет случайного sampling: целевой выбор по фактической семантической новизне и проверяемой лицензии; random_state not_applicable. Нет train/test split, поэтому проверка утечки между split здесь неприменима; документационные примеры заведомо публичны и могут быть знакомы моделям.

Общая ветка feat/data_cat3 выбрана интегратором; параллельные checkout feat/data_<risk> в одном worktree не выполнялись. Это явное операционное отклонение от исходного пожелания по имени ветки, а не скрытое соответствие.

## Оценка достижимого объёма и времени

**Наблюдение:** текущие допущенные к ревью источники дали 9 содержательно различных парных предложений, а HF полный точный поиск одного набора — 0 destructive-family совпадений. Остальные описанные источники дают review-препятствия, а не гарантированный запас строк. Никаких доказательств достижимости 250 реальных уникальных записей сейчас нет.

**Оценка, не измеренное время:** дополнительный прицельный поиск официальных Apache/MIT/CC-BY репозиториев и публичных CI Bash-примеров может дать ещё примерно 10–30 полезных строк после удаления тривиальных дублей за 4–8 часов исследования, 3–6 часов проверки поведения/контекста и 2–4 часа независимого ревью/интеграции. Основание диапазона — узкие destructive CLI-семейства, редкость видимых safe contexts у планирования/синтеза, необходимость inspect license+actual source для каждой пары. Это условная оценка с низкой уверенностью, не обещание прироста и не скрытый новый целевой объём. Получение 250 требует значительно более широкого лицензированного корпуса логов/инцидентов; без него наиболее честный результат — зафиксированный дефицит, не комбинации флагов, не замена имён ресурсов и не synthetic campaign.

Для интегратора: выполнить инертный schema/CSV/provenance/pairing/dedup review один раз после слияния; отдельно проверить перенос CC-BY атрибуции и Apache notice в карточку/sidecars. Исследователь эти проверки не запускал.
