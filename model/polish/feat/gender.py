from enum import Enum, auto

class Gender(str, Enum):
    MALE = auto()
    FEMALE = auto()
    NEUTER = auto()