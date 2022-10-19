from enum import Enum


class Animacy(str, Enum):
    ANIMATE: str = "ANIMATE"
    INANIMATE: str = "INANIMATE"
