from enum import Enum


class PartOfSpeech(str, Enum):
    NOUN: str = "NOUN"
    PRONOUN: str = "PRONOUN"
    VERB: str = "VERB"
    ADJECTIVE: str = "ADJECTIVE"
    ADVERB: str = "ADVERB"
    CONJUNCTION: str = "CONJUNCTION"
    PREPOSITION: str = "PREPOSITION"
    INTERJECTION: str = "INTERJECTION"
    NUMERAL: str = "NUMERAL"
    PARTICLE: str = "PARTICLE"
