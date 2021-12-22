import sys, os
from model.inflected_lexeme import InflectedLexeme
from model.polish.feat.case import Case

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.lexeme import Lexeme
from utils.data_structure_utils import replace_dict_keys_recursive


# TODO Prepositions are used with what cases?
class Preposition(Lexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions, cases=[]):
    """
    TODO
    """
    cases = list(map(lambda x: Case[x.upper()], cases))

    super(Preposition, self).__init__(lemma, pos, definitions)
    self.cases = cases