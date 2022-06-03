import json, sys, os
from enum import Enum, auto


from language.part_of_speech import PartOfSpeech
from language.lexeme import Lexeme
from utils.data_structure_utils import replace_dict_keys_recursive, flatten_dict_keys, split_dict_vals, get_nested_iterable_values


class InflectedLexeme(Lexeme):
  """
  A representation of a basic, uninflected word of a language, from which ideas are derived.

  Attributes:
    lemma (str): The most basic form of the word.
    pos (PartOfSpeech): The part of speech of the word.
  """
  def __init__(self, lemma, pos, definitions, inflections):
    """
    Inflected term constructor.
    """
    # check input types
    assert isinstance(pos, PartOfSpeech) or isinstance(pos, str)
    assert isinstance(pos, str)
    assert isinstance(definitions, list)
    assert isinstance(inflections, dict)

    super(InflectedLexeme, self).__init__(lemma, pos, definitions)
    self.store_inflections(inflections)


  def store_inflections(self, inflections):
    """
    Take in an [inflections] table and store it in the object.

    The table data will likely come from wiktionary, so we might have to do some preprocessing on it.
    """
    flatten_dict_keys(inflections)
    split_dict_vals(inflections)
    self.inflections = replace_dict_keys_recursive(inflections, self.form_abbreviation_dict)


  def get_inflections(self):
    """
    Get a list of all unique inflected forms of this lexeme
    """
    assert self.inflections
    return list(set(get_nested_iterable_values(self.inflections)))