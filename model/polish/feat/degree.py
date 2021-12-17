# https://en.wikipedia.org/wiki/Comparison_(grammar)
from enum import Enum, auto

class Degree(str, Enum):
    POSITIVE = auto()
    COMPARATIVE = auto()
    SUPERLATIVE = auto()