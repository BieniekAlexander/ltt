import sys, os
from model.inflected_lexeme import InflectedLexeme

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.lexeme import Lexeme
from utils.data_structure_utils import replace_dict_keys_recursive


class Interjection(Lexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions):
    """
    TODO
    """
    super(Interjection, self).__init__(lemma, pos, definitions)