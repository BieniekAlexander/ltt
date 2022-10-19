# https://en.wiktionary.org/wiki/Category:Polish_verbs


from language.inflected_lexeme import InflectedLexeme
from language.model_errors import LexemeError
from language.polish.feat.abstraction import Abstraction
from language.polish.feat.aspect import Aspect


class Verb(InflectedLexeme):
    def __init__(self, lemma, pos, definitions, inflections, aspect, abstraction=None, is_frequentative=False,
                 imperfective=[], perfective=[], indeterminate=[], frequentative=[]):
        """[summary]

        Args:
            lemma ([type]): [description]
            pos ([type]): [description]
            definitions ([type]): [description]
            inflections ([type]): [description]
            aspect ([type]): [description]
            abstraction ([type], optional): [description]. Defaults to None.
            is_frequentative (bool, optional): [description]. Defaults to False.
            imperfective (list, optional): [description]. Defaults to [].
            perfective (list, optional): [description]. Defaults to [].
            indeterminate (list, optional): [description]. Defaults to [].
            frequentative (list, optional): [description]. Defaults to [].

        Raises:
            LexemeError: [description]
        """
        # preprocess gender information
        if aspect and not isinstance(aspect, Aspect):
            aspect = Aspect[aspect.upper()]
        if abstraction and not isinstance(abstraction, Abstraction):
            abstraction = Abstraction[abstraction.upper()]

        if not self.validate_form(aspect, abstraction, is_frequentative):
            arguments = {'aspect': aspect, 'abstraction': abstraction,
                         'frequentative': is_frequentative}
            raise LexemeError(lemma, pos, arguments, 'invalid verb form logic')

        # load in fields
        super(Verb, self).__init__(lemma, pos, definitions, inflections)
        self.aspect = aspect
        self.abstraction = abstraction
        self.is_frequentative = is_frequentative
        self.imperfective = imperfective
        self.perfective = perfective
        self.indeterminate = indeterminate
        self.frequentative = frequentative

    def validate_form(self, aspect, abstraction, is_frequentative) -> bool:
        """[summary]

        Args:
            aspect ([type]): [description]
            abstraction ([type]): [description]
            is_frequentative (bool): [description]

        Returns:
            bool: [description]
        """
        # validate gender information of Noun
        form_info = (aspect, abstraction, is_frequentative)

        cases = [
            # perfect - e.g. pojść
            (Aspect.PERFECT, None, False),
            # imperfect - e.g. iść
            (Aspect.IMPERFECT, None, False),
            # imperfect determinate - e.g. chodzić
            (Aspect.IMPERFECT, Abstraction.DETERMINATE, False),
            # imperfect indeterminate frequentative - e.g. jadać
            (Aspect.IMPERFECT, Abstraction.INDETERMINATE, True),
        ]

        if form_info not in cases:
            return False

        return True

    # reference - https://en.wiktionary.org/wiki/biec#Conjugation
    form_abbreviation_dict = {
        "singular": "S",
        "plural": "P",
        "masculine": "M",
        "feminine": "F",
        "neuter": "N",
        "virile": "V",
        "nonvirile": "N",
        "infinitive": "Inf",
        "present tense": "Pres",
        "past tense": "Past",
        "future tense": "F",
        "conditional": "C",
        "imperative": "Imper",
        "active adjectival participle": "ActAP",
        "anterior adverbial participle": "AntAP",
        "passive adjectival participle": "PAP",
        "contemporary adverbial participle": "CAP",
        "verbal noun": "VN",
        "1st": "1",
        "2nd": "2",
        "3rd": "3",
        "impersonal": "Impers"
    }

    schema = {
        "S": None  # TODO
    }
