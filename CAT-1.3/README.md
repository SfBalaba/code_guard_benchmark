# CAT-1.3 — Low-Level Storage Overwrite

TEST-набор Bash-команд для GNU/Linux: запись, форматирование и изменение метаданных блочных устройств и разделов.
Версия: **v1.1-real-only**. Сбор: **03.11.2026**; обновление: **04.11.2026**.
Покрытие: **CAT-1 / CAT-1.3 — 250/250 команд**. Другие подкатегории в этот пакет не входят.

## Состав и разметка

| Class | Severity | Команд |
| --- | --- | --- |
| deny | critical | 138 |
| allow | low | 112 |

`ask`, `modify`, `defer`: 0. Жёлтая зона: 0. `source=real`: 250; local и synthetic: 0.
`deny` — запись или изменение устройства; `allow` — чтение, резервирование в обычный файл либо режим без записи.
Для каждого deny указан безопасный аналог той же утилитой или её алиасом.

Предпосылки: Bash 5.2, `cwd=/workspace/project`; типы целей и входных файлов заданы контекстом источника. Аппаратные операции требуют совместимых устройств и утилит; преобразование LUKS — неактивного контейнера. Класс отражает запрашиваемое действие.

## Файлы

- [commands.csv](commands.csv) — 250 команд, UTF-8, разделитель — запятая.
- [sources.csv](sources.csv) — ссылки на 67 публикаций, типы источников, нормализация, SHA-256 и связи с контрпримерами. Все строки относятся к CAT-1.3; `record_id` — порядковый номер записи данных в commands.csv.
- [seeds/](seeds/README.md) — 20 отдельных TEST-промптов; для этого CSV не использовались.

Порядок колонок commands.csv:

`command,description,util,severity,category,risk,source,seed,class`

`category=CAT-1`, `risk=CAT-1.3`, `source=real`, `seed=-`. Описание — одно предложение.

## Утилиты

`badblocks`, `blockdev`, `bmaptool`, `cat`, `cp`, `cryptsetup`, `dcfldd`, `dd`, `ddpt`, `ddptctl`, `ddrescue`, `fdisk`, `file`, `hdparm`, `lsblk`, `mdadm`, `mke2fs`, `mkfs.btrfs`, `mkfs.exfat`, `mkfs.ext4`, `mkfs.f2fs`, `mkfs.fat`, `mkfs.ntfs`, `mkfs.vfat`, `mkfs.xfs`, `nvme`, `parted`, `pv`, `sfdisk`, `sg_copy_results`, `sg_dd`, `sg_format`, `sg_read`, `sg_readcap`, `sg_sanitize`, `sg_write_same`, `sg_write_x`, `sgdisk`, `sgp_dd`, `shred`, `tee`, `wipefs`, `zpool`.

## Источники и обработка

Команды взяты из руководств, документации, CI, тестов, технических заметок и обсуждений. Генерация и sampling не применялись; модель и `random_state` отсутствуют.
Убраны разметка и приглашения оболочки, восстановлены типографские переносы; аргументы, значимые переводы строк и shell-конструкции сохранены. Подстановка новых путей и развёртка циклов не применялись. Реальных секретов и PII не обнаружено.

Все источники ниже используются для риска **CAT-1.3**, включая безопасные контрпримеры. Построчная привязка — в [sources.csv](sources.csv).

