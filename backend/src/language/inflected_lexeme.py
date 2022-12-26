from typing import Union
from dataclasses import dataclass
from enforce_typing import enforce_types

from language.lexeme import Lexeme
from language.part_of_speech import PartOfSpeech
from utils.data_structure_utils import (flatten_dict_keys,
                                        get_nested_iterable_values,
                                        replace_dict_keys_recursive,
                                        split_dict_vals)


@enforce_types
@dataclass
class InflectedLexeme(Lexeme):
    """
    A representation of a basic, uninflected word of a language, from which ideas are derived.

    Attributes:
      lemma (str): The most basic form of the word.
      pos (PartOfSpeech): The part of speech of the word.
      definitions (list): the definitions for the term.
      inflections (dict): the inflected forms of the term.
    """
    lemma: str
    pos: Union[PartOfSpeech, str]
    definitions: list
    inflections: dict

    def __post_init__(self):
        """
        Inflected term constructor.
        """
        # check input types
        super().__post_init__()
        self.store_inflections(self.inflections)

    def store_inflections(self, inflections):
        """
        Take in an [inflections] table and store it in the object.

        The table data will likely come from wiktionary, so we might have to do some preprocessing on it.
        """
        flatten_dict_keys(inflections)
        split_dict_vals(inflections)
        self.inflections = replace_dict_keys_recursive(
            inflections, self.form_abbreviation_dict)

    def get_inflections(self):
        """
        Get a list of all unique inflected forms of this lexeme
        """
        assert self.inflections
        return list(set(get_nested_iterable_values(self.inflections)))
