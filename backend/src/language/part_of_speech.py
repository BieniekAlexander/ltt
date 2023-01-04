from enum import Enum


class PartOfSpeech(str, Enum):
    ADJECTIVE: str = "ADJECTIVE"
    ADVERB: str = "ADVERB"
    AUXILIARY: str = "AUXILIARY"
    CONJUNCTION: str = "CONJUNCTION"
    INTERJECTION: str = "INTERJECTION"
    NOUN: str = "NOUN"
    NUMERAL: str = "NUMERAL"
    PARTICLE: str = "PARTICLE"
    PREPOSITION: str = "PREPOSITION"
    PRONOUN: str = "PRONOUN"
    VERB: str = "VERB"
    CLASSIFIER: str = "CLASSIFIER"
    COPULA: str = "COPULA"
