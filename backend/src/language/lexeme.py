from dataclasses import dataclass
from enforce_typing import enforce_types
from typing import Union

from utils.json_utils import JSONSerializable
from language.part_of_speech import PartOfSpeech
@enforce_types
@dataclass
class Lexeme(JSONSerializable):
    """
    A representation of a basic word of a language from which ideas are derived.

    Attributes:
        lemma (str): The most basic form of the word.
        pos (PartOfSpeech): The part of speech of the word.
        definitions (list): the definitions of the trm.
    """
    lemma: str
    pos: Union[PartOfSpeech, str]
    definitions: list
    
    def __post_init__(self):
        """
        Postprocess fields after construction
        """
        if type(self.pos) in [str, PartOfSpeech]:
            self.pos = PartOfSpeech[self.pos.upper()]

    def __eq__(self, other) -> bool:
        """
        Compare two terms for equality
        """
        assert issubclass(type(other), Lexeme)

        jsonSelf = self.to_json()
        jsonOther = other.to_json()
        return jsonSelf == jsonOther

    def to_bson(self):
        return self.to_json()

    @enforce_types
    def from_bson(bson: dict):
        from language import MODEL_CLASS_MAP
        bson.pop("_id", None)
        return MODEL_CLASS_MAP['POLISH'][bson.get('pos').upper()](**bson)