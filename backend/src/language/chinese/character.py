from typing import Union
from dataclasses import dataclass
from enforce_typing import enforce_types
from bson import ObjectId

from language.lexeme import Lexeme
from language.part_of_speech import PartOfSpeech
from language.chinese.feat.writing_set import WritingSet

@enforce_types
@dataclass
class Character(Lexeme):
    """
    An individual chinese character

    Attributes:
      lemma (str): The most basic form of the word. For chinese, I'll represent this with a 
      pos (PartOfSpeech): The part of speech of the word.
      definitions (list): the definitions for the term.
      is_radical
      radicals
      variants
      forms
      romanizations
      stroke_counts
    """
    lemma: str
    pos: list[Union[PartOfSpeech, str]]
    definitions: list[str]
    is_radical: bool
    radicals: list[str]
    variants: list[str]
    forms: dict[str, str]
    romanizations: dict[str, str]
    stroke_counts: dict[str, int]

    def __post_init__(self):
        """
        Postprocess construction of chinese character
        """
        self.pos = [PartOfSpeech[p.upper()] if type(p)==str else p for p in self.pos]
        self.forms = {WritingSet[key.upper()]: self.forms[key] for key in self.forms}

        assert set(WritingSet) <= set(self.forms.keys())
        assert all(stroke_count>=1 for stroke_count in self.stroke_counts.values())

        super().__post_init__()