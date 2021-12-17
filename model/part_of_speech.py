from enum import Enum, auto


class PartOfSpeech(str, Enum):
    NOUN = auto()
    PRONOUN = auto()
    VERB = auto()
    ADJECTIVE = auto()
    ADVERB = auto()
    CONJUNCTION = auto()
    PREPOSITION = auto()
    INTERJECTION = auto()
    NUMERAL = auto()
    PARTICLE = auto()

# TODO will this be the same across languages, or will I have to make it language specific?