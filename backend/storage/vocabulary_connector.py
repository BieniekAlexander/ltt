# imports
import sys, os
from bson.objectid import ObjectId
from pymongo import collection
from model import lexeme

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.collection_connector import CollectionConnector
from storage.datastore_utils import generate_query

# constants
COLLECTION = "vocabulary"


class VocabularyConnector(CollectionConnector):
  """
  A [CollectionConnector] used specifically for recording terms known by a given user
  """
  def __init__(self, uri, language, database_name=None):
    """
    Constructor

    Separate database_name argument used for testing - otherwise, the collection name defaults to the language name
    """
    language = language.lower()

    if not database_name:
      database_name = language

    super(VocabularyConnector, self).__init__(uri, database_name, COLLECTION)
    self.database_name = database_name
    self.language = language
  
  
  def push_vocabulary_entry(self, lexeme_id: str, rating: float, user_id: str) -> str:
    """
    Add a new vocabulary entry to the datastore, represented by a [lexeme_id], [rating], and [user_id]
    """
    assert user_id
    assert isinstance(rating, float)

    entry = {'lexeme_id': ObjectId(lexeme_id), 'rating': rating, 'user_id': ObjectId(user_id)}

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
      assert isinstance(entry['rating'], float)
      entry['lexeme_id'] = ObjectId(entry['lexeme_id'])
      entry['user_id'] = ObjectId(entry['user_id'])

    return super(VocabularyConnector, self).push_documents(entries)


  def get_vocabulary_entry(self, lexeme_id: str, user_id: str) -> dict:
    """
    Get a vocabulary entry and its _id, given the [lexeme_id] and [user_id]
    """
    assert lexeme_id and user_id

    if lexeme_id: lexeme_id = ObjectId(lexeme_id)
    user_id = ObjectId(user_id)
    query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
    return super(VocabularyConnector, self).get_document(query)

  
  def get_vocabulary_entries(self, lexeme_ids: list, user_ids: list) -> dict:
    """
    Get vocabulary entries and their _ids, given the [lexeme_ids] and [user_ids]
    """
    assert user_ids and lexeme_ids
    
    if isinstance(lexeme_ids, list):
      lexeme_ids = list(map(ObjectId, lexeme_ids))
    elif lexeme_ids:
      lexeme_ids = ObjectId(lexeme_ids)

    if isinstance(user_ids, list):
      user_ids = list(map(ObjectId, user_ids))
    elif user_ids:
      user_ids = ObjectId(user_ids)

    query = generate_query(lexeme_id=lexeme_ids, user_id=user_ids)
    return super(VocabularyConnector, self).get_documents(query)


  def delete_vocabulary_entry(self, lexeme_id: str, user_id: str) -> dict:
    """
    Delete vocabulary data entry and its _id, given the [lexeme_id], [form], and [pos]
    """
    if lexeme_id: lexeme_id = ObjectId(lexeme_id)
    query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
    return super(VocabularyConnector, self).delete_document(query)
  
  
  def delete_vocabulary_entries(self, lexeme_ids: list, user_ids: list) -> dict:
    """
    Delete vocabulary data entries and their _ids, given the [lexeme_ids] and [user_ids]
    """
    # TODO would it ever make sense to query for multiple user IDs?
    if isinstance(lexeme_ids, list):
      lexeme_ids = list(map(ObjectId, lexeme_ids))
    elif lexeme_ids:
      lexeme_ids = ObjectId(lexeme_ids)

    if isinstance(user_ids, list):
      ser_ids = list(map(ObjectId, user_ids))
    elif user_ids:
      ser_ids = ObjectId(user_ids)

    query = generate_query(lexeme_id=lexeme_ids, user_id=user_ids)
    return super(VocabularyConnector, self).delete_documents(query)
 

#%% main
def main():
  pass  


if __name__ == "__main__":
  main()