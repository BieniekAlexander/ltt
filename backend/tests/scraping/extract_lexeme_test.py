# tests for utilities for scraping tables from html
# % imports
# pytest testing that exceptions are raised - https://stackoverflow.com/a/29855337
import time

import pytest
import requests
from bs4 import BeautifulSoup
from language.part_of_speech import PartOfSpeech
from language.polish.feat.abstraction import Abstraction
from language.polish.feat.animacy import Animacy
from language.polish.feat.aspect import Aspect
from language.polish.feat.case import Case
from language.polish.feat.degree import Degree
from language.polish.feat.gender import Gender
from language.polish.feat.virility import Virility
from scraping.wiktionary_extract_lexeme_utils import extract_lexeme

# constants
CRAWL_DELAY = 5


# %% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture(autouse=True)
def web_crawler_delay():
    # setup
    time.sleep(CRAWL_DELAY)

    # run test
    yield


# % tests
def test_extract_polish_noun_kot():
    lemma, pos, language = "kot", "Noun", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.NOUN
    assert lexeme.diminutive == ['kotek', 'koteczek']
    assert lexeme.gender == Gender.MALE
    assert lexeme.animacy == Animacy.ANIMATE
    assert lexeme.virility == None
    assert 'cat, tomcat' in lexeme.definitions[0]
    # TODO maybe make accessing of inflections a bit more elegant?
    assert lexeme.inflections['S']['N'] == "kot"
    assert lexeme.inflections['P']['L'] == "kotach"


def test_extract_polish_noun_zimno():
    lemma, pos, language = "zimno", "Noun", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.NOUN
    assert lexeme.gender == Gender.NEUTER
    assert lexeme.animacy == None
    assert lexeme.virility == None
    assert 'cold' in lexeme.definitions[0]
    assert lexeme.inflections['S']['D'] == "zimnu"
    assert 'P' not in lexeme.inflections


def test_extract_polish_noun_drzwi():
    lemma, pos, language = "drzwi", "Noun", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.NOUN
    assert lexeme.gender == None
    assert lexeme.animacy == None
    assert lexeme.virility == Virility.NONVIRILE
    assert 'door' in lexeme.definitions[0]
    assert lexeme.inflections['P']['I'] == "drzwiami"
    assert 'S' not in lexeme.inflections


def test_extract_polish_verb_pojsc():
    lemma, pos, language = "pójść", "Verb", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.VERB
    assert lexeme.aspect == Aspect.PERFECT
    assert lexeme.abstraction == None
    assert lexeme.is_frequentative == False
    assert 'to go, to walk' in lexeme.definitions[0]
    assert lexeme.inflections['S']['M']['F']['1'] == "pójdę"


def test_extract_polish_verb_isc():
    lemma, pos, language = "iść", "Verb", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.VERB
    assert lexeme.aspect == Aspect.IMPERFECT
    assert lexeme.abstraction == None
    assert lexeme.is_frequentative == False
    assert 'to go, to walk' in lexeme.definitions[0]
    assert "będziesz szedł" in lexeme.inflections['S']['M']['F']['2']


def test_extract_polish_verb_chodzic():
    lemma, pos, language = "chodzić", "Verb", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.VERB
    assert lexeme.aspect == Aspect.IMPERFECT
    # assert lexeme.abstraction == Abstraction.INDETERMINATE TODO fix chodzić wikipedia page to have this data
    assert lexeme.is_frequentative == False
    assert 'to walk' in lexeme.definitions[0]
    assert lexeme.inflections['P']['N']['Past']['1'] == "chodziłyśmy"


def test_extract_polish_verb_jadac():
    lemma, pos, language = "jadać", "Verb", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.VERB
    assert lexeme.aspect == Aspect.IMPERFECT
    assert lexeme.abstraction == Abstraction.INDETERMINATE
    assert lexeme.is_frequentative == True
    assert 'to eat habitually' in lexeme.definitions[0]
    assert lexeme.inflections['S']['M']['Inf'] == "jadać"


def test_extract_polish_verb_chciec():
    lemma, pos, language = "chcieć", "Verb", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.VERB
    assert lexeme.aspect == Aspect.IMPERFECT
    assert lexeme.abstraction == None
    assert lexeme.is_frequentative == False
    assert 'to want' in lexeme.definitions[0]
    assert lexeme.inflections['S']['M']['C']['1'] == "chciałbym"


def test_extract_polish_adverb_szybko():
    lemma, pos, language = "szybko", "Adverb", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.ADVERB
    assert lexeme.degree == Degree.POSITIVE
    assert 'szybciej' in lexeme.comparative
    assert 'najszybciej' in lexeme.superlative
    assert 'quickly, rapidly, fast' in lexeme.definitions[0]


def test_extract_polish_adjective_szybki():
    lemma, pos, language = "szybki", "Adjective", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.ADJECTIVE
    assert lexeme.degree == Degree.POSITIVE
    assert 'szybszy' in lexeme.comparative
    assert 'najszybszy' in lexeme.superlative
    assert 'szybko' in lexeme.adverb
    assert 'fast' in lexeme.definitions[0]
    assert lexeme.inflections['S']['I']['N'] == "szybki"


