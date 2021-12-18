from enum import Enum, auto

class Gender(str, Enum):
    MALE: str = "MALE"
    FEMALE: str = "FEMALE"
    NEUTER: str = "NEUTER"