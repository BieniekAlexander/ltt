import sys, os
from language.inflected_lexeme import InflectedLexeme


from language.lexeme import Lexeme
from utils.data_structure_utils import replace_dict_keys_recursive


class Interjection(Lexeme):
  def __init__(self, lemma, pos, definitions):
    """[summary]

    Args:
        lemma ([type]): [description]
        pos ([type]): [description]
        definitions ([type]): [description]
    """
    super(Interjection, self).__init__(lemma, pos, definitions)