from typing import Union
from dataclasses import dataclass, field
from enforce_typing import enforce_types

from utils.data_structure_utils import get_nested_iterable_values
from language.lexeme import Lexeme
from language.part_of_speech import PartOfSpeech
from language.chinese.feat.writing_set import WritingSet

@enforce_types
@dataclass
class Character(Lexeme):
    """
    An individual chinese character

    Attributes:
      lemma (str): The most basic form of the word. For chinese, I'll represent this with the traditional form - see the README.md for more info
      pos (list[PartOfSpeech, str]): A list of the potential parts of speech of the character
      definitions (list): the definitions for the character
      is_radical (bool): whether or not this character is a radical
      radicals (list[str]): the radicals that this character is composed of, if it's not a radical itself
      variants (list[str]): the other ways that this character is written (i.e. radicals within other characters)
      written_forms (dict[str, str]): representation of the character in other writing sets
      romanizations (dict[str, str]): the ways that this character is romanized for speaking
      stroke_counts (dict[str, int]): the number of strokes this character takes
    """
    lemma: str
    pos: list[Union[PartOfSpeech, str]]
    definitions: list[str]
    is_radical: bool
    radicals: list[str]
    written_forms: dict[str, str]
    romanizations: dict[str, str]
    stroke_counts: dict[str, int]
    variants: list[str] = field(default_factory=list)

    def __post_init__(self):
        """
        Postprocess construction of chinese character
        """
        self.pos = list(filter(lambda p: p.upper() in list(PartOfSpeech), self.pos))
        self.pos = [PartOfSpeech[p.upper()] if type(p)==str else p for p in self.pos]
        self.written_forms = {WritingSet[key.upper()]: self.written_forms[key] for key in self.written_forms}
        self.stroke_counts = {WritingSet[key.upper()]: self.stroke_counts[key] for key in self.stroke_counts}

        assert set(WritingSet) >= set(self.written_forms.keys())
        assert set(WritingSet) >= set(self.stroke_counts.keys())
        # assert all(stroke_count>=1 for stroke_count in self.stroke_counts.values()) # TODO add this check?

        super().__post_init__()

    def to_bson(self):
        return {
        'lemma': self.lemma,
        'pos': self.pos,
        'definitions': self.definitions,
        'written_forms': dict(map(lambda x: (x.lower(), self.written_forms[x]), self.written_forms.keys())),
        'written_forms_list': list(set(get_nested_iterable_values(self.written_forms))), # TODO this isn't part of the data class, but I might need a list of values to make it searchable
        'romanizations': self.romanizations,
        'is_radical': self.is_radical,
        'stroke_counts': dict(map(lambda x: (x.lower(), self.stroke_counts[x]), self.stroke_counts.keys())),
        'radicals': self.radicals,
        'variants': self.variants
    }

    @enforce_types
    def from_bson(bson: dict):
        bson.pop("written_forms_list", None)
        bson.pop("_id", None)
        return Character(**bson)