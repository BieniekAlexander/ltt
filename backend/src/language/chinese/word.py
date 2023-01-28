from dataclasses import dataclass
from enforce_typing import enforce_types
from utils.json_utils import JSONSerializable
from utils.data_structure_utils import get_nested_iterable_values
from typing import Union
from language.part_of_speech import PartOfSpeech
from language.chinese.feat.writing_set import WritingSet

@enforce_types
@dataclass
class Word(JSONSerializable):
    """
    A semantic grouping of chinese characters

    Attributes:
        lemma (str): A string containing all of the lemma forms of the characters that make up the string
        definitions (list[str]): A list of definitions for this word
        pos (list[Union[PartOfSpeech, str]]): The potential parts of speech for this word
        written_forms (dict[str, str]): The potential written forms of this word
        romanizations (dict[str, str]): The potential romanizations of this word
    """
    lemma: str
    definitions: list[str]
    pos: list[Union[PartOfSpeech, str]]
    written_forms: dict[Union[WritingSet, str], str]
    romanizations: dict[str, str]

    def __post_init__(self):
        """
        Postprocess construction of chinese character
        """
        self.pos = [PartOfSpeech[p.upper()] if type(p)==str else p for p in self.pos]
        self.written_forms = {WritingSet[key.upper()]: self.written_forms[key] for key in self.written_forms}

        assert set(WritingSet) <= set(self.written_forms.keys())

        assert len(self.lemma) > 0
        assert len(self.definitions) > 0

    def to_bson(self):
        return {
            'lemma': self.lemma,
            'definitions': self.definitions,
            'pos': self.pos,
            'written_forms': self.written_forms,
            'written_forms_list': list(set(get_nested_iterable_values(self.written_forms))), # TODO this isn't part of the data class, but I might need a list of values to make it searchable
            'romanizations': self.romanizations
        }

    @enforce_types
    def from_bson(bson: dict):
        bson.pop("written_forms_list", None)
        bson.pop('character_ids', None)
        bson.pop("_id", None)
        return Word(**bson)