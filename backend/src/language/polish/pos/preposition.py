from enforce_typing import enforce_types
from dataclasses import dataclass, field
from typing import Union

from language.part_of_speech import PartOfSpeech
from language.lexeme import Lexeme
from language.polish.feat.case import Case

# TODO Prepositions are used with what cases?
@enforce_types
@dataclass
class Preposition(Lexeme):
    """Polish preposition

    Args:
        lemma ([type]): [description]
        pos ([type]): [description]
        definitions ([type]): [description]
        cases (list, optional): [description]. Defaults to [].
    """
    lemma: str
    pos: Union[PartOfSpeech, str]
    definitions: list[str]
    cases: list[Union[Case, str]] = field(default_factory=list)

    def __post_init__(self):
        """
        Run postprocessing after construction
        """
        self.cases = list(map(lambda x: Case[x.upper()], self.cases))

        super().__post_init__()
        
