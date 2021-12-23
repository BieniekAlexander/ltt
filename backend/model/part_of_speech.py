from enum import Enum, auto


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

# TODO will this be the same across languages, or will I have to make it language specific?