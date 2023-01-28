from enum import Enum


class Recall(int, Enum):
    FORGET = -2
    SUSPEND = -1
    UNKNOWN = 0
    BAD = 1
    GOOD = 2
    EASY = 3
   
RECALL_INTERVALS = {
    0: 1,
    1: 1.2
}

RECALL_EASINESS_FACTORS = {
    0: 0.8,
    1: 0.85,
    2: 1.0,
    3: 1.15
}