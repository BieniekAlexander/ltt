# https://en.wiktionary.org/wiki/Category:Polish_conjunctions
import sys, os
from model.inflected_lexeme import InflectedLexeme


from model.lexeme import Lexeme


class Conjunction(Lexeme):
  def __init__(self, lemma, pos, definitions):
    """[summary]

    Args:
        lemma ([type]): [description]
        pos ([type]): [description]
        definitions ([type]): [description]
    """
    super(Conjunction, self).__init__(lemma, pos, definitions)