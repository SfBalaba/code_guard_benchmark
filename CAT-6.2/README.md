# CAT-6.2 — Variable Concatenation & Indirection

v0.5, 19.11.2026. [commands.csv](commands.csv) содержит 250 TEST-записей для GNU/Linux и Bash 5.2 с `category=CAT-6` и `risk=CAT-6.2`. В [seeds/](seeds/README.md) находятся 20 отдельных TRAIN-промптов для безопасных Bash-контрпримеров и текстовых сценариев разметки риска.

Классы, 126 allow, 48 deny, 76 ask. Severity, 126 low, 12 medium, 84 high, 28 critical. Жёлтая зона, ask для известных операций с репозиториями, production-ресурсами и системными настройками, требующих одобрения. Неизвестные переменные не заменяются классом ask.

Источники, 64 real из опубликованных тестов и инструкций, 186 synthetic. Ссылки, правки, уведомления об авторских правах и тексты лицензий приведены ниже. Инцидентная телеметрия и local не представлены. В поле `command` внешние хосты в real-примерах заменены документационными адресами. Случайный отбор не применялся.

Синтетика получена по спецификациям текущей сессии Codex семейства GPT-6 с детерминированной сборкой Bash. Точный model ID недоступен, отдельных API-вызовов модели не было. TEST-задания зафиксированы до формирования команд. Полные TEST-промпты находятся в поле `seed`. При сборке TRAIN эти промпты и соответствующие примеры исключаются.

Утилиты, :, at, auditctl, cat, chmod, chown, cp, crontab, curl, docker, echo, eval, find, git, grep, helm, install, ip, iptables, kill, kubectl, loginctl, ls, mkdir, mount, nft, nmcli, passwd, pkill, printf, resolvectl, rm, sed, sleep, sysctl, systemctl, tr, ufw, umount, useradd, wget, whoami, zfs. Для соответствующих сценариев нужны стандартные CLI Git, Docker Compose v2, Kubernetes, Helm, systemd, util-linux, shadow-utils и OpenZFS. Действие оценивается как запрос, успешное выполнение и наличие production-ресурсов не предполагаются.

Обфускация, кавычки и переносы строк сохранены. Есть массивы, косвенное обращение, eval, bash -c, исполняемый heredoc и конечная рекурсия. У каждого deny и ask есть безопасный аналог той же утилитой, максимум пять вариаций рецепта с контрпримерами. Сборочные способы встречаются и в безопасных, и в рискованных строках.

Проверены происхождение, подготовка временных файлов, разметка, синтаксис с GNU Bash 5.2 в режиме `-n`, точные и близкие повторы в пределах статического анализа. Разделение с доступным локальным TRAIN проверено по полным командам и раскрытым операциям, с учётом эквивалентных опций GNU rm. При ручной сверке десяти пар с совпадающими раскрытыми операциями выявлены различия в синтаксисе и способе обращения к переменным. Сами команды не исполнялись. Статический анализ ограничен поддерживаемой грамматикой. Будущий TRAIN и независимая экспертная приёмка недоступны.

## Источники TEST

Источники относятся к `CAT-6.2`. Ссылки на репозитории ведут на использованные снимки. Правки перечислены для записей, где они применялись.

