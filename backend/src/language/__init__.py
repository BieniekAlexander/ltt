# imports
# Polish
from language.polish.pos.adjective import Adjective as PlAdjective
from language.polish.pos.adverb import Adverb as PlAdverb
from language.polish.pos.conjunction import Conjunction as PlConjunction
from language.polish.pos.interjection import Interjection as PlInterjection
from language.polish.pos.noun import Noun as PlNoun
from language.polish.pos.numeral import Numeral as PlNumeral
from language.polish.pos.particle import Particle as PlParticle
from language.polish.pos.preposition import Preposition as PlPreposition
from language.polish.pos.pronoun import Pronoun as PlPronoun
from language.polish.pos.verb import Verb as PlVerb

MODEL_CLASS_MAP = {
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
