from enforce_typing import enforce_types
from dataclasses import dataclass
from typing import Union

from language.inflected_lexeme import InflectedLexeme
from language.part_of_speech import PartOfSpeech

# TODO maybe these should just go under nouns? understand these more first
@enforce_types
@dataclass
class Numeral(InflectedLexeme):
    """Polish numerals

    Args:
        lemma ([type]): [description]
        pos ([type]): [description]
        definitions ([type]): [description]
        inflections ([type]): [description]
    """
    lemma: str
    pos: Union[PartOfSpeech, str]
    definitions: list[str]
    inflections: dict

    def __post_init__(self):
        """
        Postprocess inflection fields
        """
        super().__post_init__()

    # reference - https://en.wiktionary.org/wiki/kilka
    form_abbreviation_dict = {
        "singular": "S",
        "plural": "P",
        "plural only": "P",
        "virile": "V",
        "m pers": "V",
        "nonvirile": "N",
        "other": "N",
        "nominative": "N",
        "genitive": "G",
        "accusative": "A",
        "dative": "D",
        "instrumental": "I",
        "locative": "L",
        "vocative": "V"
    }
