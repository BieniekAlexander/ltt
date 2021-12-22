import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.model_errors import LexemeValidationError
from model.inflected_lexeme import InflectedLexeme
from model.polish.feat.gender import Gender
from model.polish.feat.animacy import Animacy
from model.polish.feat.virility import Virility



class Noun(InflectedLexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions, inflections, gender=None, animacy=None, virility=None, 
               diminutive=None, augmentative=None, masculine=None, feminine=None):
    """
    TODO
    """
    # preprocess gender information
    if gender and not isinstance(gender, Gender):
      gender = Gender[gender.upper()]
    if animacy and not isinstance(animacy, Animacy):
      animacy = Animacy[animacy.upper()]
    if virility and not isinstance(virility, Virility):
      virility = Virility[virility.upper()]

    if not self.validate_gender(gender, animacy, virility):
      arguments = {'gender': gender, 'animacy': animacy, 'virility': virility}
      raise LexemeValidationError(lemma, pos, arguments, 'invalid gender logic')

    # load in fields
    super(Noun, self).__init__(lemma, pos, definitions, inflections)
    self.gender = gender
    self.animacy = animacy
    self.virility = virility
    self.diminutive = diminutive
    self.augmentative = augmentative
    self.masculine = masculine
    self.feminine = feminine

  
  def validate_gender(self, gender=None, animacy=None, virility=None) -> bool:
    """
    TODO
    """
    # validate gender information of Noun
    gender_info = (gender, animacy, virility)

    cases = [
      (Gender.MALE, Animacy.ANIMATE, None),   # animate masculine singular - e.g. pies
      (Gender.MALE, Animacy.INANIMATE, None), # inanimate masculine singular - .e.g. kubek
      (Gender.FEMALE, None, None),            # female singular - e.g. kuchnia
      (Gender.NEUTER, None, None),            # neuter singular - e.g. zwierzę
      (None, None, Virility.VIRILE),          # virile plural - e.g. ?
      (None, None, Virility.NONVIRILE)        # nonvirile plural - e.g. drzwi
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