def test_extract_polish_adjective_czerwony():
    lemma, pos, language = "czerwony", "Adjective", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.ADJECTIVE
    assert lexeme.degree == Degree.POSITIVE
    assert lexeme.not_comparable == False
    assert 'czerwieńszy' in lexeme.comparative
    assert 'najbardziej czerwony' in lexeme.superlative
    assert 'czerwono' in lexeme.adverb
    assert 'red' in lexeme.definitions[0]
    assert lexeme.inflections['S']['N']['V'] == "czerwone"


def test_extract_polish_adjective_czerwonawy():
    lemma, pos, language = "czerwonawy", "Adjective", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.ADJECTIVE
    assert lexeme.degree == Degree.POSITIVE
    assert lexeme.not_comparable == True
    assert lexeme.comparative == []
    assert lexeme.superlative == []
    assert 'reddish' in lexeme.definitions[0]
    assert lexeme.inflections['S']['F']['G'] == "czerwonawej"


def test_extract_polish_adjective_bogatszy():
    lemma, pos, language = "bogatszy", "Adjective", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.ADJECTIVE
    assert lexeme.degree == Degree.COMPARATIVE
    assert 'bogaty' in lexeme.positive
    assert lexeme.comparative == []
    assert 'comparative degree of bogaty' in lexeme.definitions[0]
    assert lexeme.inflections['P']['N']['D'] == "bogatszym"


def test_extract_polish_adjective_najlepszy():
    lemma, pos, language = "najlepszy", "Adjective", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.ADJECTIVE
    assert lexeme.degree == Degree.SUPERLATIVE
    assert 'dobry' in lexeme.positive
    assert lexeme.superlative == []
    assert 'superlative degree of dobry; best' in lexeme.definitions[0]
    assert lexeme.inflections['P']['V']['I'] == "najlepszymi"


def test_extract_polish_conjunction_ale():
    lemma, pos, language = "ale", "Conjunction", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.CONJUNCTION
    assert 'but' in lexeme.definitions[0]


def test_extract_polish_conjunction_lecz():
    lemma, pos, language = "lecz", "Conjunction", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.CONJUNCTION
    assert 'but' in lexeme.definitions[0]


def test_extract_polish_conjunction_bowiem():
    lemma, pos, language = "bowiem", "Conjunction", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.CONJUNCTION
    assert 'because' in lexeme.definitions[0]


def test_extract_polish_interjection_kurwa():
    lemma, pos, language = "kurwa", "interjection", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.INTERJECTION
    assert '(vulgar) fuck!, shit!, damn!' in lexeme.definitions[0]


def test_extract_polish_interjection_moment():
    lemma, pos, language = "moment", "Interjection", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.INTERJECTION
    assert 'wait a minute' in lexeme.definitions[0]


def test_extract_polish_preposition_wsrod():
    lemma, pos, language = "wśród", "Preposition", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.PREPOSITION
    assert 'among, amidst' in lexeme.definitions[0]
    assert Case.GENITIVE in lexeme.cases


def test_extract_polish_preposition_bez():
    lemma, pos, language = "bez", "Preposition", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.PREPOSITION
    assert 'without, lacking' in lexeme.definitions[0]
    assert Case.GENITIVE in lexeme.cases


def test_extract_polish_preposition_za():
    lemma, pos, language = "za", "Preposition", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.PREPOSITION
    assert 'behind, beyond' in lexeme.definitions[0]
    assert Case.INSTRUMENTAL in lexeme.cases
    assert Case.ACCUSATIVE in lexeme.cases


def test_extract_polish_numeral_kilka():
    lemma, pos, language = "kilka", "Numeral", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.NUMERAL
    assert 'more than two' in lexeme.definitions[0]
    assert lexeme.inflections['P']['N']['G'] == 'kilku'


def test_extract_polish_numeral_piec():
    lemma, pos, language = "pięć", "Numeral", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.NUMERAL
    assert 'five' in lexeme.definitions[0]
    assert lexeme.inflections['P']['V']['I'] == 'pięcioma'


def test_extract_polish_particle_albo():
    lemma, pos, language = "albo", "particle", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.PARTICLE
    assert "used to express the speaker's doubt or surprise" in lexeme.definitions[0]


def test_extract_polish_particle_jeszcze():
    lemma, pos, language = "jeszcze", "particle", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.PARTICLE
    assert "yet (used with negated verbs)" in lexeme.definitions[0]


def test_extract_polish_pronoun_siebie():
    lemma, pos, language = "siebie", "pronoun", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.PRONOUN
    assert "reflexive pronoun" in lexeme.definitions[0]
    assert 'siebie' in lexeme.inflections['S']['A']


def test_extract_polish_pronoun_ja():
    lemma, pos, language = "ja", "pronoun", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.PRONOUN
    assert "I (first-person pronoun)" in lexeme.definitions[0]
    assert 'mną' in lexeme.inflections['S']['I']


def test_extract_polish_pronoun_oni():
    lemma, pos, language = "oni", "pronoun", "Polish"
    page_content = open(
        f'tests/data/wiktionary/en/wiki_{lemma}.html', 'r').read()
    soup = BeautifulSoup(page_content, "html.parser")
    lexeme = extract_lexeme(soup, lemma, pos, language)

    assert lexeme.pos == PartOfSpeech.PRONOUN
    assert "they (third-person masculine personal nominative)" in lexeme.definitions[0]
    assert 'nim' in lexeme.inflections['P']['D']


# % main
def main():
    pass
    # test_crawl_pl_simple()


if __name__ == "__main__":
    main()