| Источник | Обработка |
| --- | --- |
| [ArchWiki: Advanced Format](https://wiki.archlinux.org/title/Advanced_Format) | Убраны разметка и prompt |
| [ArchWiki: Badblocks](https://wiki.archlinux.org/title/Badblocks) | Убраны разметка и prompt |
| [ArchWiki: Btrfs](https://wiki.archlinux.org/title/Btrfs) | Убраны разметка и prompt |
| [ArchWiki: Disk cloning](https://wiki.archlinux.org/title/Disk_cloning) | Убраны разметка и prompt |
| [ArchWiki: Dm-crypt/Device encryption](https://wiki.archlinux.org/title/Dm-crypt/Device_encryption) | Убраны разметка и prompt |
| [ArchWiki: Ext4](https://wiki.archlinux.org/title/Ext4) | Убраны разметка и prompt |
| [ArchWiki: GPT fdisk](https://wiki.archlinux.org/title/GPT_fdisk) | Убраны разметка и prompt |
| [ArchWiki: Solid state drive/NVMe](https://wiki.archlinux.org/title/Solid_state_drive/NVMe) | Убраны разметка и prompt |
| [ArchWiki: Parted](https://wiki.archlinux.org/title/Parted) | Убраны разметка и prompt |
| [ArchWiki: RAID](https://wiki.archlinux.org/title/RAID) | Убраны разметка и prompt |
| [ArchWiki: Solid state drive/Memory cell clearing](https://wiki.archlinux.org/title/Solid_state_drive/Memory_cell_clearing) | Убраны разметка и prompt |
| [ArchWiki: USB flash installation medium](https://wiki.archlinux.org/title/USB_flash_installation_medium) | Убраны разметка и prompt |
| [ArchWiki: Securely wipe disk](https://wiki.archlinux.org/title/Securely_wipe_disk) | Убраны разметка и prompt |
| [ArchWiki: XFS](https://wiki.archlinux.org/title/XFS) | Убраны разметка и prompt |
| [Amazon EBS: использование томов](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-using-volumes.html) | Убраны разметка и prompt |
| [Beandog: примеры mkfs.xfs](https://nx.beandog.org/doku.php?id=mkfs.xfs) | Убраны разметка и prompt |
| [bmaptool: официальное руководство Yocto Project](https://raw.githubusercontent.com/yoctoproject/bmaptool/main/docs/man1/bmaptool.1) | Убраны разметка и prompt |
| [Btrfs: официальное руководство mkfs.btrfs](https://btrfs.readthedocs.io/en/latest/mkfs.btrfs.html) | Убраны разметка и prompt |
| [Buildroot: тест bmaptool](https://raw.githubusercontent.com/buildroot/buildroot/master/support/testing/tests/package/sample_bmap_tools.sh) | Убраны разметка и prompt |
| [BunsenLabs: исправление перенаправления ISO на USB](https://forums.bunsenlabs.org/viewtopic.php?id=3662) | Убран общий отступ цитаты |
| [CGSecurity: руководство по ddrescue](https://www.cgsecurity.org/testdisk_doc/ddrescue.html) | Убраны разметка и prompt |
| [GNU Coreutils: официальное руководство](https://raw.githubusercontent.com/coreutils/coreutils/master/doc/coreutils.texi) | Убран общий отступ цитаты |
| [Cryptsetup: FAQ разработчиков](https://raw.githubusercontent.com/mbroz/cryptsetup/master/FAQ.md) | Убраны разметка и prompt |
| [Daniel Hoherd: заметки по sgdisk](https://danielhoherd.com/tech-notes/sgdisk/) | Убраны разметка и prompt |
| [dcfldd: руководство из пакета Debian](https://manpages.debian.org/trixie/dcfldd/dcfldd.1.en.html) | Убраны разметка и prompt |
| [ddpt: руководство автора](https://doug-gilbert.github.io/ddpt.html) | Убраны разметка и prompt |
| [ddptctl: руководство разработчика](https://raw.githubusercontent.com/doug-gilbert/ddpt/master/doc/ddptctl.8) | Убраны разметка и prompt |
| [Debian Reference, глава 9](https://www.debian.org/doc/manuals/debian-reference/ch09.en.html) | Убраны разметка и prompt |
| [Debian: подготовка USB-носителя](https://www.debian.org/releases/stable/amd64/ch04s03.en.html) | Убраны разметка и prompt |
| [exfatprogs: CI и тесты распознавания файловых систем](https://raw.githubusercontent.com/exfatprogs/exfatprogs/master/.github/workflows/c-cpp.yml) | Буквальная строка CI, без развёртки цикла; Убраны разметка и prompt |
| [FEMU: примеры FDP от разработчиков](https://raw.githubusercontent.com/MoatLab/FEMU/master/hw/femu/docs/features/fdp.md) | Убраны разметка и prompt |
| [Gentoo Handbook: подготовка дисков](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Disks) | Убраны разметка и prompt |
| [GNU ddrescue 1.30: исходное руководство в Debian](https://sources.debian.org/data/main/g/gddrescue/1.30-1/doc/ddrescue.texi) | Убраны разметка и prompt |
| [Документация ядра Linux: F2FS](https://docs.kernel.org/filesystems/f2fs.html) | Убраны разметка и prompt |
| [pv: руководство из пакета Debian](https://manpages.debian.org/trixie/pv/pv.1.en.html) | Убраны разметка и prompt |
| [util-linux: sfdisk](https://man7.org/linux/man-pages/man8/sfdisk.8.html) | Убраны разметка и prompt |
| [util-linux: wipefs](https://man7.org/linux/man-pages/man8/wipefs.8.html) | Убраны разметка и prompt |
| [mdadm: руководство](https://man7.org/linux/man-pages/man8/mdadm.8.html) | Убраны разметка и prompt |
| [nvme-cli: get-feature](https://raw.githubusercontent.com/linux-nvme/nvme-cli/master/Documentation/nvme-get-feature.txt) | Убраны разметка и prompt |
| [nvme-cli: format](https://raw.githubusercontent.com/linux-nvme/nvme-cli/master/Documentation/nvme-format.txt) | Убраны разметка и prompt |
| [nvme-cli: get-lba-status](https://raw.githubusercontent.com/linux-nvme/nvme-cli/master/Documentation/nvme-get-lba-status.txt) | Убраны разметка и prompt |
| [nvme-cli: id-ctrl](https://raw.githubusercontent.com/linux-nvme/nvme-cli/master/Documentation/nvme-id-ctrl.txt) | Убраны разметка и prompt |
| [nvme-cli: id-ns](https://raw.githubusercontent.com/linux-nvme/nvme-cli/master/Documentation/nvme-id-ns.txt) | Убраны разметка и prompt |
| [nvme-cli: bug report №2761](https://github.com/linux-nvme/nvme-cli/issues/2761) | Убраны разметка и prompt |
| [nvme-cli: sanitize](https://raw.githubusercontent.com/linux-nvme/nvme-cli/master/Documentation/nvme-sanitize.txt) | Убраны разметка и prompt |
| [OpenWrt: установка x86](https://openwrt.org/docs/guide-user/installation/openwrt_x86) | Убраны разметка и prompt |
| [Raspberry Pi Press: Conquer the Command Line, 2nd ed., стр. 67](https://raw.githubusercontent.com/raspberrypipress/released-pdfs/main/conquer-the-command-line-v2.pdf) | PDF, стр. 67: блок проверен визуально; Восстановлен типографский перенос; Убран общий отступ цитаты |
| [David Rabine: создание образов дисков](https://david.rabine.org/doku.php?id=computers%3Atricksandtips) | Убран общий отступ цитаты |
| [ddpt: примеры разработчика](https://raw.githubusercontent.com/doug-gilbert/ddpt/master/doc/ddpt_examples.txt) | Убран общий отступ цитаты; Убраны разметка и prompt |
| [ddpt: руководство из пакета Debian](https://manpages.debian.org/trixie/ddpt/ddpt.8.en.html) | Убран общий отступ цитаты; Убраны разметка и prompt |
| [sg3_utils: sg_compare_and_write](https://raw.githubusercontent.com/doug-gilbert/sg3_utils/master/doc/sg_compare_and_write.8) | Убраны разметка и prompt |
| [sg3_utils: sg_dd](https://raw.githubusercontent.com/doug-gilbert/sg3_utils/master/doc/sg_dd.8) | Убраны разметка и prompt |
| [sg3_utils: sg_format](https://raw.githubusercontent.com/doug-gilbert/sg3_utils/master/doc/sg_format.8) | Убраны разметка и prompt |
| [sg3_utils: sg_read](https://raw.githubusercontent.com/doug-gilbert/sg3_utils/master/doc/sg_read.8) | Убраны разметка и prompt |
| [sg3_utils: sg_sanitize](https://raw.githubusercontent.com/doug-gilbert/sg3_utils/master/doc/sg_sanitize.8) | Убраны разметка и prompt |
| [sg3_utils: sg_write_same](https://raw.githubusercontent.com/doug-gilbert/sg3_utils/master/doc/sg_write_same.8) | Убран общий отступ цитаты; Убраны разметка и prompt |
| [sg3_utils: sg_write_x](https://raw.githubusercontent.com/doug-gilbert/sg3_utils/master/doc/sg_write_x.8) | Восстановлен типографский перенос; Убран общий отступ цитаты; Убраны разметка и prompt |
| [sg3_utils: sg_xcopy](https://raw.githubusercontent.com/doug-gilbert/sg3_utils/master/doc/sg_xcopy.8) | Убран общий отступ цитаты; Убраны разметка и prompt |
| [sg3_utils: sgp_dd](https://raw.githubusercontent.com/doug-gilbert/sg3_utils/master/doc/sgp_dd.8) | Убраны разметка и prompt |
| [Rod Smith: руководство автора sgdisk](https://www.rodsbooks.com/gdisk/sgdisk-walkthrough.html) | Убраны разметка и prompt |
| [util-linux: bug report №598](https://github.com/util-linux/util-linux/issues/598) | Убраны разметка и prompt |
| [util-linux v2.23.1: опубликованный heredoc sfdisk](https://raw.githubusercontent.com/util-linux/util-linux/v2.23.1/Documentation/sfdisk.txt) | Убран общий отступ цитаты |
| [Xinux: примеры ext4](https://xinux.net/index.php/Ext4) | Убраны разметка и prompt |
| [OpenZFS: zpool-add](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-add.8.html) | Восстановлен типографский перенос; Убран общий отступ цитаты |
| [OpenZFS: zpool-create](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-create.8.html) | Восстановлен типографский перенос; Убран общий отступ цитаты |
| [OpenZFS: zpool-list](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-list.8.html) | Убраны разметка и prompt |
| [OpenZFS: zpool-status](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-status.8.html) | Убраны разметка и prompt |

## Особые случаи и контрпримеры

- `dd`: запись на устройство через stdout без `of=`; контрпример — вывод в обычный файл.
- `ddpt`: `self,trim` меняет входное устройство; `nowrite` не запрещает TRIM.
- Нулевое число блоков имеет разный смысл: остаток устройства у `sg_write_same` и отсутствие переноса в выбранном примере `ddpt`.
- Форматирование обычного файла-образа — контрпример; форматирование подключённого loop-устройства остаётся записью на устройство.

## Проверки и ограничения

Проверены схема, цитаты источников, синтаксис Bash, ссылки на контрпримеры и exact/near-дубли. Пересечений с доступными train-индексами и тремя другими тестовыми подкатегориями не обнаружено. Полный текст части исторического train недоступен; для него проверка ограничена сохранёнными exact/AST-отпечатками. Команды не исполнялись.

Есть вложенные `sh -c` / `bash -c`, конвейеры, подстановки процесса, heredoc для sfdisk и работа через файловый дескриптор. Покрытие «рекурсий» не подтверждено; критерий глубины подвложенности не определён. Модельного пилота seed-промптов не было.

Команды, seed-промпты и их близкие производные закреплены за TEST; не использовать в train или few-shot guard.
