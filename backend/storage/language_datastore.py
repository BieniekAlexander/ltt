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
  def __init__(self, uri: str, language: str, database_name=None):
    """
    Constructor
    """
    self.language = language.lower()

    if not database_name:
      database_name = language

    self.lexicon_connector = LexiconConnector(uri, language, database_name)
    self.inflections_connector = InflectionsConnector(uri, language, database_name)
    self.language = language
    self.database_name = database_name

  
  def add_lexeme_mapping(self, lexeme: Lexeme):
    """
    Add a lexeme to the datastore, add related data (i.e. inflection mappings), and get the lexeme_id
    """
    assert isinstance(lexeme, Lexeme)
    lexeme_id = self.lexicon_connector.push_lexeme(lexeme)
    
    if isinstance(lexeme, InflectedLexeme):
      inflections = lexeme.get_inflections()
      entries = [{'lexeme_id': lexeme_id, 'pos': lexeme.pos, 'form': form} for form in inflections]
      self.inflections_connector.push_inflection_entries(entries)
    else:
      self.inflections_connector.push_inflection_entry(lexeme_id, lexeme.lemma, lexeme.pos)

    return lexeme_id


  def add_lexeme_mappings(self, lexemes: list):
    """
    Add a lexeme to the datastore, add related data (i.e. inflection mappings), and get the lexeme_id
    """
    assert isinstance(lexemes, list) and all(isinstance(lexeme, Lexeme) for lexeme in lexemes)
    lexeme_ids = self.lexicon_connector.push_lexemes(lexemes)
    
    for lexeme_id, lexeme in zip(lexeme_ids, lexemes):
      if isinstance(lexeme, InflectedLexeme):
        inflections = lexeme.get_inflections()
        entries = [{'lexeme_id': lexeme_id, 'pos': lexeme.pos, 'form': form} for form in inflections]
        self.inflections_connector.push_inflection_entries(entries)
      else:
        self.inflections_connector.push_inflection_entry(lexeme_id, lexeme.lemma, lexeme.pos)

    return lexeme_ids

  
  def delete_lexeme_mapping(self, _id):
    """
    remove a lexeme from the language datastore by [_id]
    
    TODO is this even necessary?
    """
    raise NotImplementedError("Not implementing language lexeme deletion - do I need this?")

    
  def form_to_lexeme_dictionary_mapping(self, form: str, pos: str):
    """
    Get a lexeme, given the form form and pos

    This function will return one entry if it exists, [None] if none are found, or raise an exception if multiple are found
    """
    assert isinstance(form, str)
    assert isinstance(pos, str) and pos in [pos.value for pos in PartOfSpeech]

    
    _id, inflection_entry = self.inflections_connector.get_inflection_entry_mapping(form=form, pos=pos)
    
    if inflection_entry:
      lexeme_id = ObjectId(inflection_entry['lexeme_id'])
      lexeme_id, lexeme = self.lexicon_connector.get_lexeme_dictionary_mapping(_id=lexeme_id)
      return (lexeme_id, lexeme)
    else:
      return None


  def form_to_lexeme_dictionary_mappings(self, form: str, poses: list = None) -> dict:
    """
    Get the lexemes of [form] in the specified [poses]

    This function will return one entry if it exists, [None] if none are found, or raise an exception if multiple are found
    """
    if poses == None: poses = []
    assert isinstance(form, str)
    assert all(isinstance(pos, str) and pos in [pos.value for pos in PartOfSpeech] for pos in poses)

    lexeme_ids = [ObjectId(d['lexeme_id']) for d in self.inflections_connector.get_inflection_entry_mappings(forms=[form], poses=poses).values()]
    
    if lexeme_ids:
      lexeme_dicts_dict = self.lexicon_connector.get_lexeme_dictionary_mappings(_ids=lexeme_ids)
      return lexeme_dicts_dict
    else: # we found no entries for the [form] and [poses] provided
      return {}