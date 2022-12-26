from dataclasses import dataclass
from enforce_typing import enforce_types
from bson import ObjectId


@enforce_types
@dataclass
class Word:
    """
    A semantic grouping of chinese characters

    Attributes:
      TODO
    """
    characters: list[ObjectId]
    definitions: list[str]

    def __post_init__(self):
        """
        Postprocess construction of chinese word
        """
        assert len(self.characters) > 0
        assert len(self.definitions) > 0