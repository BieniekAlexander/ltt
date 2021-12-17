from enum import Enum, auto

class Personality(str, Enum):
    PERSONAL = auto()
    IMPERSONAL = auto()