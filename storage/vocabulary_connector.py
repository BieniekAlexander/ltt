# imports
import sys, os
from bson.objectid import ObjectId
from model import lexeme

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.collection_connector import CollectionConnctor
from storage.datastore_utils import generate_query

# constants
DATABASE = "vocabulary"


class VocabularyConnector(CollectionConnctor):
  """
  A [CollectionConnector] used specifically for recording terms known by a given user
  """
  def __init__(self, uri, language, user_id):
    super(VocabularyConnector, self).__init__(uri, DATABASE, language)
    self.language = language
    self.user_id = user_id
  
  
  def push_vocabulary_entry(self, lexeme_id: str, rating: float, user_id: str = None) -> str:
    """
    Add a new vocabulary entry to the datastore, represented by a [lexeme_id], [rating], and [user_id]
    """
    if user_id is None: user_id = self.user_id
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
      if 'user_id' not in entry: entry['user_id'] = self.user_id
      assert all(key in entry for key in ['lexeme_id', 'user_id', 'rating']), "Each vocabulary entry must contain a lexeme_id, user_id, and rating"
      assert isinstance(entry['rating'], float)
      entry['lexeme_id'] = ObjectId(entry['lexeme_id'])
      entry['user_id'] = ObjectId(entry['user_id'])

    return super(VocabularyConnector, self).push_documents(entries)


  def get_vocabulary_entry_mapping(self, lexeme_id: str = None, user_id: str = None) -> dict:
    """
    Get a vocabulary entry and its _id, given the [lexeme_id] and [user_id]
    """
    if lexeme_id: lexeme_id = ObjectId(lexeme_id)
    if user_id is None: user_id = self.user_id
    user_id = ObjectId(user_id)
    query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
    return super(VocabularyConnector, self).get_document_mapping(query)

  
  def get_vocabulary_entry_mappings(self, lexeme_ids: list = None, user_ids: list = None) -> dict:
    """
    Get vocabulary entries and their _ids, given the [lexeme_ids] and [user_ids]
    """
    # TODO would it ever make sense to query for multiple user IDs?
    # TODO this is clunky - if you want the entries from all users, you have to provide an empty list, and not None, because None defaults to self.user_id
    if user_ids is None: user_ids = self.user_id
    
    if isinstance(lexeme_ids, list):
      lexeme_ids = list(map(ObjectId, lexeme_ids))
    elif lexeme_ids:
      lexeme_ids = ObjectId(lexeme_ids)

    if isinstance(user_ids, list):
      ser_ids = list(map(ObjectId, user_ids))
    elif user_ids:
      ser_ids = ObjectId(user_ids)

    query = generate_query(lexeme_id=lexeme_ids, user_id=user_ids)
    return super(VocabularyConnector, self).get_document_mappings(query)


  def delete_vocabulary_entry_mapping(self, lexeme_id: str = None, user_id: str = None) -> dict:
    """
    Delete vocabulary data entry and its _id, given the [lexeme_id], [form], and [pos]
    """
    if user_id is None: user_id = self.user_id
    if lexeme_id: lexeme_id = ObjectId(lexeme_id)
    query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
    return super(VocabularyConnector, self).delete_document_mapping(query)
  
  
  def delete_vocabulary_entry_mappings(self, lexeme_ids: list = None, user_ids: list = None) -> dict:
    """
    Delete vocabulary data entries and their _ids, given the [lexeme_ids] and [user_ids]
    """
    # TODO would it ever make sense to query for multiple user IDs?
    if user_ids is None: user_ids = self.user_id

    if isinstance(lexeme_ids, list):
      lexeme_ids = list(map(ObjectId, lexeme_ids))
    elif lexeme_ids:
      lexeme_ids = ObjectId(lexeme_ids)

    if isinstance(user_ids, list):
      ser_ids = list(map(ObjectId, user_ids))
    elif user_ids:
      ser_ids = ObjectId(user_ids)

    query = generate_query(lexeme_id=lexeme_ids, user_id=user_ids)
    return super(VocabularyConnector, self).delete_document_mappings(query)
 

#%% main
def main():
  pass  


if __name__ == "__main__":
  main()