from language.inflected_lexeme import InflectedLexeme


from language.lexeme import Lexeme
from utils.data_structure_utils import replace_dict_keys_recursive


# TODO there's probably a limited set of these terms (with some alternate forms, e.g. swoje -> swe), how to handle this?
class Pronoun(InflectedLexeme):
    def __init__(self, lemma, pos, definitions, inflections):
        """[summary]

        Args:
            lemma ([type]): [description]
            pos ([type]): [description]
            definitions ([type]): [description]
            inflections ([type]): [description]
        """
        super(Pronoun, self).__init__(lemma, pos, definitions, inflections)

    # reference - https://en.wiktionary.org/wiki/biec#Conjugation
    form_abbreviation_dict = {
        "singular": "S",
        "plural": "P",
        "masculine personal/animate": "A",
        "masculine inanimate": "I",
        "neuter": "N",
        "feminine": "F",
        "virile": "V",
        "vir pl": "V",
        "nonvirile": "N",
        "nvir pl": "N",
        "nominative": "N",
        "genitive": "G",
        "accusative": "A",
        "dative": "D",
        "instrumental": "I",
        "locative": "L",
        "vocative": "V"
    }
