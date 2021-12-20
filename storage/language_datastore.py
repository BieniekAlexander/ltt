#%% imports
import sys, os
from model import lexeme
from bson.objectid import ObjectId

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.lexicon_connector import LexiconConnector
from storage.inflections_connector import InflectionsConnector
from model.inflected_lexeme import InflectedLexeme
from model.lexeme import Lexeme
from model.part_of_speech import PartOfSpeech


#%% Implementation
class LanguageDatastore(object):
  """
  A datastore interface that abstracts storage of language data
  """
  def __init__(self, uri: str, language: str):
    """
    Constructor
    """
    self.lexicon_connector = LexiconConnector(uri, language)
    self.inflections_connector = InflectionsConnector(uri, language)

  
  def add_lexeme(self, lexeme: Lexeme):
    """
    Add a lexeme to the datastore, and add related data (i.e. inflection mappings)
    """
    assert isinstance(lexeme, Lexeme)
    lexeme_id = self.lexicon_connector.push_lexeme(lexeme)
    
    if isinstance(lexeme, InflectedLexeme):
      inflections = lexeme.get_inflections()
      entries = [{'lexeme_id': lexeme_id, 'pos': lexeme.pos, 'form': form} for form in inflections]
      self.inflections_connector.push_inflection_entries(entries)
    else:
      self.inflections_connector.push_inflection_entry(lexeme_id, lexeme.lemma, lexeme.pos)

    
  def get_lexeme(self, form: str, pos: str):
    """
    Get a lexeme, given the form form and pos

    This function will return one entry if it exists, [None] if none are found, or raise an exception if multiple are found
    """
    assert isinstance(form, str)
    assert isinstance(pos, str) and pos in [pos.value for pos in PartOfSpeech]

    _, inflection_entry = self.inflections_connector.get_inflection_entry_mapping(form=form, pos=pos)
    lexeme_id = ObjectId(inflection_entry['lexeme_id'])
    _, lexeme = self.lexicon_connector.get_lexeme_mapping(_id=lexeme_id)
    return lexeme


  def get_lexemes(self, form: str, poses: str = None):
    """
    Get the lexemes which 

    This function will return one entry if it exists, [None] if none are found, or raise an exception if multiple are found
    """
    assert isinstance(form, str)

    if isinstance(poses, list):
      assert all(isinstance(pos, str) and pos in [pos.value for pos in PartOfSpeech] for pos in poses)
    elif poses:
      assert isinstance(poses, str) and poses in [poses.value for pos in PartOfSpeech]

    lexeme_ids = list(self.inflections_connector.get_inflection_entry_mappings(forms=form, poses=poses).keys())
    lexeme_ids = list(map(ObjectId, lexeme_ids))
    print(lexeme_ids)
    lexeme_mappings = self.lexicon_connector.get_lexeme_mappings(_ids=lexeme_ids)
    return lexeme_mappings.values()