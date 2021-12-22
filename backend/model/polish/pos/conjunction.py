# https://en.wiktionary.org/wiki/Category:Polish_conjunctions
import sys, os
from model.inflected_lexeme import InflectedLexeme

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.lexeme import Lexeme


class Conjunction(Lexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions):
    """
    TODO
    """
    super(Conjunction, self).__init__(lemma, pos, definitions)