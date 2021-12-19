# imports
import sys, os
from bson.objectid import ObjectId
from model import lexeme

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.collection_connector import CollectionConnctor
from storage.datastore_utils import generate_query

# constants
DATABASE = "vocabulary"


#%% implementation
def cast_object_id(id):
  if isinstance(id, str):
    return ObjectId(id)
  elif isinstance(id, ObjectId):
    return id
  else:
    raise TypeError("id should be a [str] or an [ObjectId}")


class VocabularyConnector(CollectionConnctor):
  """
  A [CollectionConnector] used specifically for recording terms known by a given user
  """
  def __init__(self, uri, language, user_id):
    super(VocabularyConnector, self).__init__(uri, DATABASE, language)
    self.language = language
    self.user_id = user_id
  
  
  def push_vocabulary_entry(self, entry: dict = None, lexeme_id: str = None, rating: float = None, user_id: int = None) -> str:
    """
    Add a new vocabulary entry to the datastore, represented by an [entry] dict or a [lexeme_id], [rating], and [user_id]
    """
    if user_id is None: user_id = self.user_id
    assert (entry and not lexeme_id and not rating and not user_id) or (not entry and lexeme_id and rating and user_id), "Only supply either an entry dict, or the keys of an entry"

    if lexeme_id and rating and user_id:
      lexeme_id = cast_object_id(lexeme_id)
      entry = {'lexeme_id': lexeme_id, 'rating': rating, 'user_id': user_id}
    elif entry:
      entry['lexeme_id'] = cast_object_id(entry['lexeme_id'])

    if any(key not in entry for key in ['lexeme_id', 'rating', 'user_id']):
      # TODO more specific exception
      raise Exception(f"missing lexeme_id, rating, or user_id for this entry - {entry}")

    return super(VocabularyConnector, self).push_document(entry)


  def push_vocabulary_entries(self, entries: list) -> list:
    """
    Add list of vocabulary entries to the datastore, each represented by a dictionary

    dictionaries must contain 'lexeme_id', 'user_id', and 'rating'
    """
    assert isinstance(entries, list)

    for entry in entries:
      assert isinstance(entry, dict)
      assert all(key in entry for key in ['lexeme_id', 'user_id', 'rating']), "Each vocabulary entry must contain a lexeme_id, user_id, and rating"
      entry['lexeme_id'] = cast_object_id(entry['lexeme_id'])

    return super(VocabularyConnector, self).push_documents(entries)


  def get_vocabulary_entry_mapping(self, lexeme_id: str = None, user_id: int = None) -> dict:
    """
    Get a vocabulary entry and its _id, given the [lexeme_id] and [user_id]
    """
    if user_id is None: user_id = self.user_id
    lexeme_id = cast_object_id(lexeme_id)
    query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
    return super(VocabularyConnector, self).get_document_mapping(query)

  
  def get_inflection_entry_mappings(self, lexeme_ids: list = None, user_ids: list = None) -> dict:
    """
    Get vocabulary entries and their _ids, given the [lexeme_ids] and [user_ids]
    """
    # TODO would it ever make sense to query for multiple user IDs?
    if user_ids is None: user_ids = self.user_id
    
    if isinstance(lexeme_ids, list):
      lexeme_ids = list(map(lambda x: cast_object_id(x), lexeme_ids))
    else:
      lexeme_ids = cast_object_id(lexeme_ids)

    query = generate_query(lexeme_id=lexeme_ids, user_id=user_ids)
    return super(VocabularyConnector, self).get_document_mappings(query)


  def pop_inflection_entry_mapping(self, lexeme_id: str = None, user_id: int = None) -> dict:
    """
    Pop inflection data entry and its _id, given the [lexeme_id], [form], and [pos]
    """
    if user_id is None: user_id = self.user_id
    lexeme_id = cast_object_id(lexeme_id)
    query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
    return super(VocabularyConnector, self).pop_document_mapping(query)
  
  
  def pop_inflection_entry_mappings(self, lexeme_ids: list = None, user_ids: list = None) -> dict:
    """
    Pop inflection data entries and their _ids, given the [lexeme_ids] and [user_ids]
    """
    # TODO would it ever make sense to query for multiple user IDs?
    if user_ids is None: user_ids = self.user_id

    if isinstance(lexeme_ids, list):
      lexeme_ids = list(map(lambda x: cast_object_id(x), lexeme_ids))
    else:
      lexeme_ids = cast_object_id(lexeme_ids)

    query = generate_query(lexeme_id=lexeme_ids, user_id=user_ids)
    return super(VocabularyConnector, self).pop_document_mappings(query)
 

#%% main
def main():
  pass  


if __name__ == "__main__":
  main()