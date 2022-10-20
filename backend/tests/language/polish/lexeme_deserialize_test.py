# %% imports
import json

from bs4 import BeautifulSoup
from language.lexeme_decoder import LexemeDecoder
from language.part_of_speech import PartOfSpeech
from scraping.wiktionary_extract_lexeme_utils import extract_lexeme
from utils.json_utils import JSONSerializableEncoder

# %% pytest fixtures


# % tests
def test_deserialize_polish_lexeme_basic():
    json_str = open('tests/language/polish/data/particle_niemal.json').read()
    lexeme = json.loads(json_str, cls=LexemeDecoder)

    assert lexeme.lemma == "niemal"
    assert 'almost, nearly, practically' in lexeme.definitions[0]
    assert lexeme.pos == PartOfSpeech.PARTICLE


def test_deserialize_polish_lexeme_special_characters():
    json_str = open('tests/language/polish/data/conjunction_choc.json').read()
    lexeme = json.loads(json_str, cls=LexemeDecoder)

    assert lexeme.lemma == "choć"


def test_deserialize_polish_lexeme_encoded_characters():
    json_str = open(
        'tests/language/polish/data/conjunction_chociaz.json').read()
    lexeme = json.loads(json_str, cls=LexemeDecoder)

    assert lexeme.lemma == "chociaż"


def test_deserialize_polish_adjective():
    json_str = open(
        'tests/language/polish/data/adjective_czerwony.json').read()
    lexeme = json.loads(json_str, cls=LexemeDecoder)

    assert lexeme.lemma == "czerwony"
    assert 'red' in lexeme.definitions[0]
    assert lexeme.pos == PartOfSpeech.ADJECTIVE
    print(lexeme.inflections)
    assert lexeme.inflections['S']['F']['A'] == "czerwoną"


def test_deserialize_polish_noun():
    json_str = open('tests/language/polish/data/noun_pies.json').read()
    lexeme = json.loads(json_str, cls=LexemeDecoder)

    assert lexeme.lemma == "noun"
    assert 'dog' in lexeme.definitions[0]
    assert lexeme.pos == PartOfSpeech.NOUN
    assert lexeme.inflections['P']['I'] == "psami"


def test_deserialize_polish_noun():
    json_str = open('tests/language/polish/data/noun_pies.json').read()
    lexeme = json.loads(json_str, cls=LexemeDecoder)

    assert lexeme.lemma == "pies"
    assert 'dog' in lexeme.definitions[0]
    assert lexeme.pos == PartOfSpeech.NOUN
    assert lexeme.inflections['P']['I'] == "psami"


def test_encoding_invertible_polish_noun():
    lemma, pos, language = "kot", "Noun", "Polish"
    page_content = open('tests/data/wiktionary/en/wiki_kot.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    json_str = json.dumps(lexeme, cls=JSONSerializableEncoder)
    decoded_lexeme = json.loads(json_str, cls=LexemeDecoder)
    assert lexeme == decoded_lexeme


# %% main
def main():
    test_deserialize_polish_lexeme_special_characters()


if __name__ == "__main__":
    main()
