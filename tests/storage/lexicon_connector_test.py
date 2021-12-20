#%% imports
import os, sys, json, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from storage.lexicon_connector import LexiconConnector
from model.lexeme import Lexeme, LexemeDecoder

# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "test"


#%% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture(autouse=True)
def lexicon_connector():
  """
  Establish a connection to the mongodb database
  """
  test_lexicon_connector = LexiconConnector(MONGODB_URL, LANGUAGE)

  # run test
  yield test_lexicon_connector

  # cleanup
  test_lexicon_connector.collection.drop()
  test_lexicon_connector.collection.drop_indexes()


#%% tests
# push and get
def test_push_and_get_lexeme(lexicon_connector):
  lexeme = Lexeme('ope', 'CONJUNCTION', [])
  lexicon_connector.push_lexeme(lexeme)
  _, returned_lexeme = lexicon_connector.get_lexeme_mapping(lemma=lexeme.lemma, pos=lexeme.pos)

  assert lexeme == returned_lexeme
  

def test_push_and_get_lexeme_dictionary(lexicon_connector):
  lexeme = Lexeme('ope', 'CONJUNCTION', [])
  lexeme_dict = lexeme.to_json_dictionary()
  lexicon_connector.push_lexeme(lexeme_dict)
  _, returned_lexeme_dict = lexicon_connector.get_lexeme_dictionary_mapping(lemma=lexeme.lemma, pos=lexeme.pos)

  assert lexeme.lemma == returned_lexeme_dict['lemma']


def test_push_and_get_lexemes(lexicon_connector):
  lemmas = ['hi', 'julia']
  lexemes = [Lexeme(l, "CONJUNCTION", []) for l in lemmas]
  lexicon_connector.push_lexemes(lexemes)
  returned_lexeme_mappings = lexicon_connector.get_lexeme_mappings(lemmas=lemmas)

  for _id, lexeme in returned_lexeme_mappings.items():
    assert lexeme.lemma in lemmas


def test_push_and_get_lexeme_dictionaries(lexicon_connector):
  lemmas = ['hi', 'julia']
  lexemes = [Lexeme(l, "CONJUNCTION", []) for l in lemmas]
  lexicon_connector.push_lexemes(lexemes)
  returned_lexeme_mappings = lexicon_connector.get_lexeme_dictionary_mappings(lemmas=lemmas)

  for _id, lexeme_dictionary in returned_lexeme_mappings.items():
    assert lexeme_dictionary['lemma'] in lemmas


# push and pop
def test_push_and_pop_lexeme(lexicon_connector):
  lexeme = Lexeme('ope', 'CONJUNCTION', [])
  lexicon_connector.push_lexeme(lexeme)
  _, returned_lexeme = lexicon_connector.pop_lexeme_mapping(lemma=lexeme.lemma, pos=lexeme.pos)

  assert lexeme == returned_lexeme

  with pytest.raises(Exception): # TODO change exception type
    _, returned_lexeme = lexicon_connector.get_lexeme_mapping(lemma=lexeme.lemma, pos=lexeme.pos)
  

def test_push_and_pop_lexeme_dictionary(lexicon_connector):
  lexeme = Lexeme('ope', 'CONJUNCTION', [])
  lexeme_dict = lexeme.to_json_dictionary()
  lexicon_connector.push_lexeme(lexeme_dict)
  _, returned_lexeme_dict = lexicon_connector.pop_lexeme_dictionary_mapping(lemma=lexeme.lemma, pos=lexeme.pos)

  assert lexeme.lemma == returned_lexeme_dict['lemma']

  with pytest.raises(Exception): # TODO change exception type
    _, returned_lexeme = lexicon_connector.get_lexeme_dictionary_mapping(lemma=lexeme.lemma, pos=lexeme.pos)


def test_push_and_pop_lexemes(lexicon_connector):
  lemmas = ['hi', 'julia']
  lexemes = [Lexeme(l, "CONJUNCTION", []) for l in lemmas]
  lexicon_connector.push_lexemes(lexemes)
  returned_lexeme_mappings = lexicon_connector.pop_lexeme_mappings(lemmas=lemmas)

  for _id, lexeme in returned_lexeme_mappings.items():
    assert lexeme.lemma in lemmas

  with pytest.raises(Exception): # TODO change exception type
    _, returned_lexeme = lexicon_connector.get_lexeme_mapping(lemma=lemmas[0])  


def test_push_and_pop_lexeme_dictionaries(lexicon_connector):
  lemmas = ['hi', 'julia']
  lexemes = [Lexeme(l, "CONJUNCTION", []) for l in lemmas]
  lexicon_connector.push_lexemes(lexemes)
  returned_lexeme_mappings = lexicon_connector.pop_lexeme_dictionary_mappings(lemmas=lemmas)

  for _id, lexeme_dictionary in returned_lexeme_mappings.items():
    assert lexeme_dictionary['lemma'] in lemmas

  with pytest.raises(Exception): # TODO change exception type
    _, returned_lexeme = lexicon_connector.get_lexeme_dictionary_mapping(lemma=lemmas[0])


def test_multiple_lexemes_same_lemma_get_lexeme_fails(lexicon_connector):
  noun_str = open('tests/storage/data/noun_czerwony.json').read()
  noun = json.loads(noun_str, cls=LexemeDecoder)
  adj_str = open('tests/storage/data/adjective_czerwony.json').read()
  adj = json.loads(adj_str, cls=LexemeDecoder)
  lexemes = [noun, adj]
  lexicon_connector.push_lexemes(lexemes)

  with pytest.raises(Exception): # TODO change exception type
    _, returned_lexeme = lexicon_connector.get_lexeme_dictionary_mapping(lemma='czerwony')


#% main
def main():
  pass


if __name__ == "__main__":
  main()