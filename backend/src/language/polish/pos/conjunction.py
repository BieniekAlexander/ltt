from enforce_typing import enforce_types
from dataclasses import dataclass
from typing import Union

from language.lexeme import Lexeme
from language.part_of_speech import PartOfSpeech


@enforce_types
@dataclass
class Conjunction(Lexeme):
    """Polish Conjunction

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
        Test assertions of polish conjunction state
        """    
        super().__post_init__()
