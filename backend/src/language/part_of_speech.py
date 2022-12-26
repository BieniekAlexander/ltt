from enum import Enum


class PartOfSpeech(str, Enum):
    ADJECTIVE: str = "ADJECTIVE"
    ADVERB: str = "ADVERB"
    AUXILIARY: str = "AUXILIARY" # TODO is this the same as a particle? https://classicaljapanese.wordpress.com/2014/02/26/explanation-of-auxiliary-verbs-and-particles-bound-forms/
    CONJUNCTION: str = "CONJUNCTION"
    INTERJECTION: str = "INTERJECTION"
    NOUN: str = "NOUN"
    NUMERAL: str = "NUMERAL"
    PARTICLE: str = "PARTICLE"
    PREPOSITION: str = "PREPOSITION"
    PRONOUN: str = "PRONOUN"
    VERB: str = "VERB"
