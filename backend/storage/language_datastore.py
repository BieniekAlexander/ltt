#%% imports
import sys, os
from model import lexeme
from bson.objectid import ObjectId

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.datastore_client import DatastoreClient
from storage.lexicon_connector import LexiconConnector
from storage.inflections_connector import InflectionsConnector
from storage.vocabulary_connector import VocabularyConnector
from model.inflected_lexeme import InflectedLexeme
from model.lexeme import Lexeme
from model.part_of_speech import PartOfSpeech


#%% Implementation
# TODO revisit this interface - should it be instantiated with respect to a user? what pattern should be used here?
class LanguageDatastore(object):
  """
  A datastore interface that abstracts storage of language data
  """
  def __init__(self, client: DatastoreClient, language: str, database_name=None):
    """
    Constructor
    """
    self.language = language.lower()

    if not database_name:
      database_name = language

    self.lexicon_connector = LexiconConnector(client, language, database_name)
    self.inflections_connector = InflectionsConnector(client, language, database_name)
    self.vocabulary_connector = VocabularyConnector(client, language, database_name)
    self.language = language
    self.database_name = database_name

  
  def add_lexeme(self, lexeme: Lexeme):
    """
    Add a lexeme to the datastore, add related data (i.e. inflection mappings), and get the lexeme_id
    """
    assert isinstance(lexeme, Lexeme)
    lexeme_id = self.lexicon_connector.push_lexeme_entry(lexeme)
    
    if isinstance(lexeme, InflectedLexeme):
      inflections = lexeme.get_inflections()
      entries = [{'lexeme_id': lexeme_id, 'pos': lexeme.pos, 'form': form} for form in inflections]
      self.inflections_connector.push_inflection_entries(entries)
    else:
      self.inflections_connector.push_inflection_entry(lexeme_id, lexeme.lemma, lexeme.pos)

    return lexeme_id


  def add_lexemes(self, lexemes: list):
    """
    Add a lexeme to the datastore, add related data (i.e. inflection mappings), and get the lexeme_id
    """
    assert isinstance(lexemes, list) and all(isinstance(lexeme, Lexeme) for lexeme in lexemes)
    lexeme_ids = self.lexicon_connector.push_lexeme_entries(lexemes)
    
    for lexeme_id, lexeme in zip(lexeme_ids, lexemes):
      if isinstance(lexeme, InflectedLexeme):
        inflections = lexeme.get_inflections()
        entries = [{'lexeme_id': lexeme_id, 'pos': lexeme.pos, 'form': form} for form in inflections]
        self.inflections_connector.push_inflection_entries(entries)
      else:
        self.inflections_connector.push_inflection_entry(lexeme_id, lexeme.lemma, lexeme.pos)

    return lexeme_ids

  
  def delete_lexeme(self, _id):
    """
    remove a lexeme from the language datastore by [_id]
    
    TODO is this even necessary?
    """
    raise NotImplementedError("Not implementing language lexeme deletion - do I need this?")

    
  def get_lexeme_from_form(self, form: str, pos: str):
    """
    Get a lexeme, given the form form and pos

    This function will return one entry if it exists, [None] if none are found, or raise an exception if multiple are found
    """
    assert isinstance(form, str)
    assert isinstance(pos, str) and pos in [pos.value for pos in PartOfSpeech]

    
    entry = self.inflections_connector.get_inflection_entry(form=form, pos=pos)
    
    if entry:
      lexeme_id = ObjectId(entry['lexeme_id'])
      entry = self.lexicon_connector.get_lexeme_entry(_id=lexeme_id)
      return entry
    else:
      return None


  def get_lexemes_from_form(self, form: str, poses: list = None) -> dict:
    """
    Get the lexemes of [form] in the specified [poses]

    This function will return one entry if it exists, [None] if none are found, or raise an exception if multiple are found
    """
    if poses == None: poses = []
    assert isinstance(form, str)
    assert all(isinstance(pos, str) and pos in [pos.value for pos in PartOfSpeech] for pos in poses)

    lexeme_ids = [ObjectId(d['lexeme_id']) for d in self.inflections_connector.get_inflection_entries(forms=[form], poses=poses)]
    
    if lexeme_ids:
      lexeme_dicts_dict = self.lexicon_connector.get_lexeme_entries(_ids=lexeme_ids)
      return lexeme_dicts_dict
    else: # we found no entries for the [form] and [poses] provided
      return {}

    
  def get_vocabulary_entry(self, lexeme_id: str, user_id: str) -> dict:
    return self.vocabulary_connector.get_vocabulary_entry(lexeme_id, user_id)


  def get_vocabulary_entries(self, lexeme_ids: list, user_id: str) -> dict:
    assert isinstance(user_id, str) 
    return self.vocabulary_connector.get_vocabulary_entries(lexeme_ids, [user_id])

  
  def add_vocabulary_entry(self, lexeme_id, rating, user_id) -> str:
    """
    Add a [lexeme_id], [rating] entry to the vocabulary for [user_id]

    Args:
      lexeme_id: the identifier of the lexeme to be added to the vocabulary
      rating: the initial SRS rating of the vocabulary term for the user
      user_id: a [str] identifying the user that should receive the new vocabulary entry
    """
    self.vocabulary_connector.push_vocabulary_entry(lexeme_id, rating, user_id)


  def add_vocabulary_entries(self, entries: list, user_id: str) -> list:
    """
    Add a list of vocabulary [entries] to the vocabulary for [user_id]

    Args:
      entries: a [list] of [dict]s containing a lexeme_id and rating
      user_id: a [str] identifying the user that should receive the new vocabulary entries
    """
    assert all('lexeme_id' in entry and 'rating' in entry and 'user_id' not in entry for entry in entries)

    return self.vocabulary_connector.push_vocabulary_entries([{'user_id': user_id, 'lexeme_id': entry['lexeme_id'], 'rating': entry['rating']} for entry in entries])