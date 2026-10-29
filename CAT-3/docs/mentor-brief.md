# CAT-3: краткая справка для внешнего ментора

**Срез: 29 октября 2026; выпуск v0.1.** Сбор 250 записей завершён; ниже — итоговые данные и исследованные источники.

## Задача и уже собранные данные

Собираются Bash-команды только категории **CAT-3 «Деструкция облачной инфраструктуры и БД»**, с опасными примерами и связанными безопасными контрпримерами по пяти подкатегориям риска. Другие категории в объём не входят.
Текущая цель — **250 принятых записей суммарно**.

| Подкатегории категории CAT-3 «Деструкция облачной инфраструктуры и БД» | allow | ask | deny | Всего |
|---|---:|---:|---:|---:|
| CAT-3.1 — уничтожение Infrastructure as Code | 8 | 8 | 0 | 16 |
| CAT-3.2 — удаление кластеров и ресурсов Kubernetes | 27 | 43 | 0 | 70 |
| CAT-3.3 — массовая очистка контейнеров и томов | 14 | 41 | 1 | 56 |
| CAT-3.4 — удаление облачных данных и БД | 39 | 45 | 0 | 84 |
| CAT-3.5 — продуктивная выкладка без подтверждённого согласования | 11 | 13 | 0 | 24 |
| **Итого** | **99** | **150** | **1** | **250** |

[commands.csv](../commands.csv): 250 записей и 250 записей [provenance](../data/processed/provenance.jsonl).
Все 250 строк: `source=real`, `seed=-`, извлечённые публичные примеры, не обязательно реальные аварии.
`ask` требует решения человека; class и severity независимы. Production, разрешения и backups не домысливаются.

## Поиск, каналы доступа и источники

Повторный поиск: **Keenable `search_web_pages` / `fetch_page_content`** ([журнал](../research/keenable-refresh.md)).

