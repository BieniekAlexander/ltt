from enum import Enum, auto

class Animacy(str, Enum):
    ANIMATE: str = "ANIMATE"
    INANIMATE: str = "INANIMATE"