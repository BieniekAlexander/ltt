#%% imports
import os, sys, json, pytest, requests, time
from bs4 import BeautifulSoup


from scraping.wiktionary_extract_lexeme_utils import extract_lexeme
from language.lexeme import LexemeEncoder

# constants
CRAWL_DELAY = 5


#%% pytest fixtures
# https://stackoverflow.com/questions/22627659/run-code-before-and-after-each-test-in-py-test, https://docs.pytest.org/en/6.2.x/fixture.html
@pytest.fixture(autouse=True)
def web_crawler_delay():
  # setup
  time.sleep(CRAWL_DELAY)
  
  # run test
  yield


#% tests
def test_serialize_polish_lexeme_to_json_dictionary():
  lemma, pos, language = "jeszcze", "particle", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  lexeme_json_dict = lexeme.to_json_dictionary()
  assert lexeme_json_dict


def test_serialize_polish_lexeme_with_json_encoder():
  lemma, pos, language = "choć", "conjunction", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  lexeme_json_dict = json.dumps(lexeme, cls=LexemeEncoder)
  assert isinstance(lexeme_json_dict, str)


def test_serialize_polish_lexeme_to_json_str():
  lemma, pos, language = "chociaż", "conjunction", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  lexeme_json_str = lexeme.to_json_str()
  print(lexeme_json_str)
  assert isinstance(lexeme_json_str, str)


def test_serialize_polish_noun():
  lemma, pos, language = "kot", "Noun", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  lexeme_json_dict = lexeme.to_json_dictionary()
  assert lexeme_json_dict['pos'] == "NOUN"
  assert lexeme_json_dict['lemma'] == "kot"
  assert lexeme_json_dict['inflections']['P']['A'] == "koty"


def test_serialize_polish_verb():
  lemma, pos, language = "mieć", "Verb", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  lexeme_json_dict = lexeme.to_json_dictionary()
  assert lexeme_json_dict['pos'] == "VERB"
  assert lexeme_json_dict['lemma'] == "mieć"
  assert lexeme_json_dict['inflections']['S']['M']['Pres']['1'] == "mam"


def test_serialize_polish_adjective():
  lemma, pos, language = "brzydszy", "Adjective", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  lexeme_json_dict = lexeme.to_json_dictionary()
  assert lexeme_json_dict['pos'] == "ADJECTIVE"
  assert lexeme_json_dict['lemma'] == "brzydszy"
  assert lexeme_json_dict['degree'] == "COMPARATIVE"
  assert lexeme_json_dict['inflections']['S']['N']['A'] == "brzydsze"


def test_serialize_polish_adverb():
  lemma, pos, language = "najszybciej", "Adverb", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  lexeme_json_dict = lexeme.to_json_dictionary()
  assert lexeme_json_dict['pos'] == "ADVERB"
  assert lexeme_json_dict['lemma'] == "najszybciej"
  assert lexeme_json_dict['degree'] == "SUPERLATIVE"


#%% main
def main():
  test_serialize_polish_lexeme_to_json_str()

if __name__ == "__main__":
  main()