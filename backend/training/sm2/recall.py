from enum import Enum


class Recall(int, Enum):
  UNKNOWN = 0
  BAD = 1
  OKAY = 2
  GOOD = 3
  GREAT = 4
  KNOWN = 5