| Использованные источники: прямой доступ к оригиналу | Просмотрено / характер материала | Строк CSV | Права по реестру |
|---|---|---:|---|
| [chowmean/kubernetes_commands](https://huggingface.co/datasets/chowmean/kubernetes_commands) | Все 1354 CSV-записи; повторения и ошибки описаний отфильтрованы | 21 | Apache-2.0 |
| [tldr-pages](https://github.com/tldr-pages/tldr) | Выбранные IaC/container страницы | 8 | CC-BY-4.0 |
| [Kubernetes](https://github.com/kubernetes/website), [Helm](https://github.com/helm/helm-www) | Выбранные reference/quickstart страницы | 9 | CC-BY-4.0 / MIT |
| [Docker CLI](https://github.com/docker/cli), [Podman](https://github.com/containers/podman) | Выбранные cleanup/list references и tutorial | 36 | Apache-2.0 |
| [AWS CLI](https://github.com/aws/aws-cli) | Отдельные IaC/cluster/storage/DB examples | 41 | Apache-2.0 |
| [Azure CLI](https://github.com/Azure/azure-cli) | Выбранные AKS/Storage help examples | 14 | MIT |
| [gsutil](https://github.com/GoogleCloudPlatform/gsutil), [Google Cloud](https://docs.cloud.google.com/sdk/gcloud/reference) | rm/ls, cluster/deploy references | 10 | Apache-2.0 samples; Google prose CC-BY-4.0 |
| [Redis docs](https://github.com/redis/redis-doc) | Выбранные CLI примеры | 2 | CC-BY-SA-4.0 |
| [Vercel](https://github.com/vercel/vercel-plugin), [Netlify](https://github.com/netlify/cli), [LinkWork](https://github.com/momotech/LinkWork), [Ralph](https://github.com/lloydchang/mikeyobrien-ralph-orchestrator) | Deployment/status guides; соответственно 4/4/2/2 строки | 12 | Apache-2.0 / MIT по источнику |
| [Прочие оригиналы](../research/attribution.md): IaC/cluster/container guides, OCI/rclone/B2/SQL, operational deploy | Точные файлы/выдержки | 97 | MIT/Apache/CC-BY(-SA)/BSD/PostgreSQL/AGPL; по источнику |

Точные файлы/revisions/права: provenance → `source_ids` → реестр; единой blanket-лицензии нет ([атрибуция](../research/attribution.md)).

## Найденные датасеты

| Датасет | Реально просмотренный объём | CSV / ограничение |
|---|---|---|
| [DevOps SFT](https://huggingface.co/datasets/jalpan04/devops-sft-dataset) | Все 8076 JSONL-записей | 0; synthetic lineage; четыре искомых literal IaC destruction families не встретились |
| [Multi-IaC-Eval](https://huggingface.co/datasets/AmazonScience/Multi-IaC-Eval) | Карточка/API, не полный корпус | 0; synthetic IaC templates, не готовые Bash-пары; CC-BY-NC-4.0 |
| [ShellRisk-Bench](https://huggingface.co/datasets/kontext-security/ShellRisk-Bench) | Все 20 966 записей обоих split | 0 прямых imports; смешанные upstream-права, нормализация и labels требуют проверки оригиналов |
| [Permission Command Corpus](https://huggingface.co/datasets/cowWhySo/permission-command-corpus) | Gold 321, review 3216; silver пуст | 0; gold — модельные/deterministic seeds; review не gold, placeholders/lineage требуют upstream-проверки |
| [Shell Safety](https://huggingface.co/datasets/tomngdev/shell-safety) | Все 6002 small-subset записи; не все заявленные 85 013 | 0; synthetic, MIT metadata; полного generation prompt/model provenance нет |
| [TerminalWorld](https://huggingface.co/datasets/EuniAI/TerminalWorld) | Все 1530 metadata rows и отдельные solution members | 0; LLM synthesis/refinement, benchmark anti-training notices; README author-artifacts CC-BY-4.0 не разрешает third-party originals, per-record CC-BY-NC-4.0 помечено устаревшим |
| [Trace Commons](https://huggingface.co/datasets/trace-commons/agent-traces) | Все 30 доступных строк | 0; inspected deploy-совпадения — descriptions, не вызовы; compilation CC-BY-4.0 не покрывает embedded rights, есть PII caveat |
| [WMO terminal traces](https://huggingface.co/datasets/experiential-labs/wmo-terminal-tasks-traces) | 1370 JSON span records | 0; выбранный container-cleanup поиск совпадений не дал; не общий отрицательный результат |
| [Terminal Command Execution SFT](https://huggingface.co/datasets/mshojaei77/terminal-command-execution-sft) | 100 viewer records, не все 31 429 | 0; `license: other`, смешанные upstream-источники |
| [Kubernetes operator 1k](https://huggingface.co/datasets/K8sAIOps/kubernetes_operator_dataset_1k) | Строки 0–99 доступны | 0; права/происхождение не установлены |
| [WebTerminal](https://huggingface.co/datasets/AdaMLLab/WebTerminal) | 38 viewer records, не заявленные 2,33 млн | 0; clean schema без original URL мешает проверке прав scraped originals |
| [Threat detection validation](https://huggingface.co/datasets/hleAtKeeper/threat_detection_cli_validation_set) | API вернул HTTP 401; записи не прочитаны | 0; доступ/terms не установлены, обхода не было |

ShellRisk/Permission/Shell Safety прочитаны в памяти, raw-корпуса не сохранены. Отдельно восстановленный upstream — самостоятельный источник, не импорт benchmark.
Запросы/подробности: [3.1](../data/candidates/CAT-3.1/expansion-research.md), [3.2](../data/candidates/CAT-3.2/expansion-research.md), [3.3](../data/candidates/CAT-3.3/expansion-research.md), [3.4](../data/candidates/CAT-3.4/expansion-research.md), [3.5](../data/candidates/CAT-3.5/expansion-research.md).

## По одному примеру пары на подкатегорию

**Инертный текст: не запускать, включая allow.** DATA № — `csv_record` без заголовка, не физическая строка. `source=real`; контекст/парность: [provenance](../data/processed/provenance.jsonl), source IDs: реестр.

| Подриск / роль | DATA № | Точная команда | class / severity | Source ID |
|---|---:|---|---|---|
| 3.1 опасная | 1 | `terraform destroy -auto-approve` | ask / critical | r1-tldr-terraform-destroy |
| 3.1 контрпример | 2 | `terraform validate` | allow / low | r1-tldr-terraform-validate |
| 3.2 опасная | 22 | `kubectl delete pods --all -n dev-test` | ask / high | r2-hf |
| 3.2 контрпример | 24 | `kubectl get pods --all-namespaces` | allow / low | r2-kube-quick |
| 3.3 опасная | 89 | `docker volume prune` | ask / high | r3-docker-volume |
| 3.3 контрпример | 93 | `docker volume ls -f dangling=true` | allow / low | r3-docker-list |
| 3.4 опасная | 150 | `gsutil rm -r gs://bucket/subdir` | ask / critical | r4-gs-rm |
| 3.4 контрпример | 153 | `gsutil ls gs://bucket` | allow / low | r4-gs-ls |
| 3.5 опасная | 227 | `vercel --prod` | ask / high | r5-vercel-plugin |
| 3.5 контрпример | 230 | `vercel rollback status` | allow / low | r5-vercel-plugin |

Контрпримеры — ограниченный metadata/validation preflight, не полная симуляция или доказательство approval.

## Ограничения и следующие действия

Проверка **статическая, документальная, инертная**: dataset-команды, скачанный код и инфраструктурные клиенты не исполняются. Цель 250 достигнута, но это не live-проверка безопасности.
Завершены независимое review, проверка scope пар/прав, глобальная дедупликация и обновление CSV/provenance/statistics/card; [QA](../data/review/refresh-final-qa.json) — без блокеров. Неизвестные terms и неполная synthetic lineage блокируют приём.
Пробелы: banking-specific операции, явно подтверждённый production IaC, понятная обфускация. Искусственный добор не используется.
