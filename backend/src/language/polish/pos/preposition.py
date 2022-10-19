from language.inflected_lexeme import InflectedLexeme
from language.polish.feat.case import Case


from language.lexeme import Lexeme
from utils.data_structure_utils import replace_dict_keys_recursive


# TODO Prepositions are used with what cases?
class Preposition(Lexeme):
    def __init__(self, lemma, pos, definitions, cases=[]):
        """[summary]

        Args:
            lemma ([type]): [description]
            pos ([type]): [description]
            definitions ([type]): [description]
            cases (list, optional): [description]. Defaults to [].
        """
        cases = list(map(lambda x: Case[x.upper()], cases))

        super(Preposition, self).__init__(lemma, pos, definitions)
        self.cases = cases
