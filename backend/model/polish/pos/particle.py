# https://en.wiktionary.org/wiki/Category:Polish_particles
import sys, os
from model.inflected_lexeme import InflectedLexeme


from model.lexeme import Lexeme


class Particle(Lexeme):
  def __init__(self, lemma, pos, definitions):
    """[summary]

    Args:
        lemma ([type]): [description]
        pos ([type]): [description]
        definitions ([type]): [description]
    """
    super(Particle, self).__init__(lemma, pos, definitions)