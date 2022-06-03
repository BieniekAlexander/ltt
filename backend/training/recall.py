from enum import Enum


class Recall(str, Enum):
  UNKNOWN: str = "UNKNOWN"
  BAD: str = "BAD"
  OKAY: str = "OKAY"
  GOOD: str = "GOOD"
  KNOWN: str = "KNOWN"