#%% imports
import os, sys, json, pytest
from pymongo import MongoClient


from storage.language_datastore import LanguageDatastore
from storage.vocabulary_connector import VocabularyConnector
from language.lexeme import LexemeDecoder
from scraping.annotation_utils import annotate_text
from storage.datastore_schemata.polish_schemata import lexeme_index, user_vocabulary_index
from training.sm2.stats import Stats

# constants
LANGUAGE = "polish"
USER_ID = "0"*24


#%% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture()
def language_datastore():
  """
  Establish a connection to the mongodb database
  """
  ds_client = MongoClient()
  test_language_datastore = LanguageDatastore(ds_client, LANGUAGE)
  test_language_datastore.lexicon_connector.collection.create_index(**lexeme_index)

  # run test
  yield test_language_datastore

  # cleanup
  test_language_datastore.lexicon_connector.collection.drop({})
  test_language_datastore.lexicon_connector.collection.drop_indexes()
  test_language_datastore.inflections_connector.collection.drop({})
  test_language_datastore.inflections_connector.collection.drop_indexes()


@pytest.fixture()
def vocabulary_connector():
  """
  Establish a connection to the mongodb database
  """
  ds_client = MongoClient()
  test_vocabulary_connector = VocabularyConnector(ds_client, LANGUAGE)
  test_vocabulary_connector.collection.create_index(**user_vocabulary_index)

  # run test
  yield test_vocabulary_connector

  # cleanup
  test_vocabulary_connector.collection.drop({})
  test_vocabulary_connector.collection.drop_indexes()


#%% tests
def test_annotate_text_all_known_no_vocabulary(language_datastore):
  lexeme_0_str = open('tests/interface/data/noun_ciało.json').read()
  lexeme_0 = json.loads(lexeme_0_str, cls=LexemeDecoder)
  lexeme_1_str = open('tests/interface/data/verb_być.json').read()
  lexeme_1 = json.loads(lexeme_1_str, cls=LexemeDecoder)
  lexeme_2_str = open('tests/interface/data/adjective_prawdziwy.json').read()
  lexeme_2 = json.loads(lexeme_2_str, cls=LexemeDecoder)
  
  lexemes = [lexeme_0, lexeme_1, lexeme_2]
  language_datastore.add_lexemes(lexemes)

  text = "ciało jest prawdziwe."
  annotations = annotate_text(text, language_datastore)

  for lexeme, annotation in list(zip(lexemes, annotations)):
    annotation_lexeme = annotation['lexeme']
    assert lexeme.lemma == annotation_lexeme['lemma']


def test_annotate_text_some_known(language_datastore):
  lexeme_0_str = open('tests/interface/data/noun_ciało.json').read()
  lexeme_0 = json.loads(lexeme_0_str, cls=LexemeDecoder)
  lexeme_1_str = open('tests/interface/data/verb_być.json').read()
  lexeme_1 = json.loads(lexeme_1_str, cls=LexemeDecoder)

  lexemes = [lexeme_0, lexeme_1]
  language_datastore.add_lexemes(lexemes)

  text = "ciało jest prawdziwe."
  annotations = annotate_text(text, language_datastore)

  assert annotations[0]['lexeme']['lemma'] == lexeme_0.lemma
  assert 'lexeme' not in annotations[2]


def test_annotate_text_some_known_discover(language_datastore):
  lexeme_0_str = open('tests/interface/data/noun_ciało.json').read()
  lexeme_0 = json.loads(lexeme_0_str, cls=LexemeDecoder)
  lexeme_1_str = open('tests/interface/data/verb_być.json').read()
  lexeme_1 = json.loads(lexeme_1_str, cls=LexemeDecoder)
  lexeme_2_str = open('tests/interface/data/adjective_prawdziwy.json').read()
  lexeme_2 = json.loads(lexeme_2_str, cls=LexemeDecoder)

  lexemes = [lexeme_0, lexeme_1]
  language_datastore.add_lexemes(lexemes)

  text = "ciało jest prawdziwe."
  annotations = annotate_text(text, language_datastore, discovery_mode=True)

  assert annotations[0]['lexeme']['lemma'] == lexeme_0.lemma
  assert annotations[1]['lexeme']['lemma'] == lexeme_1.lemma
  assert annotations[2]['lexeme']['lemma'] == lexeme_2.lemma


def test_annotate_some_vocabulary(language_datastore, vocabulary_connector: VocabularyConnector):
  lexeme_0_str = open('tests/interface/data/noun_ciało.json').read()
  lexeme_0 = json.loads(lexeme_0_str, cls=LexemeDecoder)
  lexeme_1_str = open('tests/interface/data/verb_być.json').read()
  lexeme_1 = json.loads(lexeme_1_str, cls=LexemeDecoder)
  lexeme_2_str = open('tests/interface/data/adjective_prawdziwy.json').read()
  lexeme_2 = json.loads(lexeme_2_str, cls=LexemeDecoder)

  lexemes = [lexeme_0, lexeme_1]
  lexeme_ids = language_datastore.add_lexemes(lexemes)

  entry = {'lexeme_id': lexeme_ids[0], 'stats': Stats(), 'user_id': USER_ID}
  vocabulary_mapping = vocabulary_connector.push_vocabulary_entry(**entry)

  text = "ciało jest prawdziwe."
  annotations = annotate_text(text, language_datastore, user_id=USER_ID)

  assert annotations[0]['lexeme']['lemma'] == lexeme_0.lemma
  assert annotations[1]['lexeme']['lemma'] == lexeme_1.lemma
  assert 'lexeme' not in annotations[2]

  assert annotations[0]['vocabulary_id'] != None
  assert 'vocabulary_id' not in annotations[1]
  assert 'vocabulary_id' not in annotations[2]


#%% main
def main():
  pass


if __name__ == "__main__":
  main()