#%% imports
import os, sys, json, pytest, requests, time
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from scraping.wiktionary_extract_utils import extract_lexeme

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
# TODO check values in extracted lexemes
def test_serialize_polish_noun_kot_to_json_dict():
  lemma, pos, language = "kot", "Noun", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  lexeme_json_dict = lexeme.to_json_dict()
  assert lexeme_json_dict['pos'] == "NOUN"
  assert lexeme_json_dict['lemma'] == "kot"
  assert lexeme_json_dict['inflections']['P']['A'] == "koty"


def test_serialize_polish_noun_kot_to_json_str():
  lemma, pos, language = "czerwony", "Adjective", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  lexeme_json_str = lexeme.to_json_str()


#%% main
def main():
  test_serialize_polish_noun_kot_to_json_dict()

if __name__ == "__main__":
  main()