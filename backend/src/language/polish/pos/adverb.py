# https://en.wiktionary.org/wiki/Category:Polish_adverbs
import sys, os



from language.lexeme import Lexeme
from language.polish.feat.degree import Degree
from language.model_errors import LexemeError

# TODO handle comparative and superlative?
class Adverb(Lexeme):
  def __init__(self, lemma, pos, definitions, degree, positive=[], comparative=[], superlative=[], adjective=[], not_comparable=False):
    """[summary]

    Args:
        lemma ([type]): [description]
        pos ([type]): [description]
        definitions ([type]): [description]
        degree ([type]): [description]
        positive (list, optional): [description]. Defaults to [].
        comparative (list, optional): [description]. Defaults to [].
        superlative (list, optional): [description]. Defaults to [].
        adjective (list, optional): [description]. Defaults to [].
        not_comparable (bool, optional): [description]. Defaults to False.

    Raises:
        LexemeError: [description]
    """
    if degree and not isinstance(degree, Degree):
      degree = Degree[degree.upper()]

    if not self.validate_degrees(degree, positive, comparative, superlative, not_comparable):
      args = {'degree': degree, 'positive': positive, 'comparative': comparative, 'superlative': superlative, 'not_comparable': not_comparable}
      raise LexemeError(lemma, pos, args, f"The adverb had invalid arguments regarding degree - {args}")

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