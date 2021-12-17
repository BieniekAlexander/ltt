from enum import Enum, auto

class Animacy(str, Enum):
    ANIMATE = auto()
    INANIMATE = auto()