# %% imports
import json
import pytest

from bson.objectid import ObjectId
from language.lexeme_decoder import LexemeDecoder
from mongomock import MongoClient
from scraping.annotation_utils import annotate_text
from storage.datastore_schemata.polish_schemata import (lexeme_index,
                                                        vocabulary_index)
from storage.language_datastores.polish_datastore import PolishDatastore
from training.sm2_anki.stats import Stats

# constants
LANGUAGE = "polish"
USER_ID = ObjectId("0"*24)
ds_client = MongoClient()


# %% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture()
def language_datastore():
    """
    Establish a connection to the mongodb database
    """
    test_language_datastore = PolishDatastore(ds_client)

    # run test
    yield test_language_datastore

    # cleanup
    test_language_datastore.lexicon_connector.collection.drop({})


# %% tests
def test_annotate_text_all_known_no_vocabulary(language_datastore: PolishDatastore):
    lexeme_0_str = open('tests/interface/data/noun_ciało.json').read()
    lexeme_0 = json.loads(lexeme_0_str, cls=LexemeDecoder)
    lexeme_1_str = open('tests/interface/data/verb_być.json').read()
    lexeme_1 = json.loads(lexeme_1_str, cls=LexemeDecoder)
    lexeme_2_str = open('tests/interface/data/adjective_prawdziwy.json').read()
    lexeme_2 = json.loads(lexeme_2_str, cls=LexemeDecoder)

    lexemes = [lexeme_0, lexeme_1, lexeme_2]
    language_datastore.add_lexemes(lexemes)

    text = "ciało jest prawdziwe."
    annotations = annotate_text(text, language_datastore, language="polish")

    for lexeme, annotation in list(zip(lexemes, annotations)):
        annotation_lexeme = annotation['lexeme']
        assert lexeme.lemma == annotation_lexeme['lemma']


def test_annotate_text_some_known(language_datastore: PolishDatastore):
    lexeme_0_str = open('tests/interface/data/noun_ciało.json').read()
    lexeme_0 = json.loads(lexeme_0_str, cls=LexemeDecoder)
    lexeme_1_str = open('tests/interface/data/verb_być.json').read()
    lexeme_1 = json.loads(lexeme_1_str, cls=LexemeDecoder)

    lexemes = [lexeme_0, lexeme_1]
    language_datastore.add_lexemes(lexemes)

    text = "ciało jest prawdziwe."
    annotations = annotate_text(text, language_datastore, language="polish")

    assert annotations[0]['lexeme']['lemma'] == lexeme_0.lemma
    assert 'lexeme' not in annotations[2]


def test_annotate_text_some_known_discover(language_datastore: PolishDatastore):
    lexeme_0_str = open('tests/interface/data/noun_ciało.json').read()
    lexeme_0 = json.loads(lexeme_0_str, cls=LexemeDecoder)
    lexeme_1_str = open('tests/interface/data/verb_być.json').read()
    lexeme_1 = json.loads(lexeme_1_str, cls=LexemeDecoder)
    lexeme_2_str = open('tests/interface/data/adjective_prawdziwy.json').read()
    lexeme_2 = json.loads(lexeme_2_str, cls=LexemeDecoder)

    lexemes = [lexeme_0, lexeme_1]
    language_datastore.add_lexemes(lexemes)

    text = "ciało jest prawdziwe."
    annotations = annotate_text(text, language_datastore, language="polish", discovery_mode=True)

    assert annotations[0]['lexeme']['lemma'] == lexeme_0.lemma
    assert annotations[1]['lexeme']['lemma'] == lexeme_1.lemma
    assert annotations[2]['lexeme']['lemma'] == lexeme_2.lemma


def test_annotate_some_vocabulary(language_datastore: PolishDatastore):
    lexeme_0_str = open('tests/interface/data/noun_ciało.json').read()
    lexeme_0 = json.loads(lexeme_0_str, cls=LexemeDecoder)
    lexeme_1_str = open('tests/interface/data/verb_być.json').read()
    lexeme_1 = json.loads(lexeme_1_str, cls=LexemeDecoder)
    lexeme_2_str = open('tests/interface/data/adjective_prawdziwy.json').read()
    lexeme_2 = json.loads(lexeme_2_str, cls=LexemeDecoder)

    lexemes = [lexeme_0, lexeme_1]
    lexeme_ids = language_datastore.add_lexemes(lexemes)

    entry = {'lexeme_id': lexeme_ids[0], 'stats': {'definition': Stats()}, 'user_id': USER_ID}
    vocabulary_id_0 = language_datastore.add_vocabulary_entry(**entry)

    text = "ciało jest prawdziwe."
    annotations = annotate_text(text, language_datastore, language="polish", user_id=USER_ID)

    print(list(language_datastore.lexicon_connector.collection.find()))
    print(list(language_datastore.vocabulary_connector.collection.find()))

    assert annotations[0]['lexeme']['lemma'] == lexeme_0.lemma
    assert annotations[1]['lexeme']['lemma'] == lexeme_1.lemma
    assert 'lexeme' not in annotations[2]

    assert annotations[0]['vocabulary_id'] == vocabulary_id_0
    assert 'vocabulary_id' not in annotations[1] or annotations[1]['vocabulary_id'] == None
    assert 'vocabulary_id' not in annotations[2] or annotations[2]['vocabulary_id'] == None