from enforce_typing import enforce_types
from dataclasses import dataclass, field
from typing import Union

from language.lexeme import Lexeme
from language.model_errors import LexemeError
from language.polish.feat.degree import Degree
from language.part_of_speech import PartOfSpeech

# TODO handle comparative and superlative?

@enforce_types
@dataclass
class Adverb(Lexeme):
    """
    Polish adverb

    Args:
        lemma ([type]): [description]
        pos ([type]): [description]
        definitions ([type]): [description]
        degree ([type]): [description]
        positive (list, optional): [description]. Defaults to [].
        comparative (list, optional): [description]. Defaults to [].
        superlative (list, optional): [description]. Defaults to [].
        adjective (list, optional): [description]. Defaults to [].
        not_comparable (bool, optional): [description]. Defaults to False.
    """
    lemma: str
    pos: Union[PartOfSpeech, str]
    definitions: list[str]
    degree: Union[Degree, str]
    positive: list[str] = field(default_factory=list)
    comparative: list[str] = field(default_factory=list)
    superlative: list[str] = field(default_factory=list)
    adjective: list[str] = field(default_factory=list)
    not_comparable: bool = False
    
    def __post_init__(self):
        """
        Test assertions on this lexeme after construction
        """
        if self.degree and not isinstance(self.degree, Degree):
            self.degree = Degree[self.degree.upper()]

        if not self.validate_degrees(self.degree, self.positive, self.comparative, self.superlative, self.not_comparable):
            args = {'degree': self.degree, 'positive': self.positive, 'comparative': self.comparative,
                    'superlative': self.superlative, 'not_comparable': self.not_comparable}
            raise LexemeError(
                self.lemma, self.pos, args, f"The adverb had invalid arguments regarding degree - {args}")

        super(Adverb, self).__post_init__()

    def validate_degrees(self, degree, positive, comparative, superlative, not_comparable):
        """
        Checks that the form of this adverb is valid and doesn't overlap with references to other degrees.
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
