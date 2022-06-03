from enum import Enum, auto

class Personality(str, Enum):
    PERSONAL: str = "PERSONAL"
    IMPERSONAL: str = "IMPERSONAL"