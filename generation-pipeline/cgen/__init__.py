"""CodeGuard-Bench: каркас генерации синтетических bash-команд.

Конвейер: load_seeds -> generate -> clean -> dedup -> validate -> export (+ report).
Код описывает КАК генерировать; ЧТО генерировать задаётся конфигом.
"""

__version__ = "0.1.0"
