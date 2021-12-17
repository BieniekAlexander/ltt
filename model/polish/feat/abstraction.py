# https://en.wiktionary.org/wiki/abstract_verb#English
from enum import Enum, auto

class Abstraction(str, Enum):
    INDETERMINATE = auto()
    DETERMINATE = auto()