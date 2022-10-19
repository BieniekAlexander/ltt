from enum import Enum


class Case(str, Enum):
    NOMINATIVE: str = "NOMINATIVE"
    GENITIVE: str = "GENITIVE"
    ACCUSATIVE: str = "ACCUSATIVE"
    INSTRUMENTAL: str = "INSTRUMENTAL"
    LOCATIVE: str = "LOCATIVE"
    DATIVE: str = "DATIVE"
    VOCATIVE: str = "VOCATIVE"