| Источник | Тип | Real | Synthetic | Лицензии | Правки |
| --- | --- | ---: | ---: | --- | --- |
| [agenttrailhq/guard @ `299f8a7b2e`](https://github.com/agenttrailhq/guard/tree/299f8a7b2ebf1352cd6bc54744738f52b0103082) | тесты | 4 | 0 | Apache-2.0 | без содержательных правок |
| [delphisecurity/xaidr @ `c2fd10d169`](https://github.com/delphisecurity/xaidr/tree/c2fd10d16932513ce56a31978d818c300b16d74d) | тесты | 1 | 0 | Apache-2.0 | без содержательных правок |
| [emiliano-go/trustsight @ `7107f47876`](https://github.com/emiliano-go/trustsight/tree/7107f478762533f97eee7e66c856dd26ce6f562b) | тесты | 5 | 0 | MIT | замена внешних хостов на документационные адреса, удаление маркеров строк diff |
| [everruns/bashkit @ `bb6e17f4c8`](https://github.com/everruns/bashkit/tree/bb6e17f4c8d8ae3048ff0a2dcf9e6ae8757a56b4) | тесты | 1 | 0 | MIT | без содержательных правок |
| [garrytan/gstack @ `f79a8905c7`](https://github.com/garrytan/gstack/tree/f79a8905c75fbc7e436e274d0cdbac8ecdeec458) | тесты | 3 | 0 | MIT | без содержательных правок |
| [HoshimuraYuto/credential-guard @ `da2c426ce0`](https://github.com/HoshimuraYuto/credential-guard/tree/da2c426ce0c4539fa8bcd0304f8750e9f1e7e84b) | тесты | 3 | 0 | MIT | замена внешних хостов на документационные адреса |
| [manuelschipper/nah @ `7230be14c0`](https://github.com/manuelschipper/nah/tree/7230be14c0586c8ebe9a6be0c4d9a43f4949216a) | безопасные примеры, тесты | 28 | 0 | MIT | без содержательных правок |
| [NousResearch/hermes-agent @ `f7e2898aae`](https://github.com/NousResearch/hermes-agent/tree/f7e2898aaefc8f967dbf7345e3999a65672fe60e) | тесты | 8 | 0 | MIT | замена внешних хостов на документационные адреса |
| [openclaw/openclaw @ `757fe86309`](https://github.com/openclaw/openclaw/tree/757fe86309febb529274ef7ce10f3b94b862e408) | тесты | 1 | 0 | MIT | без содержательных правок |
| [ryo-ebata/cc-audit @ `59355682cd`](https://github.com/ryo-ebata/cc-audit/tree/59355682cd92c5af8413b8a0be609573f496c681) | тесты | 3 | 0 | MIT | без содержательных правок |
| [silv3rshi3ld/commandguard @ `283e366e36`](https://github.com/silv3rshi3ld/commandguard/tree/283e366e36dec6744f6141fdf08d4e2cff688ef7) | тесты | 1 | 0 | MIT | без содержательных правок |
| [swisskyrepo/PayloadsAllTheThings @ `08ea40e77d`](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/08ea40e77db3f42ef8f20c65196f3936a19b6c86) | инструкции | 3 | 0 | MIT | без содержательных правок |
| [tannermidd/specpi-jev-guard @ `da63a13ab7`](https://github.com/tannermidd/specpi-jev-guard/tree/da63a13ab7b7b7f3a39799e284a2f103f992477c) | тесты | 3 | 0 | MIT | без содержательных правок |

Синтетика без внешнего первоисточника: 186 записей. Метод и сведения о модели указаны выше.

## Атрибуция и лицензии

Опубликованные фрагменты сохраняют лицензии своих источников. Ниже приведены исходные уведомления и тексты лицензий.

### manuelschipper/nah

License: https://raw.githubusercontent.com/manuelschipper/nah/7230be14c0586c8ebe9a6be0c4d9a43f4949216a/LICENSE

```text
MIT License

Copyright (c) 2026 Manuel Schipper

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### delphisecurity/xaidr

License: https://raw.githubusercontent.com/delphisecurity/xaidr/c2fd10d16932513ce56a31978d818c300b16d74d/LICENSE

```text
Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright 2026 Delphi Security Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

Original NOTICE:

```text
xaidr
Copyright 2026 Delphi Security Inc.

This product includes software developed at Delphi Security Inc.

This product includes data from the Public Suffix List
(https://publicsuffix.org/list/public_suffix_list.dat), vendored as
xaidr/value_origin/_psl_data.py. That file is subject to the terms of the
Mozilla Public License, v. 2.0. A copy of the MPL is available at
https://mozilla.org/MPL/2.0/.

This product includes data derived from the Unicode Character Database and
the Unicode IDNA Compatibility Processing tables (UTS #46), version 13.0.0,
vendored as xaidr/value_origin/_idna_data.py. Copyright (c) 1991-2020
Unicode, Inc. Distributed under the Unicode License Agreement - Data Files
and Software (https://www.unicode.org/license.txt).
```

### ryo-ebata/cc-audit

License: https://raw.githubusercontent.com/ryo-ebata/cc-audit/59355682cd92c5af8413b8a0be609573f496c681/LICENSE

```text
MIT License

Copyright (c) 2024-2025 Ryo Ebata

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### openclaw/openclaw

License: https://raw.githubusercontent.com/openclaw/openclaw/757fe86309febb529274ef7ce10f3b94b862e408/LICENSE

```text
MIT License

Copyright (c) 2025 Peter Steinberger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### HoshimuraYuto/credential-guard

License: https://raw.githubusercontent.com/HoshimuraYuto/credential-guard/da2c426ce0c4539fa8bcd0304f8750e9f1e7e84b/LICENSE

```text
MIT License

Copyright (c) 2026 Hoshimura Yuto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### silv3rshi3ld/commandguard

License: https://raw.githubusercontent.com/silv3rshi3ld/commandguard/283e366e36dec6744f6141fdf08d4e2cff688ef7/LICENSE-MIT

```text
MIT License

Copyright (c) 2026 CommandGuard contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### NousResearch/hermes-agent

License: https://raw.githubusercontent.com/NousResearch/hermes-agent/f7e2898aaefc8f967dbf7345e3999a65672fe60e/LICENSE

```text
MIT License

Copyright (c) 2025 Nous Research

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### tannermidd/specpi-jev-guard

License: https://raw.githubusercontent.com/tannermidd/specpi-jev-guard/da63a13ab7b7b7f3a39799e284a2f103f992477c/LICENSE

```text
MIT License

Copyright (c) 2026 Tanner Middleton

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### swisskyrepo/PayloadsAllTheThings

License: https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/08ea40e77db3f42ef8f20c65196f3936a19b6c86/LICENSE

```text
MIT License

Copyright (c) 2019 Swissky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### agenttrailhq/guard

License: https://raw.githubusercontent.com/agenttrailhq/guard/299f8a7b2ebf1352cd6bc54744738f52b0103082/LICENSE

```text
Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
```

### emiliano-go/trustsight

License: https://raw.githubusercontent.com/emiliano-go/trustsight/7107f478762533f97eee7e66c856dd26ce6f562b/LICENSE

```text
MIT License

Copyright (c) 2026 Emiliano G.O.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### everruns/bashkit

License: https://raw.githubusercontent.com/everruns/bashkit/bb6e17f4c8d8ae3048ff0a2dcf9e6ae8757a56b4/LICENSE

```text
MIT License

Copyright (c) 2024-2026 Everruns

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Original NOTICE:

```text
Bashkit
Copyright (c) 2024-2026 Everruns

This product is an independent implementation of a sandboxed bash interpreter.

================================================================================
ACKNOWLEDGMENTS
================================================================================

Bashkit is an independent implementation that draws design inspiration from
several open source projects. We gratefully acknowledge:

--------------------------------------------------------------------------------
just-bash
--------------------------------------------------------------------------------
Copyright (c) Vercel Inc.
Licensed under the Apache License, Version 2.0

Repository: https://github.com/vercel/just-bash

Bashkit's sandboxing architecture and multi-tenant design was inspired by
just-bash's approach to safe bash execution. No code was copied; this is an
independent Rust implementation.

--------------------------------------------------------------------------------
Oils (formerly Oil Shell)
--------------------------------------------------------------------------------
Copyright (c) Andy Chu and contributors
Licensed under the Apache License, Version 2.0

Repository: https://github.com/oilshell/oil

The Oils project's comprehensive bash compatibility testing approach inspired
our spec test methodology. Our test cases are independently written following
similar testing principles.

--------------------------------------------------------------------------------
One True AWK
--------------------------------------------------------------------------------
Copyright (c) Lucent Technologies
Licensed under the Lucent Public License

Repository: https://github.com/onetrueawk/awk

The behavior and semantics of our AWK builtin implementation are informed by
the One True AWK specification. Our implementation is written from scratch in
Rust using the original AWK language definition as reference.

--------------------------------------------------------------------------------
jq
--------------------------------------------------------------------------------
Copyright (c) Stephen Dolan
Licensed under the MIT License

Repository: https://github.com/jqlang/jq

Our jq builtin aims for compatibility with jq's query syntax and behavior.
The implementation uses the jaq Rust crates (MIT licensed) rather than jq
source code directly.

--------------------------------------------------------------------------------
BashBox
--------------------------------------------------------------------------------
Copyright (c) Pushpak Chhajed
Licensed under the MIT License

Repository: https://github.com/shipfastlabs/bashbox

The spec cases in crates/bashkit/tests/spec_cases/bash/bashbox-*.test.sh are
copied from BashBox's test suite (script and expected stdout, recorded from
GNU bash). The full MIT license text is in THIRD_PARTY_LICENSES/MIT.txt.

================================================================================
RUST DEPENDENCIES
================================================================================

Bashkit uses the following notable Rust crates. Full dependency information
is available via `cargo tree` or in the Cargo.lock file.

jaq-core, jaq-std (MIT)
  - JQ expression parsing and evaluation
  - Copyright (c) Michael Färber

jaq-json (MIT), vendored in crates/bashkit/src/builtins/jq/jaq_json/
  - JSON value type for jq, with bashkit resource-limit patches
  - Copyright (c) Michael Färber
  - Repository: https://github.com/01mf02/jaq

uutils/coreutils fmt (MIT), vendored in crates/bashkit/src/builtins/fmt/
  - linebreak.rs and parasplit.rs: fmt line breaking and paragraph splitting
  - Copyright (c) uutils developers
  - Repository: https://github.com/uutils/coreutils

grep, grep-regex, grep-searcher (MIT/Apache-2.0)
  - Text search functionality
  - Part of the ripgrep project by Andrew Gallant

tokio (MIT)
  - Async runtime
  - Copyright (c) Tokio Contributors

serde, serde_json (MIT/Apache-2.0)
  - Serialization framework
  - Copyright (c) David Tolnay and serde contributors

regex (MIT/Apache-2.0)
  - Regular expression engine
  - Copyright (c) The Rust Project Developers

All dependencies are permissively licensed (MIT, Apache-2.0, BSD, ISC, Zlib).
See THIRD_PARTY_LICENSES/ for full license texts of key dependencies.

================================================================================
INDEPENDENT IMPLEMENTATION NOTICE
================================================================================

Bashkit is an independent implementation of a bash-like shell interpreter.
It is not affiliated with, endorsed by, or derived from:

- GNU Bash (GPL licensed)
- The original Bourne shell
- Any of the projects mentioned above

The shell syntax parser, interpreter, virtual filesystem, and all builtins
(except where noted) are original implementations written in Rust. The jq
value type in crates/bashkit/src/builtins/jq/jaq_json/ is a modified copy of
jaq-json (MIT, Michael Färber), see RUST DEPENDENCIES above. The fmt line
breaker in crates/bashkit/src/builtins/fmt/ is a modified copy of uutils
coreutils fmt (MIT, uutils developers).
```

### garrytan/gstack

License: https://raw.githubusercontent.com/garrytan/gstack/f79a8905c75fbc7e436e274d0cdbac8ecdeec458/LICENSE

```text
MIT License

Copyright (c) 2026 Garry Tan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
