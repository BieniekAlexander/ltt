from enforce_typing import enforce_types
from dataclasses import dataclass, field
from typing import Union, Optional

from language.inflected_lexeme import InflectedLexeme
from language.model_errors import LexemeError
from language.part_of_speech import PartOfSpeech
from language.polish.feat.animacy import Animacy
from language.polish.feat.gender import Gender
from language.polish.feat.personality import Personality
from language.polish.feat.virility import Virility

@enforce_types
@dataclass
class Noun(InflectedLexeme):
    """Polish Noun

    Args: TODO fill in types, I'm lazy right now
        lemma
        pos
        definitions
        inflections
        gender
        animacy
        virility
        personality
        diminutive
        augmentative
        masculine
        feminine
    """
    lemma: str
    pos: Union[PartOfSpeech, str]
    definitions: list[str]
    inflections: dict
    diminutive: Optional[list] = field(default_factory=list)
    augmentative: Optional[list] = field(default_factory=list)
    masculine: Optional[list] = field(default_factory=list)
    feminine: Optional[list] = field(default_factory=list)
    gender: Optional[Union[Gender, str]] = None # TODO would a noun ever not have a gender?
    animacy: Optional[Union[Animacy, str]] = None
    virility: Optional[Union[Virility, str]] = None
    personality: Optional[Union[Personality, str]] = None
    

    def __post_init__(self):
        """
        Test assertions of noun construction
        """
        # preprocess gender information
        if self.gender and not isinstance(self.gender, Gender):
            self.gender = Gender[self.gender.upper()]
        if self.personality and not isinstance(self.personality, Personality):
            self.personality = Personality[self.personality.upper()]
        if self.animacy and not isinstance(self.animacy, Animacy):
            self.animacy = Animacy[self.animacy.upper()]
        if self.virility and not isinstance(self.virility, Virility):
            self.virility = Virility[self.virility.upper()]

        if self.diminutive is None: self.diminutive = []
        if self.augmentative is None: self.augmentative = []
        if self.masculine is None: self.masculine = []
        if self.feminine is None: self.feminine = []

        if not self.validate_gender(self.gender, self.personality, self.animacy, self.virility):
            arguments = {'gender': self.gender, 'personality': self.personality,
                         'animacy': self.animacy, 'virility': self.virility}
            raise LexemeError(self.lemma, self.pos, arguments, 'invalid gender logic')

        super().__post_init__()

    def validate_gender(self, gender: Gender = None, personality: Personality = None, animacy: Animacy = None, virility: Virility = None) -> bool:
        """
        TODO
        """
        # validate gender information of Noun
        gender_info = (gender, personality, animacy, virility)

        cases = [
            # animate masculine singular - e.g. pies
            (Gender.MALE, Personality.PERSONAL, None, None),
            # animate masculine singular - e.g. pies
            (Gender.MALE, None, Animacy.ANIMATE, None),
            # inanimate masculine singular - .e.g. kubek
            (Gender.MALE, None, Animacy.INANIMATE, None),
            # female singular - e.g. kuchnia
            (Gender.FEMALE, None, None, None),
            # neuter singular - e.g. zwierzę
            (Gender.NEUTER, None, None, None),
            # virile plural - e.g. ?
            (None, None, None, Virility.VIRILE),
            # nonvirile plural - e.g. drzwi
            (None, None, None, Virility.NONVIRILE)
        ]

        if gender_info not in cases:
            return False

        return True

    # reference - https://en.wiktionary.org/wiki/ptak#Declension
    form_abbreviation_dict = {
        "singular": "S",
        "plural": "P",
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
            "N": None,
            "G": None,
            "D": None,
            "A": None,
            "I": None,
            "L": None,
            "V": None
        },
        "P": {
            "N": None,
            "G": None,
            "D": None,
            "A": None,
            "I": None,
            "L": None,
            "V": None
        }
    }
