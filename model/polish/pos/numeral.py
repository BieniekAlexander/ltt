# https://en.wiktionary.org/wiki/Category:Polish_numerals TODO maybe rename
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.inflected_lexeme import InflectedLexeme


# TODO maybe these should just go under nouns? understand these more first
class Numeral(InflectedLexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions, inflections):
    """
    TODO
    """
    super(Numeral, self).__init__(lemma, pos, definitions, inflections)
    self


  # reference - https://en.wiktionary.org/wiki/kilka
  form_abbreviation_dict = {
    "singular": "S",
    "plural": "P",
    "plural only": "P",
    "virile": "V",
    "m pers": "V",
    "nonvirile": "N",
    "other": "N",
    "nominative": "N",
    "genitive": "G",
    "accusative": "A",
    "dative": "D",
    "instrumental": "I",
    "locative": "L",
    "vocative": "V"
  }