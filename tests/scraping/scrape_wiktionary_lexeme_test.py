# tests for utilities for scraping tables from html
#% imports
# pytest testing that exceptions are raised - https://stackoverflow.com/a/29855337
import os, sys, json, pytest, requests, time
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from scraping.wiktionary_scrape_lexeme_utils import find_language_header, get_inflection_table, get_lemma, get_summary_paragraph, seek_inflection_table, seek_pos_header
from scraping.scraping_errors import ScrapingFindError

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
def test_find_polish_entry():
  lemma, language = "ptak", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lang_header = find_language_header(soup, language)
  assert lang_header


def test_find_polish_entry_fails():
  lemma, language = "spruce", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")

  with pytest.raises(ScrapingFindError):
    lang_header = find_language_header(soup, language)


def test_find_polish_part_of_speech_entry():
  lemma, language, pos = "ptak", "Polish", "Noun"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lang_header = find_language_header(soup, language)
  pos_header = seek_pos_header(lang_header, pos, language)
  assert pos_header


def test_find_polish_part_of_speech_entry_fails():
  lemma, language, pos = "ptak", "Polish", "Verb"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lang_header = find_language_header(soup, language)
  
  with pytest.raises(ScrapingFindError):
    pos_header = seek_pos_header(lang_header, pos, language)


def test_find_polish_part_of_speech_entry_in_wrong_language_fails():
  lemma, language, pos = "pies", "Polish", "Verb"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lang_header = find_language_header(soup, language)
  
  with pytest.raises(ScrapingFindError):
    pos_header = seek_pos_header(lang_header, pos, language)


def test_find_polish_inflection_table_verb():
  lemma, language, pos = "jeść", "Polish", "Verb"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  inflection_table = get_inflection_table(soup, pos, language)
  assert inflection_table


def test_find_polish_inflection_table_noun():
  lemma, language, pos = "zima", "Polish", "Noun"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  inflection_table = get_inflection_table(soup, pos, language)
  assert inflection_table


def test_find_polish_inflection_table_adjective():
  lemma, language, pos = "czerwony", "Polish", "Adjective"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  inflection_table = get_inflection_table(soup, pos, language)
  assert inflection_table


def test_find_polish_summary_phrase_preposition():
  lemma, language, pos = "pod względem", "Polish", "Preposition"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma.replace(' ', '_')}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  summary_paragraph = get_summary_paragraph(soup, pos, language)
  assert summary_paragraph


def test_find_polish_inflection_table_preposition_fails():
  lemma, language, pos = "obok", "Polish", "Preposition"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  
  with pytest.raises(ScrapingFindError):
    inflection_table = get_inflection_table(soup, pos, language)


def test_find_polish_inflection_table_not_in_pos_fails():
  lemma, language, pos = "zimno", "Polish", "Adverb"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  
  with pytest.raises(ScrapingFindError):
    inflection_table = get_inflection_table(soup, pos, language)


def test_find_polish_lemma():
  term, language, pos = "psa", "Polish", "Noun"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  lemma = get_lemma(soup, pos, language)

  assert lemma == "pies"


def test_find_polish_lemma_multiple_inflections():
  term, language, pos = "szare", "Polish", "Adjective"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  lemma = get_lemma(soup, pos, language)

  assert lemma == "szary"
  

def test_find_polish_lemma_fails():
  term, language, pos = "pies", "Polish", "Noun"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  lemma = get_lemma(soup, pos, language)

  assert lemma == None


def test_find_polish_lemma_fails_on_wrong_lemma():
  # might get confused with the Welsh entry - "soft mutation of gwe"
  term, language, pos = "we", "Polish", "Preposition"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lemma = get_lemma(soup, pos, language)
  
  assert lemma == None


#% main
def main():
  test_find_polish_lemma_fails_on_wrong_lemma()


if __name__ == "__main__":
  main()