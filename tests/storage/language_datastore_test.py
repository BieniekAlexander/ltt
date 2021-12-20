#%% imports
import os, sys, json, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from storage.language_datastore import LanguageDatastore
from model.lexeme import Lexeme, LexemeDecoder
from storage.datastore_utils import lexeme_index

# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "test"


#%% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture(autouse=True)
def language_datastore():
  """
  Establish a connection to the mongodb database
  """
  test_language_datastore = LanguageDatastore(MONGODB_URL, LANGUAGE)
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
  language_datastore.add_lexeme(lexeme)
  returned_lexeme = language_datastore.get_lexeme(form=lexeme.inflections['S']['I'], pos="NOUN")


def test_add_and_get_lexemes(language_datastore):
  noun_str = open('tests/storage/data/noun_czerwony.json').read()
  noun = json.loads(noun_str, cls=LexemeDecoder)
  adj_str = open('tests/storage/data/adjective_czerwony.json').read()
  adj = json.loads(adj_str, cls=LexemeDecoder)

  language_datastore.add_lexeme(noun)
  language_datastore.add_lexeme(adj)
  returned_lexemes = language_datastore.get_lexemes(form='czerwony')


#%% main
def main():
  pass


if __name__ == "__main__":
  main()