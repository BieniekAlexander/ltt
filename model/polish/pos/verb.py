# https://en.wiktionary.org/wiki/Category:Polish_verbs
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.inflected_lexeme import InflectedLexeme
from model.model_errors import LexemeValidationError
from model.polish.feat.aspect import Aspect
from model.polish.feat.abstraction import Abstraction


# TODO verb aspect, abstraaction
class Verb(InflectedLexeme):
  """
  TODO
  """
  def __init__(self, lemma, pos, definitions, inflections, aspect, abstraction=None, is_frequentative=False,
               imperfective=[], perfective=[], indeterminate=[], frequentative=[]):
    """
    TODO
    """
    # preprocess gender information
    if aspect and not isinstance(aspect, Aspect):
      aspect = Aspect[aspect.upper()]
    if abstraction and not isinstance(abstraction, Abstraction):
      abstraction = Abstraction[abstraction.upper()]

    if not self.validate_form(aspect, abstraction, is_frequentative):
      arguments = {'aspect': aspect, 'abstraction': abstraction, 'frequentative': is_frequentative}
      raise LexemeValidationError(lemma, pos, arguments, 'invalid verb form logic')

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
    """
    TODO
    """
    # validate gender information of Noun
    form_info = (aspect, abstraction, is_frequentative)

    cases = [
      (Aspect.PERFECT, None, False),                        # perfect - e.g. pojść
      (Aspect.IMPERFECT, None, False),                      # imperfect - e.g. iść
      (Aspect.IMPERFECT, Abstraction.DETERMINATE, False),   # imperfect determinate - e.g. chodzić
      (Aspect.IMPERFECT, Abstraction.INDETERMINATE, True),  # imperfect indeterminate frequentative - e.g. jadać
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
    "S": None # TODO
  }