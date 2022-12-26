# %% imports
import json

import pytest
from language.lexeme_decoder import LexemeDecoder
from mongomock import MongoClient
from storage.language_datastores.polish_datastore import PolishDatastore
from storage.datastore_utils import generate_query

# constants
LANGUAGE = "polish"


# %% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture(autouse=True)
def language_datastore() -> PolishDatastore:
    """
    Establish a connection to the mongodb database
    """
    ds_client = MongoClient()
    test_language_datastore = PolishDatastore(ds_client)

    # run test
    yield test_language_datastore

    # cleanup
    test_language_datastore.lexicon_connector.collection.drop({})


# %% tests
# push and get
def test_add_and_get_lexeme(language_datastore: PolishDatastore):
    json_str = open('tests/storage/data/noun_czerwony.json').read()
    lexeme = json.loads(json_str, cls=LexemeDecoder)
    language_datastore.add_lexeme(lexeme)
    returned_lexeme = language_datastore.get_lexeme_from_form(form=lexeme.inflections['S']['I'], pos="NOUN")

    assert returned_lexeme


def test_get_lexeme_none(language_datastore: PolishDatastore):
    noun_str = open('tests/storage/data/noun_czerwony.json').read()
    noun = json.loads(noun_str, cls=LexemeDecoder)
    adj_str = open('tests/storage/data/adjective_czerwony.json').read()
    adj = json.loads(adj_str, cls=LexemeDecoder)

    language_datastore.add_lexeme(noun)
    language_datastore.add_lexeme(adj)

    assert language_datastore.get_lexeme_from_form(form='niebieski', pos="ADJECTIVE") == None


def test_get_lexeme_wrong_pos_none(language_datastore: PolishDatastore):
    noun_str = open('tests/storage/data/noun_czerwony.json').read()
    noun = json.loads(noun_str, cls=LexemeDecoder)
    adj_str = open('tests/storage/data/adjective_czerwony.json').read()
    adj = json.loads(adj_str, cls=LexemeDecoder)

    language_datastore.add_lexeme(noun)
    language_datastore.add_lexeme(adj)

    assert language_datastore.get_lexeme_from_form(form='czerwony', pos="ADVERB") == None


def test_add_and_get_lexemes(language_datastore: PolishDatastore):
    noun_str = open('tests/storage/data/noun_czerwony.json').read()
    noun = json.loads(noun_str, cls=LexemeDecoder)
    adj_str = open('tests/storage/data/adjective_czerwony.json').read()
    adj = json.loads(adj_str, cls=LexemeDecoder)

    language_datastore.add_lexeme(noun)
    language_datastore.add_lexeme(adj)
    returned_lexemes = language_datastore.get_lexemes_from_form(
        form='czerwony')

    assert returned_lexemes


def test_get_lexemes_none(language_datastore: PolishDatastore):
    noun_str = open('tests/storage/data/noun_czerwony.json').read()
    noun = json.loads(noun_str, cls=LexemeDecoder)
    adj_str = open('tests/storage/data/adjective_czerwony.json').read()
    adj = json.loads(adj_str, cls=LexemeDecoder)

    language_datastore.add_lexeme(noun)
    language_datastore.add_lexeme(adj)

    assert language_datastore.get_lexemes_from_form(form='niebieski') == []


def test_get_lexemes_wrong_pos_none(language_datastore: PolishDatastore):
    noun_str = open('tests/storage/data/noun_czerwony.json').read()
    noun = json.loads(noun_str, cls=LexemeDecoder)
    adj_str = open('tests/storage/data/adjective_czerwony.json').read()
    adj = json.loads(adj_str, cls=LexemeDecoder)

    language_datastore.add_lexeme(noun)
    language_datastore.add_lexeme(adj)

    assert language_datastore.get_lexemes_from_form(
        form='niebieski', pos=['VERB', 'ADVERB']) == []


# %% main
def main():
    pass


if __name__ == "__main__":
    main()
