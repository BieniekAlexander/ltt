# https://en.wiktionary.org/wiki/Category:Polish_particles
import sys, os
from model.inflected_lexeme import InflectedLexeme

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.lexeme import Lexeme


class Particle(Lexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions):
    """
    TODO
    """
    super(Particle, self).__init__(lemma, pos, definitions)