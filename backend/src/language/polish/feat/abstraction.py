# https://en.wiktionary.org/wiki/abstract_verb#English
from enum import Enum


class Abstraction(str, Enum):
    INDETERMINATE: str = "INDETERMINATE"
    DETERMINATE: str = "DETERMINATE"
