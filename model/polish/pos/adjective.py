# https://en.wiktionary.org/wiki/Category:Polish_adjectives
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.inflected_lexeme import InflectedLexeme
from model.polish.feat.degree import Degree
from model.model_errors import LexemeValidationError


# TODO handle comparative and superlative?
class Adjective(InflectedLexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions, inflections, degree, positive=[], comparative=[], superlative=[], adverb=[], not_comparable=False):
    """
    TODO
    """
    if degree and not isinstance(degree, Degree):
      degree = Degree[degree.upper()]

    if not self.validate_degrees(degree, positive, comparative, superlative, not_comparable):
      args = {'degree': degree, 'positive': positive, 'comparative': comparative, 'superlative': superlative, 'not_comparable': not_comparable}
      raise LexemeValidationError(lemma, pos, args, f"The adjective had invalid arguments regarding degree - {args}")

    # load in fields
    super(Adjective, self).__init__(lemma, pos, definitions, inflections)
    self.degree = degree
    self.positive = positive
    self.comparative = comparative
    self.superlative = superlative
    self.adverb = adverb
    self.not_comparable = not_comparable


  def validate_degrees(self, degree, positive, comparative, superlative, not_comparable):
    """
    Checks that the form of this adjective is valid and doesn't overlap with references to other degrees.
    """
    if not degree or not isinstance(degree, Degree): # degree not supplied
      return False
    
    if not_comparable and (degree is not Degree.POSITIVE or comparative or superlative): # if the form is not comparable, then...
      return False

    if not not_comparable:
      if (degree is Degree.POSITIVE and (positive or not comparative or not superlative)) \
          or (degree is Degree.COMPARATIVE and (not positive or comparative)) \
          or (degree is Degree.SUPERLATIVE and (not positive or superlative)):
        return False
    
    # everything checks out
    return True

    
  # reference - https://en.wiktionary.org/wiki/czerwony#Declension_2
  form_abbreviation_dict = {
    "singular": "S",
    "plural": "P",
    "masculine personal/animate": "A",
    "masculine inanimate": "I",
    "neuter": "N",
    "feminine": "F",
    "virile": "V",
    "nonvirile": "N",
    "nominative": "N",
    "genitive": "G",
    "accusative": "A",
    "dative": "D",
    "instrumental": "I",
    "locative": "L",
    "vocative": "V"
  }


  schema = {
    "S": {
      "A": {
        "N": None,
        "G": None,
        "D": None,
        "A": None,
        "I": None,
        "L": None,
        "V": None
      },
      "I": {
        "N": None,
        "G": None,
        "D": None,
        "A": None,
        "I": None,
        "L": None,
        "V": None
      },
      "N": {
        "N": None,
        "G": None,
        "D": None,
        "A": None,
        "I": None,
        "L": None,
        "V": None
      },
      "F": {
        "N": None,
        "G": None,
        "D": None,
        "A": None,
        "I": None,
        "L": None,
        "V": None
      }
    },
    "P": {
      "V": {
        "N": None,
        "G": None,
        "D": None,
        "A": None,
        "I": None,
        "L": None,
        "V": None
      },
      "N": {
        "N": None,
        "G": None,
        "D": None,
        "A": None,
        "I": None,
        "L": None,
        "V": None
      }
    }
  }