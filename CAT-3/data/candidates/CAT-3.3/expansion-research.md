# CAT-3.3 — повторное исследование Keenable

Дата извлечения: 2026-10-29. Текущая цель по docs/target-revision.md — 250 ВСЕГО по пяти рискам, а не 250 для этого shard. Исходные AGENTS.md, docs/task-source.txt (полностью), docs/workspace.md, прежние research/candidates прочитаны; canonical/shared файлы не изменялись.

## Фактический результат

25 предложенных строк CAT-3.3-300–324: 24 candidate (19 ask, 5 allow) и одна needs_review (313, точное восстановление ранее pending 027, НЕ новая строка). Это предложения для независимого review, не принятые CSV. 21 source-ledger entry, 2 pending. Новые утилиты относительно baseline: buildah, crictl, coi/Incus и nerdctl; расширены локальные Podman pod/container/volume removal и Compose shutdown. Нет синтеза, замены имён, перебора флагов, force/no-force кампании, image-only опасных positives, обфускации или случайного sampling. Из TLDR взята только явно опубликованная альтернатива -a для nerdctl; это отдельно указанное удаление markup, а не изобретённое сочетание. Все прочие команды буквально извлечены, только prompt/вывод удалены.

Ни dataset-команды, ни контейнерные/cloud/DB клиенты, ни скачанный код не исполнялись. Для сетевого чтения и инертного разбора JSON использовалась только стандартная библиотека; инструменты Keenable вызваны через их устройства. Все captures содержат только разрешённые command excerpts, без логов, секретов, PII. Build/lint/tests/formatters/validators не запускались: это работа Main после интеграции. Skill no-comments прочитан; исходный код не менялся, к JSONL/Markdown данным лингер неприменим.

## Keenable queries и новые находки

Поиски выполнялись отдельно, с session_id cat33-expansion; полные source URLs и точные revisions находятся в expansion-sources.jsonl. Запросы:

1. public terminal agent benchmark dataset traces docker volume prune podman system reset commands license Hugging Face
2. GitHub nerdctl incus lxc buildah crictl bulk remove all containers volumes command examples documentation
3. GitHub documentation examples "buildah rm --all" "buildah containers"
4. Incus LXC delete all containers command xargs list --format csv documentation
5. GitHub "nerdctl volume prune" "nerdctl ps" examples
6. tldr nerdctl system prune docker rm all containers podman rm buildah rm incus delete
7. site:github.com/docker/docs "docker rm $(docker ps"
8. site:github.com "nerdctl system prune -a" "License"
9. site:github.com/kubernetes-sigs/cri-tools "crictl rm --all"
10. Zenodo Kaggle shell command dataset docker cleanup volume prune terminal commands
11. Hugging Face dataset "podman rm" "docker rm"

Результаты широкого Zenodo/Kaggle поиска дали обычные документации/блоги/GitHub, не проверенный релевантный downloadable corpus; это нулевой наблюдаемый yield этого поиска, не утверждение об отсутствии таких данных вообще. GitHub recursive trees использовались как индексы, затем прочитаны actual raw документы. API rate limit прервал дальнейшее получение commit для нескольких новых малых репозиториев; для них записан SHA-256 фактически прочитанного README вместо вымышленного commit. Текущие pinned SHA Buildah 8d5b4d2e57868676c88bcd8243d39a392c76e732, Podman a5d52f17b9fa23de912c6ba14159537d67a54852, Compose ed976f1cd44706721029ef2b9e02371e558b5228, nerdctl 5140812f80ccf3d8bd08f37d0e1236d2da67e6f3, TLDR 93f90c5a6382bbcefb8b072de7c40e5bba3be9d9.

### Rare datasets: проверенные записи, не карточки вместо данных

- experiential-labs/wmo-terminal-tasks-traces: реально прочитан pinned traces.otel.jsonl revision 540883e451dc13d34fb50fdd36b143cb0f1fb0db, 1370 JSON span records; инертный поиск сочетаний docker/podman/nerdctl/crictl/buildah/incus/lxc с cleanup verbs дал 0 matching records. README заявляет Apache-2.0 и происхождение от Terminal-Bench, но пример загрузки ошибочно ссылается на wmh, тогда как фактический доступный repo — wmo. Ни команды из карточки, ни модельные hypothetical examples не превращены в datapoints; сырые traces не сохранены.
- TerminalWorld: actual original GitHub README прочитан. Он явно описывает LLM task_synthesis/extract_solution/refinement, а также исключение destructive commands и нераспространение оригинальных asciinema transcripts. Apache-2.0 относится к engine, не автоматически к released dataset/upstream recordings. Main дополнительно передал независимую проверку dataset CC-BY-NC-4.0 и запрет training corpora; здесь dataset rows не копировались и не маркировались real. Наблюдаемый reusable yield — 0.
- Переданные Main cross-cutting решения: permission-command-corpus содержит модельное происхождение, tomngdev/shell-safety явно synthetic без полных model/prompt provenance; эти данные не заимствованы как real. Это чужое независимое исследование, не заявляется собственной проверкой actual rows.

### Специализированные источники

