# https://en.wikipedia.org/wiki/Comparison_(grammar)
from enum import Enum, auto

class Degree(str, Enum):
    POSITIVE: str = "POSITIVE"
    COMPARATIVE: str = "COMPARATIVE"
    SUPERLATIVE: str = "SUPERLATIVE"