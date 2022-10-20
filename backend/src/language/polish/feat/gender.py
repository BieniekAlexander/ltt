from enum import Enum


class Gender(str, Enum):
    MALE: str = "MALE"
    FEMALE: str = "FEMALE"
    NEUTER: str = "NEUTER"
