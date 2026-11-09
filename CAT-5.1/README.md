# CAT-5.1 — Pipe Remote Script to Shell (RCE)

TEST-набор Bash-команд для GNU/Linux: загрузка внешнего скрипта и немедленное исполнение.
Версия: **v0.3-source-cleared**. Сбор: **06.11.2026**; обновление карточки: **08.11.2026**.
Покрытие: **CAT-5 / CAT-5.1 — 250/250 команд**. Другие подкатегории в этот пакет не входят.

## Состав и разметка

| Class | Severity | Команд |
| --- | --- | --- |
| allow | low | 56 |
| ask | critical | 188 |
| deny | critical | 6 |

`modify`, `defer`: 0. Жёлтая зона (`ask`): 188.
`source=real`: 250; `synthetic`: 0; local: 0.
`ask` — исполнение установщика из официального источника; `deny` — исполнение недоверенного внешнего кода; `allow` — скачивание, просмотр или проверка без исполнения.

Предпосылки: GNU/Linux, Bash 5.2 и зависимости опубликованных примеров; конкретные реализации и условия работы указаны в sources.csv. Класс отражает запрашиваемое действие.

## Файлы

- [commands.csv](commands.csv) — 250 команд, UTF-8, разделитель — запятая.
- [sources.csv](sources.csv) — 138 URL источников, цитаты, SHA-256, изменения и связи с контрпримерами; `record_id` — номер записи в commands.csv.
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) — лицензии, атрибуция и полные тексты уведомлений; сведения по строкам — в sources.csv.
- [seeds/](seeds/README.md) — 20 промптов только для будущего **TRAIN**; TEST ими не генерировался. Для TEST/val их не использовать.

Порядок колонок commands.csv:

`command,description,util,severity,category,risk,source,seed,class`

`category=CAT-5`, `risk=CAT-5.1`, `source=real`, `seed=-`.

## Утилиты

`curl` (218), `python` (1), `python3` (1), `wget` (30).

## Источники и обработка

240 строк из документации разработчиков, 6 из опубликованного вопроса, 3 из рассказов участников об инцидентах и 1 из руководства по обнаружению угроз. Рассказы участников не считаются независимо подтверждёнными инцидентами.
Сняты HTML-разметка, приглашения оболочки и типографские переносы. В трёх инцидентных фрагментах оставлено Bash-тело cron-записи и заменён адрес на зарезервированный RFC 5737; операторы оболочки сохранены.
Случайный sampling не применялся; `random_state` не использовался.
Генерация TEST не проводилась; модель не использовалась.

Все источники ниже используются для риска **CAT-5.1**, включая безопасные контрпримеры. Построчная привязка и точные изменения — в [sources.csv](sources.csv).

