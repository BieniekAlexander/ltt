#%% imports
import sys, os


# abstract - for testing purposes
from model.lexeme import Lexeme

# Polish
from model.polish.pos.adjective import Adjective as PlAdjective
from model.polish.pos.adverb import Adverb as PlAdverb
from model.polish.pos.conjunction import Conjunction as PlConjunction
from model.polish.pos.numeral import Numeral as PlNumeral
from model.polish.pos.particle import Particle as PlParticle
from model.polish.pos.interjection import Interjection as PlInterjection
from model.polish.pos.noun import Noun as PlNoun
from model.polish.pos.preposition import Preposition as PlPreposition
from model.polish.pos.pronoun import Pronoun as PlPronoun
from model.polish.pos.verb import Verb as PlVerb


model_class_map = {
  "POLISH": {
    "ADJECTIVE": PlAdjective,
    "ADVERB": PlAdverb,
    "CONJUNCTION": PlConjunction,
    "NUMERAL": PlNumeral,
    "PARTICLE": PlParticle,
    "INTERJECTION": PlInterjection,
    "NOUN": PlNoun,
    "PREPOSITION": PlPreposition,
    "PRONOUN": PlPronoun,
    "VERB": PlVerb
  },
  "TEST": {
    "ADJECTIVE": PlAdjective,
    "ADVERB": PlAdverb,
    "CONJUNCTION": PlConjunction,
    "NUMERAL": PlNumeral,
    "PARTICLE": PlParticle,
    "INTERJECTION": PlInterjection,
    "NOUN": PlNoun,
    "PREPOSITION": PlPreposition,
    "PRONOUN": PlPronoun,
    "VERB": PlVerb
  }
}