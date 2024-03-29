# %% imports
import json

import pytest
from language.lexeme import Lexeme
from language.lexeme_decoder import LexemeDecoder
from mongomock import MongoClient
from storage.lexicon_connector import LexiconConnector

# constants
LANGUAGE = "polish"


# %% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture(autouse=True)
def lexicon_connector():
    """
    Establish a connection to the mongodb database
    """
    ds_client = MongoClient()
    test_lexicon_connector = LexiconConnector(ds_client, LANGUAGE)

    # run test
    yield test_lexicon_connector

    # cleanup
    test_lexicon_connector.collection.drop()
    test_lexicon_connector.collection.drop_indexes()


# %% tests
def test_push_and_get_lexeme_entry(lexicon_connector):
    lexeme = Lexeme('ope', 'CONJUNCTION', [])
    lexeme_dict = lexeme.to_json()
    lexicon_connector.push_lexeme_entry(lexeme_dict)
    entry = lexicon_connector.get_lexeme_entry(
        lemma=lexeme.lemma, pos=lexeme.pos)

    assert lexeme.lemma == entry['lemma']


def test_push_and_get_lexeme_entries(lexicon_connector):
    lemmas = ['hi', 'julia']
    lexemes = [Lexeme(l, "CONJUNCTION", []) for l in lemmas]
    lexicon_connector.push_lexeme_entries(lexemes)
    returned_lexeme_entries = lexicon_connector.get_lexeme_entries(
        lemmas=lemmas)

    for entry in returned_lexeme_entries:
        print(returned_lexeme_entries)
        assert entry['lemma'] in lemmas


# push and delete
def test_push_and_delete_lexeme_entry(lexicon_connector):
    lexeme = Lexeme('ope', 'CONJUNCTION', [])
    lexeme_dict = lexeme.to_json()
    lexicon_connector.push_lexeme_entry(lexeme_dict)
    lexicon_connector.delete_lexeme_entry(lemma=lexeme.lemma, pos=lexeme.pos)


def test_push_and_delete_lexeme_entries(lexicon_connector):
    lemmas = ['hi', 'julia']
    lexemes = [Lexeme(l, "CONJUNCTION", []) for l in lemmas]
    lexicon_connector.push_lexeme_entries(lexemes)
    lexicon_connector.delete_lexeme_entries(lemmas=lemmas)


def test_multiple_lexemes_same_lemma_get_lexeme_fails(lexicon_connector):
    noun_str = open('tests/storage/data/noun_czerwony.json').read()
    noun = json.loads(noun_str, cls=LexemeDecoder)
    adj_str = open('tests/storage/data/adjective_czerwony.json').read()
    adj = json.loads(adj_str, cls=LexemeDecoder)
    lexemes = [noun, adj]
    lexicon_connector.push_lexeme_entries(lexemes)

    with pytest.raises(Exception):  # TODO change exception type
        _, returned_lexeme = lexicon_connector.get_lexeme_entry(
            lemma='czerwony')


# % main
def main():
    pass


if __name__ == "__main__":
    main()
