#%% imports
import os, sys, json, pytest, pymongo
from bson.objectid import ObjectId

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from storage.datastore_client import DatastoreClient
from storage.lexicon_connector import LexiconConnector
from storage.vocabulary_connector import VocabularyConnector


# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "polish"


#%% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture()
def vocabulary_connector():
  """
  Establish a connection to the mongodb database
  """
  
  ds_client = DatastoreClient(MONGODB_URL)
  test_vocabulary_connector = VocabularyConnector(ds_client, LANGUAGE)
  test_vocabulary_connector.collection.create_index([("user_id", pymongo.ASCENDING), ("lexeme_id", pymongo.ASCENDING)], name="user vocabulary index", unique=True)

  # run test
  yield test_vocabulary_connector

  # cleanup
  test_vocabulary_connector.collection.drop()
  test_vocabulary_connector.collection.drop_indexes()


#%% tests
# push and get
def test_push_and_get_vocabulary_entry(vocabulary_connector):
  user_id_1 = ObjectId()
  user_id_2 = ObjectId()
  lexeme_id = ObjectId()
  rating_1=1.0
  rating_2=0.8
  entry_2 = {'lexeme_id': lexeme_id, 'user_id': user_id_2, 'rating': rating_2}

  vocabulary_connector.push_vocabulary_entry(lexeme_id=lexeme_id, rating=rating_1, user_id=user_id_1)
  vocabulary_connector.push_vocabulary_entry(**entry_2)
  
  vocabulary_connector.get_vocabulary_entry(lexeme_id=lexeme_id, user_id=user_id_1)
  vocabulary_connector.get_vocabulary_entry(lexeme_id=lexeme_id, user_id=user_id_2)


def test_push_and_get_vocabulary_entries(vocabulary_connector):
  user_id_1 = ObjectId()
  user_id_2 = ObjectId()
  lexeme_id = ObjectId()
  rating_1=1.0
  rating_2=0.8
  entries = [{'lexeme_id': lexeme_id, 'rating': rating_1, 'user_id': user_id_1},
    {'lexeme_id': lexeme_id, 'user_id': user_id_2, 'rating': rating_2}
  ]

  vocabulary_connector.push_vocabulary_entries(entries)
  vocabulary_connector.get_vocabulary_entries(lexeme_ids=lexeme_id, user_ids=[user_id_1, user_id_2])


def test_push_and_delete_vocabulary_entry(vocabulary_connector):
  user_id = ObjectId()
  lexeme_id = ObjectId()
  rating=1.0
  
  vocabulary_connector.push_vocabulary_entry(lexeme_id=lexeme_id, rating=rating, user_id=user_id)
  vocabulary_connector.delete_vocabulary_entry(lexeme_id=lexeme_id, user_id= user_id)


def test_push_and_delete_vocabulary_entries(vocabulary_connector):
  user_id_1 = ObjectId()
  user_id_2 = ObjectId()
  lexeme_id = ObjectId()
  rating_1=1.0
  rating_2=0.8
  entries = [{'lexeme_id': lexeme_id, 'rating': rating_1, 'user_id': user_id_1},
    {'lexeme_id': lexeme_id, 'user_id': user_id_2, 'rating': rating_2}
  ]

  vocabulary_connector.push_vocabulary_entries(entries)
  vocabulary_connector.delete_vocabulary_entries(lexeme_ids=lexeme_id, user_ids=[user_id_1, user_id_2])


def test_push_vocabulary_duplicate_entries_fail(vocabulary_connector):
  user_id_1 = ObjectId()
  lexeme_id = ObjectId()
  rating=1.0

  vocabulary_connector.push_vocabulary_entry(lexeme_id=lexeme_id, rating=rating, user_id=user_id_1)
  
  with pytest.raises(Exception):
    vocabulary_connector.push_vocabulary_entry(lexeme_id=lexeme_id, rating=rating)


#% main
def main():
  pass


if __name__ == "__main__":
  main()