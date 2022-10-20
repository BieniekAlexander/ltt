

from language.inflected_lexeme import InflectedLexeme
from language.model_errors import LexemeError
from language.polish.feat.animacy import Animacy
from language.polish.feat.gender import Gender
from language.polish.feat.personality import Personality
from language.polish.feat.virility import Virility


class Noun(InflectedLexeme):
    def __init__(self, lemma, pos, definitions, inflections, gender: Gender = None, animacy: Animacy = None, virility: Virility = None, personality: Personality = None,
                 diminutive=None, augmentative=None, masculine=None, feminine=None):
        """_summary_

        Args:
            lemma (_type_): _description_
            pos (_type_): _description_
            definitions (_type_): _description_
            inflections (_type_): _description_
            gender (Gender, optional): _description_. Defaults to None.
            animacy (Animacy, optional): _description_. Defaults to None.
            virility (Virility, optional): _description_. Defaults to None.
            personality (Personality, optional): _description_. Defaults to None.
            diminutive (_type_, optional): _description_. Defaults to None.
            augmentative (_type_, optional): _description_. Defaults to None.
            masculine (_type_, optional): _description_. Defaults to None.
            feminine (_type_, optional): _description_. Defaults to None.

        Raises:
            LexemeError: _description_
        """
        # preprocess gender information
        if gender and not isinstance(gender, Gender):
            gender = Gender[gender.upper()]
        if personality and not isinstance(personality, Personality):
            personality = Personality[personality.upper()]
        if animacy and not isinstance(animacy, Animacy):
            animacy = Animacy[animacy.upper()]
        if virility and not isinstance(virility, Virility):
            virility = Virility[virility.upper()]

        if not self.validate_gender(gender, personality, animacy, virility):
            arguments = {'gender': gender, 'personality': personality,
                         'animacy': animacy, 'virility': virility}
            raise LexemeError(lemma, pos, arguments, 'invalid gender logic')

        # load in fields
        super(Noun, self).__init__(lemma, pos, definitions, inflections)
        self.gender = gender
        self.personality = personality
        self.animacy = animacy
        self.virility = virility
        self.diminutive = diminutive
        self.augmentative = augmentative
        self.masculine = masculine
        self.feminine = feminine

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
