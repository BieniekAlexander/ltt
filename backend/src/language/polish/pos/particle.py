from enforce_typing import enforce_types
from dataclasses import dataclass
from typing import Union

from language.lexeme import Lexeme
from language.part_of_speech import PartOfSpeech

@enforce_types
@dataclass
class Particle(Lexeme):
    """Polish Particle

    Args:
        lemma ([type]): [description]
        pos ([type]): [description]
        definitions ([type]): [description]
    """
    lemma: str
    pos: Union[PartOfSpeech, str]
    definitions: list[str]

    def __post_init__(self):
        """
        Run checks
        """
        super().__post_init__()
