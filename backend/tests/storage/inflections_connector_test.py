#%% imports
import os, sys, json, pytest, pymongo
from bson.objectid import ObjectId

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from storage.mongodb_client import DatastoreClient
from storage.lexicon_connector import LexiconConnector
from storage.inflections_connector import InflectionsConnector
from model.lexeme import LexemeDecoder

# constants
MONGODB_URL = "mongodb://localhost:27017/"
ds_client = DatastoreClient(MONGODB_URL)
LANGUAGE = "test"


#%% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture()
def lexicon_connector():
  """
  Establish a connection to the mongodb database
  """
  test_lexicon_connector = LexiconConnector(ds_client, LANGUAGE)

  # run test
  yield test_lexicon_connector

  # cleanup
  test_lexicon_connector.collection.drop()
  test_lexicon_connector.collection.drop_indexes()


@pytest.fixture()
def inflections_connector():
  """
  Establish a connection to the mongodb database
  """
  
  test_inflections_connector = InflectionsConnector(ds_client, LANGUAGE)
  test_inflections_connector.collection.create_index([("form", pymongo.ASCENDING), ("pos", pymongo.ASCENDING), ("lexeme_id", pymongo.ASCENDING)], name="inflections index", unique=True)

  # run test
  yield test_inflections_connector

  # cleanup
  test_inflections_connector.collection.drop()
  test_inflections_connector.collection.drop_indexes()


#%% tests
# push and get
def test_push_and_get_inflection(inflections_connector):
  lexeme_id = ObjectId()
  form = "potato"
  pos = "NOUN"

  inflections_connector.push_inflection_entry(lexeme_id=lexeme_id, form=form, pos=pos)
  inflections_connector.get_inflection_entry(lexeme_id=lexeme_id, form=form, pos=pos)


def test_push_args_missing_fail(inflections_connector):
  lexeme_id = ObjectId()
  form = "potato"

  with pytest.raises(Exception):
    inflections_connector.push_inflection_entry(lexeme_id=lexeme_id, form=form)


def test_push_and_get_inflections(lexicon_connector, inflections_connector):
  json_str = open('tests/storage/data/noun_czerwony.json').read()
  lexeme = json.loads(json_str, cls=LexemeDecoder)
  inflections = list(set(lexeme.get_inflections()))
  lexeme_id = lexicon_connector.push_lexeme_entry(lexeme)
  entries = []

  for inflection in inflections:
    entry = {'form': inflection, 'pos': lexeme.pos.value, 'lexeme_id': lexeme_id}
    entries.append(entry)

  inflections_connector.push_inflection_entries(entries)
  results = inflections_connector.get_inflection_entries(poses=lexeme.pos.value, lexeme_ids=lexeme_id)


def test_push_and_delete_inflection_args(inflections_connector):
  lexeme_id = ObjectId()
  form = "potato"
  pos = "NOUN"

  inflections_connector.push_inflection_entry(lexeme_id=lexeme_id, form=form, pos=pos)
  inflections_connector.delete_inflection_entry(lexeme_id=lexeme_id, form=form, pos=pos)


def test_push_and_delete_inflections(lexicon_connector, inflections_connector):
  json_str = open('tests/storage/data/noun_czerwony.json').read()
  lexeme = json.loads(json_str, cls=LexemeDecoder)
  inflections = list(set(lexeme.get_inflections()))
  lexeme_id = lexicon_connector.push_lexeme_entry(lexeme)
  entries = []

  for inflection in inflections:
    entry = {'form': inflection, 'pos': lexeme.pos.value, 'lexeme_id': lexeme_id}
    entries.append(entry)

  inflections_connector.push_inflection_entries(entries)
  inflections_connector.delete_inflection_entries(poses=lexeme.pos.value, lexeme_ids=lexeme_id)



#% main
def main():
  pass


if __name__ == "__main__":
  main()