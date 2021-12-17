from enum import Enum, auto

class Case(str, Enum):
    NOMINATIVE = auto()
    GENITIVE = auto()
    ACCUSATIVE = auto()
    INSTRUMENTAL = auto()
    LOCATIVE = auto()
    DATIVE = auto()
    VOCATIVE = auto()