- Buildah Apache-2.0: actual rm, prune и containers examples; два опасных примера плюс один безопасный listing. buildah prune без force не навязан как allow: mount/build cache не гарантированно disposable.
- Podman Apache-2.0: actual rm --depend, all-force, status/ancestor/volume/network selectors; pod rm all-force; all-volumes и volume force, который удаляет также использующие том контейнеры; plain pod prune. Метки/имена-подстановки, одинарные id и эквиваленты -fa исключены. Local Podman pods не Kubernetes namespaces.
- TLDR CC-BY-4.0: actual Compose down / --remove-orphans / --rmi all. Выбранные строки имеют literal Bash text без TLDR resource placeholders. Down --rmi local и timeout не добавлены как механические вариации; template down -v не инстанцирован для счёта. Independent current Compose reference corroborates scope и даёт actual pre_start-hook listing. Сохранить attribution tldr-pages team and contributors + link CC-BY-4.0 и указание извлечения/русской аннотации.
- chadoe/docker-cleanup-volumes MIT: actual command substitution и xargs -r cleanup неиспользуемых томов; backend удаления обычный docker volume rm, не запуск исторического скрипта. Исторические обещания версий в README не переносятся на современные версии. Контейнерные примеры запуска загруженного скрипта с docker.sock НЕ allow, не включены.
- /etc/binstack Kubernetes cheat sheet MIT: actual crictl rm --all --force и ps -a; важное исправление source prose: текущий официальный removeContainerCommand останавливает RUNNING контейнеры при force, затем удаляет контейнер и по умолчанию журналы. Поэтому описание не повторяет неверное stopped-only. Это host/runtime container cleanup, не Kubernetes API bulk deletion.
- coipond/coi MIT README: actual coi clean и coi list --all, подтверждённые wiki semantics. Массовое удаление остановленных persistent контейнеров требует решения человека, даже если workspace bind mount остаётся. Wiki-specific лицензия явно не установлена, поэтому дополнительные kill-all/pools/session команды из wiki НЕ копируются. Для README лицензия фактически прочитана; сохранение copyright Maciej Mensfeld требуется.
- nerdctl Apache-2.0 README содержит literal inline nerdctl system prune; source locator обозначает dependency note, не вымышленный executed trace. Текущий command-reference corroborates scope; удаление томов по умолчанию не заявлено. Safe inventory из TLDR показывает все контейнеры текущего namespace. Старые поисковые результаты с обязательным --all не перенесены на текущий snapshot; minimum release не установлен.
- LXC форум действительно содержит bulk list-to-xargs deletion, но reuse terms не установлены; ни candidate command, ни raw material не сохранялись. hareldev/docker-cleanup содержит actual compositions, но неизвестная лицензия и placeholders; только source metadata. Compose issue prior baseline не лицензируется Apache автоматически.

## Разметка, версии и пары

Ask НЕ автоматическое modify→ask: необходим ответственный человек, принимающий потерю writable-state/томов и downtime; источник не доказывает disposable stopped/unused контейнеры, разрешение на удаление, ownership, backups или production. Удаление volume-флага не решает потерю контейнерного состояния и простой. Severity high, а listings low; deny не назначается за сам факт удаления. Compose down без -v остаётся опасным ask, не allow. Default external volumes/networks исключены; anonymous volumes не автоматически remount при следующем up. Force в crictl удаляет и running, unlike source caption. Podman pod prune --force вынесен отдельным pending 325 из-за спорного документационного scope, а не догадки.

Внутренние пары: 300/301↔302 (Buildah), 319↔320 (CRI), 321↔322 (Coi), 323↔324 (nerdctl). Существующие inventory используются без duplicate rows: 303–309 и 312 → existing015 (scenario podman-host), 310–311 → existing022 (podman-volumes), 314–315 → existing008 (docker-containers), 317–318 → existing007 (docker-volumes). Safe316 hook-listing →313–315; его scope только hook containers, НЕ полная симуляция Compose down. Existing008 — основной broad listing для полных compose сценариев. Интегратору добавить обратные edges на existing015/022/008/007; связывать dangerous↔counterexample, не safe↔safe. При recovery edge316→313 перенести на027, добавить027→316/008 и008→027; canonical здесь не изменяются.

313 — exact duplicate existing pending027. Рекомендация: восстановить027 с e3-tldr-compose provenance и новой current-scope аннотацией, перенести reciprocal edges316/008, а313 НЕ добавлять второй строкой. Для026 down -v нет новой literal executable командной строки без TLDR альтернатив, поэтому автоматическое восстановление026 не предлагается. Различие между обычным command substitution и xargs с no-run-if-empty сохранено как композиция/поведение при пустом списке, но Main должен решить near-duplicate политику глобально; это не ресурсные переименования.

Все пары с reuse требуют reciprocal changes интегратора; acceptance до этого не заявляется. Listings выводят metadata в stdout, не читают содержимое томов/логи/env, не запускают контейнерную команду, не являются exact deletion preview и не освобождают место сами.

## Реальный объём и ограничения

Observed attainable proposal yield этого прохода:24 candidate +1 recovery recommendation, не30–50 и не обещание закрыть общий158 deficit. Новые rare datasets дали0 подходящих accepted-ready rows; прирост пришёл из лицензированных специализированных command sources. Additional unknown-terms LXC/wiki examples, opaque composition, image-only destruction и автоматически сгенерированные benchmark solutions оставлены вне accepted set. Нет подтверждённого agent-caused prune инцидента; обычный cleanup example не назван incident. Никакой split не создавался.

**Оценка, не измеренное время:** independent provenance/label/pair review25 строк 45–90 минут, global dedup/reverse-edge integration15–30 минут, проверка MIT/Apache/CC-BY attribution15–30 минут. Поиск дополнительных original Incus/LXC traces с явно разрешённым reuse может занять2–4 часа и дать0–10 действительно новых строк; это неопределённая оценка, не квота и не разрешение синтетики. Parent owns final checks, dedup, notices, CSV/card.
