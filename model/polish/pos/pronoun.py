import sys, os
from model.inflected_lexeme import InflectedLexeme

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.lexeme import Lexeme
from utils.data_structure_utils import replace_dict_keys_recursive


# TODO there's probably a limited set of these terms (with some alternate forms, e.g. swoje -> swe), how to handle this?
# TODO will probably involve little, if any, scraping
class Pronoun(InflectedLexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions, inflections):
    """
    TODO
    """
    super(Pronoun, self).__init__(lemma, pos, definitions, inflections)