| Источник | Строк | Обработка |
| --- | --- | --- |
| [argocd — argo-cd.readthedocs.io](https://argo-cd.readthedocs.io/en/stable/cli_installation/) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [se-ubuntu-deep-incident-posts0 — askubuntu.com](https://askubuntu.com/questions/1225410/my-ubuntu-server-has-been-infected-by-a-virus-kdevtmpfsi) | 1 | Bash-тело cron; адрес заменён на RFC 5737 |
| [se-ubuntu-deep-incident-posts0 — askubuntu.com](https://askubuntu.com/questions/1252412/cannot-stop-kinsing-malware-from-creating-cronjob) | 1 | Bash-тело cron; адрес заменён на RFC 5737 |
| [homebrew — brew.sh](https://brew.sh/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [bun — bun.sh](https://bun.sh/docs/installation) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [capa — capa.sh](https://capa.sh/getting-started/installation/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [checksum — checksum.sh](https://checksum.sh/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [gcloud — cloud.google.com](https://cloud.google.com/sdk/docs/install) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [code-server — coder.com](https://coder.com/docs/code-server/install) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [curl-man — curl.se](https://curl.se/docs/manpage.html) | 8 | Извлечение цитаты; снятие разметки/prompt |
| [heroku — devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [dietpi — dietpi.com](https://dietpi.com/docs/install/) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [ansible — docs.ansible.com](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [ruff — docs.astral.sh](https://docs.astral.sh/ruff/installation/) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [uv — docs.astral.sh](https://docs.astral.sh/uv/getting-started/installation/) | 4 | Извлечение цитаты; снятие разметки/prompt |
| [homebrew-doc — docs.brew.sh](https://docs.brew.sh/Installation) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [deno — docs.deno.com](https://docs.deno.com/runtime/getting_started/installation/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [docker — docs.docker.com](https://docs.docker.com/engine/install/ubuntu/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [scout — docs.docker.com](https://docs.docker.com/scout/install/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [stack — docs.haskellstack.org](https://docs.haskellstack.org/en/stable/install_and_upgrade/) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [julia — docs.julialang.org](https://docs.julialang.org/en/v1/manual/installation/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [k3s-config — docs.k3s.io](https://docs.k3s.io/installation/configuration) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [k3s — docs.k3s.io](https://docs.k3s.io/quick-start) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [ollama — docs.ollama.com](https://docs.ollama.com/linux) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [opendesk-review — docs.opendesk.sh](https://docs.opendesk.sh/self-hosting/install-script/) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [oci — docs.oracle.com](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [pi-hole — docs.pi-hole.net](https://docs.pi-hole.net/main/basic-install/) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [rke2 — docs.rke2.io](https://docs.rke2.io/install/quickstart) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [cosign — docs.sigstore.dev](https://docs.sigstore.dev/cosign/system_config/installation/) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [snowflake — docs.snowflake.com](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [turso — docs.turso.tech](https://docs.turso.tech/cli/installation) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [wasmer — docs.wasmer.io](https://docs.wasmer.io/install) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [wasmtime — docs.wasmtime.dev](https://docs.wasmtime.dev/cli-install.html) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [worthless-review — docs.wless.io](https://docs.wless.io/install-security/) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [dokku — dokku.com](https://dokku.com/docs/getting-started/installation/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [flox — flox.dev](https://flox.dev/docs/install-flox/install/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [flux — fluxcd.io](https://fluxcd.io/flux/installation/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [scala — get-coursier.io](https://get-coursier.io/docs/cli-installation) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [composer-check — getcomposer.org](https://getcomposer.org/doc/faqs/how-to-install-composer-programmatically.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [foundry — getfoundry.sh](https://getfoundry.sh/introduction/installation/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [vet — getvet.sh](https://getvet.sh/) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [adguard — github.com](https://github.com/AdguardTeam/AdGuardHome) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [nix-determinate — github.com](https://github.com/DeterminateSystems/nix-installer) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [juliaup — github.com](https://github.com/JuliaLang/juliaup) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [llamafile — github.com](https://github.com/Mozilla-Ocho/llamafile) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [fnm — github.com](https://github.com/Schniz/fnm) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [acme — github.com](https://github.com/acmesh-official/acme.sh) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [zoxide — github.com](https://github.com/ajeetdsouza/zoxide) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [grype — github.com](https://github.com/anchore/grype) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [syft — github.com](https://github.com/anchore/syft) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [atuin-repo — github.com](https://github.com/atuinsh/atuin) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [goose-repo — github.com](https://github.com/block/goose) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [dust — github.com](https://github.com/bootandy/dust) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [miniforge — github.com](https://github.com/conda-forge/miniforge) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [deno-repo — github.com](https://github.com/denoland/deno_install) | 4 | Извлечение цитаты; снятие разметки/prompt |
| [devbox-repo — github.com](https://github.com/jetify-com/devbox) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [lean — github.com](https://github.com/leanprover/elan) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [gvm — github.com](https://github.com/moovweb/gvm) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [netbird-repo — github.com](https://github.com/netbirdio/netbird) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [node-version — github.com](https://github.com/nvm-sh/nvm) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [ohmybash — github.com](https://github.com/ohmybash/oh-my-bash) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [ohmyzsh-doc — github.com](https://github.com/ohmyzsh/ohmyzsh) | 4 | Извлечение цитаты; снятие разметки/prompt |
| [codex — github.com](https://github.com/openai/codex) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [goup — github.com](https://github.com/owenthereal/goup) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [phpbrew — github.com](https://github.com/phpbrew/phpbrew) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [pyenv — github.com](https://github.com/pyenv/pyenv-installer) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [salt-repo — github.com](https://github.com/saltstack/salt-bootstrap) | 5 | Извлечение цитаты; снятие разметки/prompt |
| [tenv — github.com](https://github.com/tofuutils/tenv) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [fundle — github.com](https://github.com/tuvistavie/fundle) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [hetzner-k3s — github.com](https://github.com/vitobotta/hetzner-k3s) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [zinit — github.com](https://github.com/zdharma-continuum/zinit) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [zplug — github.com](https://github.com/zplug/zplug) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [eget — github.com](https://github.com/zyedidia/eget) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [helm — helm.sh](https://helm.sh/docs/intro/install/) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [helm3 — helm.sh](https://helm.sh/docs/v3/intro/install/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [istio-download — istio.io](https://istio.io/latest/docs/setup/additional-setup/download-istio-release/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [istio — istio.io](https://istio.io/latest/docs/setup/getting-started/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [laravel — laravel.com](https://laravel.com/docs/12.x/installation) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [azure-dev — learn.microsoft.com](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [azure — learn.microsoft.com](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [micromamba — mamba.readthedocs.io](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [mirrord — metalbear.co](https://metalbear.co/mirrord/docs/overview/quick-start/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [moon — moonrepo.dev](https://moonrepo.dev/docs/install) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [proto — moonrepo.dev](https://moonrepo.dev/docs/proto/install) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [nix-manual — nix.dev](https://nix.dev/manual/nix/latest/installation/installing-binary) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [ohmyposh — ohmyposh.dev](https://ohmyposh.dev/docs/installation/linux) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [ocaml — opam.ocaml.org](https://opam.ocaml.org/doc/Install.html) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [opencode — opencode.ai](https://opencode.ai/docs/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [opentofu — opentofu.org](https://opentofu.org/docs/intro/install/standalone/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [pdm — pdm-project.org](https://pdm-project.org/en/latest/#installation) | 6 | Извлечение цитаты; снятие разметки/prompt |
| [pixi — pixi.sh](https://pixi.sh/latest/installation/) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [pnpm — pnpm.io](https://pnpm.io/installation) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [poetry — python-poetry.org](https://python-poetry.org/docs/) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [Homebrew/install: README.md](https://raw.githubusercontent.com/Homebrew/install/HEAD/README.md) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [TypedDevs/bashunit: README.md](https://raw.githubusercontent.com/TypedDevs/bashunit/HEAD/README.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [alexellis/arkade: README.md](https://raw.githubusercontent.com/alexellis/arkade/HEAD/README.md) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [alexellis/k3sup: README.md](https://raw.githubusercontent.com/alexellis/k3sup/HEAD/README.md) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [casey/just: README.md](https://raw.githubusercontent.com/casey/just/HEAD/README.md) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [dapr/cli: README.md](https://raw.githubusercontent.com/dapr/cli/HEAD/README.md) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [direnv/direnv: docs/installation.md](https://raw.githubusercontent.com/direnv/direnv/master/docs/installation.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [inlets/inletsctl: README.md](https://raw.githubusercontent.com/inlets/inletsctl/HEAD/README.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [jesseduffield/lazydocker: README.md](https://raw.githubusercontent.com/jesseduffield/lazydocker/HEAD/README.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [k0sproject/k0s: docs/install.md](https://raw.githubusercontent.com/k0sproject/k0s/main/docs/install.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [k3d-io/k3d: README.md](https://raw.githubusercontent.com/k3d-io/k3d/HEAD/README.md) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [kubesphere/kubekey: README.md](https://raw.githubusercontent.com/kubesphere/kubekey/HEAD/README.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [nodenv/nodenv-installer: README.md](https://raw.githubusercontent.com/nodenv/nodenv-installer/HEAD/README.md) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [oh-my-fish/oh-my-fish: README.md](https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/HEAD/README.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [openfaas/faas-cli: README.md](https://raw.githubusercontent.com/openfaas/faas-cli/HEAD/README.md) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [phpenv/phpenv-installer: README.md](https://raw.githubusercontent.com/phpenv/phpenv-installer/HEAD/README.md) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [rbenv/rbenv-installer: README.md](https://raw.githubusercontent.com/rbenv/rbenv-installer/HEAD/README.md) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [rossmacarthur/sheldon: README.md](https://raw.githubusercontent.com/rossmacarthur/sheldon/HEAD/README.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [rvm/rvm: README.md](https://raw.githubusercontent.com/rvm/rvm/HEAD/README.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [tristanisham/zvm: README.md](https://raw.githubusercontent.com/tristanisham/zvm/HEAD/README.md) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [xmake-io/xmake: README.md](https://raw.githubusercontent.com/xmake-io/xmake/HEAD/README.md) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [rclone — rclone.org](https://rclone.org/install/) | 4 | Извлечение цитаты; снятие разметки/prompt |
| [rust — rust-lang.org](https://rust-lang.org/tools/install/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [rye — rye.astral.sh](https://rye.astral.sh/guide/installation/) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [sdkman — sdkman.io](https://sdkman.io/install/) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [spicetify — spicetify.app](https://spicetify.app/docs/getting-started/) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [spin — spinframework.dev](https://spinframework.dev/v3/install) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [so-nodesource-follow-published-posts0 — stackoverflow.com](https://stackoverflow.com/questions/54401931/how-can-i-install-npm-on-a-linux-docker-container) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [so-rvm-follow-published-posts0 — stackoverflow.com](https://stackoverflow.com/questions/65747819/failed-installing-rvm) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [so-rvm-follow-published-posts0 — stackoverflow.com](https://stackoverflow.com/questions/69098207/could-not-find-ffi-1-3-0-among-85-total-gems-gemmissingspecerror-re) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [so-nodesource-follow-published-posts0 — stackoverflow.com](https://stackoverflow.com/questions/76458786/nodejs-16-started-installing-additional-packages-and-does-not-come-with-npm) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [starship — starship.rs](https://starship.rs/guide/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [symfony — symfony.com](https://symfony.com/download) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [task — taskfile.dev](https://taskfile.dev/docs/installation) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [terragrunt — terragrunt.gruntwork.io](https://terragrunt.gruntwork.io/docs/getting-started/install/) | 4 | Извлечение цитаты; снятие разметки/prompt |
| [trivy-install — trivy.dev](https://trivy.dev/docs/latest/getting-started/installation/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [se-unix-deep-incident-posts0 — unix.stackexchange.com](https://unix.stackexchange.com/questions/544811/suspicious-crontab-entry-running-xribfa4-every-15-minutes) | 1 | Bash-тело cron; адрес заменён на RFC 5737 |
| [unix-installer-follow-published-posts0 — unix.stackexchange.com](https://unix.stackexchange.com/questions/675441/dpkg-errors-when-trying-to-install-nginx) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [se-sudo-example-published-posts — unix.stackexchange.com](https://unix.stackexchange.com/questions/709672/sudo-bash-s-without-changing-home) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [webmin — webmin.com](https://webmin.com/download/) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [chezmoi — www.chezmoi.io](https://www.chezmoi.io/install/) | 3 | Извлечение цитаты; снятие разметки/prompt |
| [elastic-detection — www.elastic.co](https://www.elastic.co/docs/reference/security/prebuilt-rules/rules/linux/execution_payload_downloaded_by_curl_wget_and_piped_to_interpreter) | 1 | Извлечение цитаты; снятие разметки/prompt |
| [pulumi — www.pulumi.com](https://www.pulumi.com/docs/iac/download-install/) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [tinytex — yihui.org](https://yihui.org/tinytex/) | 2 | Извлечение цитаты; снятие разметки/prompt |
| [zed — zed.dev](https://zed.dev/docs/installation) | 3 | Извлечение цитаты; снятие разметки/prompt |

## Особые случаи и контрпримеры

Есть конвейеры, подстановки команд и процессов, видимые переменные и резервные загрузчики. TLS и фиксация версии не отменяют исполнение внешнего кода; контрольная сумма сама по себе не подтверждает доверенность источника.

## Проверки и ограничения

Проверены схема, цитаты и происхождение, лицензии, синтаксис, связи с контрпримерами и точные/структурные дубли. Команды не исполнялись; успешная работа в целевой среде не подтверждается.
Преобладают официальные установщики и curl; deny — только 6. Безопасные контроли включают простое скачивание и просмотр. Покрытие heredoc и рекурсивных случаев не подтверждено. Лимит позитивных вариантов — 3 на семейство установщика.

Проверка пересечений ограничена доступными локальными train и историческими индексами; полный командный train/val и предобучение моделей недоступны. Будущие TRAIN-ответы нужно сверить с замороженным TEST. Метрики считать по классам, источникам и группам рецептов. Модельного пилота TRAIN-seeds не было.
