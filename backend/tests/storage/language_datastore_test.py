#%% imports
import os, sys, json, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from storage.language_datastore import LanguageDatastore
from model.lexeme import Lexeme, LexemeDecoder
from storage.datastore_utils import lexeme_index
# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "polish"
DATABASE_NAME = LANGUAGE+"_test"


#%% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture(autouse=True)
def language_datastore():
  """
  Establish a connection to the mongodb database
  """
  test_language_datastore = LanguageDatastore(MONGODB_URL, LANGUAGE, database_name=DATABASE_NAME)
  test_language_datastore.lexicon_connector.collection.create_index(**lexeme_index)

  # run test
  yield test_language_datastore

  # cleanup
  test_language_datastore.lexicon_connector.collection.drop({})
  test_language_datastore.lexicon_connector.collection.drop_indexes()
  test_language_datastore.inflections_connector.collection.drop({})
  test_language_datastore.inflections_connector.collection.drop_indexes()
  

#%% tests
# push and get
def test_add_and_get_lexeme(language_datastore):
  json_str = open('tests/storage/data/noun_czerwony.json').read()
  lexeme = json.loads(json_str, cls=LexemeDecoder)
  language_datastore.add_lexeme_mapping(lexeme)
  returned_lexeme = language_datastore.form_to_lexeme_mapping(form=lexeme.inflections['S']['I'], pos="NOUN")

  assert returned_lexeme


def test_get_lexeme_none(language_datastore):
  noun_str = open('tests/storage/data/noun_czerwony.json').read()
  noun = json.loads(noun_str, cls=LexemeDecoder)
  adj_str = open('tests/storage/data/adjective_czerwony.json').read()
  adj = json.loads(adj_str, cls=LexemeDecoder)

  language_datastore.add_lexeme_mapping(noun)
  language_datastore.add_lexeme_mapping(adj)

  assert language_datastore.form_to_lexeme_mapping(form='niebieski', pos="ADJECTIVE") == None


def test_get_lexeme_wrong_pos_none(language_datastore):
  noun_str = open('tests/storage/data/noun_czerwony.json').read()
  noun = json.loads(noun_str, cls=LexemeDecoder)
  adj_str = open('tests/storage/data/adjective_czerwony.json').read()
  adj = json.loads(adj_str, cls=LexemeDecoder)

  language_datastore.add_lexeme_mapping(noun)
  language_datastore.add_lexeme_mapping(adj)

  assert language_datastore.form_to_lexeme_mapping(form='czerwony', pos="ADVERB") == None


def test_add_and_get_lexemes(language_datastore):
  noun_str = open('tests/storage/data/noun_czerwony.json').read()
  noun = json.loads(noun_str, cls=LexemeDecoder)
  adj_str = open('tests/storage/data/adjective_czerwony.json').read()
  adj = json.loads(adj_str, cls=LexemeDecoder)

  language_datastore.add_lexeme_mapping(noun)
  language_datastore.add_lexeme_mapping(adj)
  returned_lexemes = language_datastore.form_to_lexeme_mappings(form='czerwony')

  assert returned_lexemes


def test_get_lexemes_none(language_datastore):
  noun_str = open('tests/storage/data/noun_czerwony.json').read()
  noun = json.loads(noun_str, cls=LexemeDecoder)
  adj_str = open('tests/storage/data/adjective_czerwony.json').read()
  adj = json.loads(adj_str, cls=LexemeDecoder)

  language_datastore.add_lexeme_mapping(noun)
  language_datastore.add_lexeme_mapping(adj)

  assert language_datastore.form_to_lexeme_mappings(form='niebieski') == {}


def test_get_lexemes_wrong_pos_none(language_datastore):
  noun_str = open('tests/storage/data/noun_czerwony.json').read()
  noun = json.loads(noun_str, cls=LexemeDecoder)
  adj_str = open('tests/storage/data/adjective_czerwony.json').read()
  adj = json.loads(adj_str, cls=LexemeDecoder)

  language_datastore.add_lexeme_mapping(noun)
  language_datastore.add_lexeme_mapping(adj)

  assert language_datastore.form_to_lexeme_mappings(form='niebieski', poses=['VERB', 'ADVERB']) == {}


#%% main
def main():
  pass


if __name__ == "__main__":
  main()