# https://en.wiktionary.org/wiki/Category:Polish_adverbs
import sys, os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.lexeme import Lexeme
from model.polish.feat.degree import Degree
from model.model_errors import LexemeValidationError

# TODO handle comparative and superlative?
class Adverb(Lexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions, degree, positive=[], comparative=[], superlative=[], adjective=[], not_comparable=False):
    """
    TODO
    """
    if degree and not isinstance(degree, Degree):
      degree = Degree[degree.upper()]

    if not self.validate_degrees(degree, positive, comparative, superlative, not_comparable):
      args = {'degree': degree, 'positive': positive, 'comparative': comparative, 'superlative': superlative, 'not_comparable': not_comparable}
      raise LexemeValidationError(lemma, pos, args, f"The adverb had invalid arguments regarding degree - {args}")

    super(Adverb, self).__init__(lemma, pos, definitions)
    self.degree = degree
    self.positive = positive
    self.comparative = comparative
    self.superlative = superlative
    self.not_comparable = not_comparable


  def validate_degrees(self, degree, positive, comparative, superlative, not_comparable):
    """
    Checks that the form of this adverb is valid and doesn't overlap with references to other degrees.
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