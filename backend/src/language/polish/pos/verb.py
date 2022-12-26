from enforce_typing import enforce_types
from dataclasses import dataclass, field
from typing import Union, Optional

from language.part_of_speech import PartOfSpeech
from language.inflected_lexeme import InflectedLexeme
from language.model_errors import LexemeError
from language.polish.feat.abstraction import Abstraction
from language.polish.feat.aspect import Aspect


@enforce_types
@dataclass
class Verb(InflectedLexeme):
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
    """
    lemma: str
    pos: Union[PartOfSpeech, str]
    definitions: list[str]
    inflections: dict
    aspect: Union[Aspect, str]
    abstraction: Optional[Union[Abstraction, str]] = None
    is_frequentative: bool = False
    imperfective: list[str] = field(default_factory=list)
    perfective: list[str] = field(default_factory=list)
    indeterminate: list[str] = field(default_factory=list)
    frequentative: list[str] = field(default_factory=list)

    def __post_init__(self):
        """
        postprocess verb
        """
        # preprocess gender information
        if self.aspect and not isinstance(self.aspect, Aspect):
            self.aspect = Aspect[self.aspect.upper()]
        if self.abstraction and not isinstance(self.abstraction, Abstraction):
            self.abstraction = Abstraction[self.abstraction.upper()]

        if not self.validate_form(self.aspect, self.abstraction, self.is_frequentative):
            arguments = {'aspect': self.aspect, 'abstraction': self.abstraction,
                         'frequentative': self.is_frequentative}
            raise LexemeError(self.lemma, self.pos, arguments, 'invalid verb form logic')

        super().__post_init__()

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
