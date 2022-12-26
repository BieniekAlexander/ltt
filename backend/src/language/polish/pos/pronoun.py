from enforce_typing import enforce_types
from dataclasses import dataclass
from typing import Union

from language.part_of_speech import PartOfSpeech
from language.inflected_lexeme import InflectedLexeme

# TODO there's probably a limited set of these terms (with some alternate forms, e.g. swoje -> swe), how to handle this?
@enforce_types
@dataclass
class Pronoun(InflectedLexeme):
    """Polish pronoun

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
        Post construction processing
        """
        super().__post_init__()

    # reference - https://en.wiktionary.org/wiki/biec#Conjugation
    form_abbreviation_dict = {
        "singular": "S",
        "plural": "P",
        "masculine personal/animate": "A",
        "masculine inanimate": "I",
        "neuter": "N",
        "feminine": "F",
        "virile": "V",
        "vir pl": "V",
        "nonvirile": "N",
        "nvir pl": "N",
        "nominative": "N",
        "genitive": "G",
        "accusative": "A",
        "dative": "D",
        "instrumental": "I",
        "locative": "L",
        "vocative": "V"
    }
