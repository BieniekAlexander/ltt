from dataclasses import dataclass, field
from enforce_typing import enforce_types
from typing import Union

from language.inflected_lexeme import InflectedLexeme
from language.model_errors import LexemeError
from language.part_of_speech import PartOfSpeech 
from language.polish.feat.degree import Degree


@enforce_types
@dataclass
class Adjective(InflectedLexeme):
    """Polish Adjective

    Args:
        lemma (str): lemma form
        pos
        definitions (list)
        inflections (dict)
        degree
        positive (list, optional): the positive forms of the adjective, if they exist and this isn't it
        comparative (list, optional): the comparative forms of the adjective, if they exist and this isn't it
        superlative (list, optional): the superlative forms of the adjective, if they exist and this isn't it
        adverb (list, optional): the adverb forms of the adjective, if they exist
        not_comparable (bool, optional): true if this adjective is not comparable
    """
    lemma: str
    pos: Union[PartOfSpeech, str]
    definitions: list[str]
    inflections: dict
    degree: Union[Degree, str]
    positive: list[str] = field(default_factory=list)
    comparative: list[str] = field(default_factory=list)
    superlative: list[str] = field(default_factory=list)
    adverb: list[str] = field(default_factory=list)
    not_comparable: bool = False

    def __post_init__(self):
        """
        check initialization
        """
        if self.degree and not isinstance(self.degree, Degree):
            self.degree = Degree[self.degree.upper()]

        if not self.validate_degrees(self.degree, self.positive, self.comparative, self.superlative, self.not_comparable):
            args = {'degree': self.degree, 'positive': self.positive, 'comparative': self.comparative,
                    'superlative': self.superlative, 'not_comparable': self.not_comparable}
            raise LexemeError(
                self.lemma, self.pos, args, f"The adjective had invalid arguments regarding degree - {args}")

        super().__post_init__()
        

    def validate_degrees(self, degree, positive, comparative, superlative, not_comparable):
        """
        Checks that the form of this adjective is valid and doesn't overlap with references to other degrees.
        """
        if not degree or not isinstance(degree, Degree):  # degree not supplied
            return False

        # if the form is not comparable, then...
        if not_comparable and (degree is not Degree.POSITIVE or comparative or superlative):
            return False

        if not not_comparable:
            if (degree is Degree.POSITIVE and (positive or not comparative or not superlative)) \
                    or (degree is Degree.COMPARATIVE and (not positive or comparative)) \
                    or (degree is Degree.SUPERLATIVE and (not positive or superlative)):
                return False

        # everything checks out
        return True

    # reference - https://en.wiktionary.org/wiki/czerwony#Declension_2
    form_abbreviation_dict = {
        "singular": "S",
        "plural": "P",
        "masculine personal/animate": "A",
        "masculine inanimate": "I",
        "neuter": "N",
        "feminine": "F",
        "virile": "V",
        "nonvirile": "N",
        "nominative": "N",
        "genitive": "G",
        "accusative": "A",
        "dative": "D",
        "instrumental": "I",
        "locative": "L",
        "vocative": "V"
    }

    schema = {
        "S": {
            "A": {
                "N": None,
                "G": None,
                "D": None,
                "A": None,
                "I": None,
                "L": None,
                "V": None
            },
            "I": {
                "N": None,
                "G": None,
                "D": None,
                "A": None,
                "I": None,
                "L": None,
                "V": None
            },
            "N": {
                "N": None,
                "G": None,
                "D": None,
                "A": None,
                "I": None,
                "L": None,
                "V": None
            },
            "F": {
                "N": None,
                "G": None,
                "D": None,
                "A": None,
                "I": None,
                "L": None,
                "V": None
            }
        },
        "P": {
            "V": {
                "N": None,
                "G": None,
                "D": None,
                "A": None,
                "I": None,
                "L": None,
                "V": None
            },
            "N": {
                "N": None,
                "G": None,
                "D": None,
                "A": None,
                "I": None,
                "L": None,
                "V": None
            }
        }
    }
