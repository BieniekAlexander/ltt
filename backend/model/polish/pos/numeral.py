# https://en.wiktionary.org/wiki/Category:Polish_numerals TODO maybe rename
import sys, os


from model.inflected_lexeme import InflectedLexeme


# TODO maybe these should just go under nouns? understand these more first
class Numeral(InflectedLexeme):
  def __init__(self, lemma, pos, definitions, inflections):
    """[summary]

    Args:
        lemma ([type]): [description]
        pos ([type]): [description]
        definitions ([type]): [description]
        inflections ([type]): [description]
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