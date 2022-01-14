# tests for utilities for scraping tables from html
#% imports
# pytest testing that exceptions are raised - https://stackoverflow.com/a/29855337
import os, sys, json, pytest, requests, time
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from scraping.wiktionary_scrape_lexeme_utils import find_language_header, get_inflection_table, get_lemma, get_summary_paragraph, seek_pos_header, get_term_parts_of_speech
from scraping.scraping_errors import ScrapingFormatError

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


def test_find_polish_entry_returns_none():
  lemma, language = "spruce", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")

  assert find_language_header(soup, language) == None


def test_find_polish_part_of_speech_entry():
  lemma, language, pos = "ptak", "Polish", "Noun"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lang_header = find_language_header(soup, language)
  pos_header = seek_pos_header(lang_header, pos, language)
  assert pos_header


def test_find_polish_part_of_speech_entry_returns_none():
  lemma, language, pos = "ptak", "Polish", "Verb"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lang_header = find_language_header(soup, language)
  
  assert seek_pos_header(lang_header, pos, language) == None


def test_find_polish_part_of_speech_entry_in_wrong_language_returns_none():
  lemma, language, pos = "pies", "Polish", "Verb"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lang_header = find_language_header(soup, language)
  
  assert seek_pos_header(lang_header, pos, language) == None


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
  
  assert get_inflection_table(soup, pos, language) == None


def test_find_polish_inflection_table_not_in_pos_fails():
  lemma, language, pos = "zimno", "Polish", "Adverb"
  termUrl = f"https://en.wiktionary.org/wiki/{lemma}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  
  assert get_inflection_table(soup, pos, language) == None


def test_find_polish_lemma_on_lexeme_entry():
  term, language, pos = "pies", "Polish", "Noun"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  lemma = get_lemma(soup, pos, language)

  assert lemma == "pies"


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
  

def test_find_polish_lemma_wrong_pos_returns_none():
  term, language, pos = "pies", "Polish", "Adjective"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  lemma = get_lemma(soup, pos, language)

  assert lemma == None


def test_find_polish_lemma_wrong_language_returns_none():
  term, language, pos = "amo", "Polish", "Noun"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 
  
  assert get_lemma(soup, pos, language) == None


def test_find_polish_lemma_no_entry_returns_none():
  # TODO same as above
  term, language, pos = "fearful", "Polish", "Noun"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser") 

  assert get_lemma(soup, pos, language) == None


def test_find_polish_lemma_returns_none_on_wrong_lemma():
  # testing that scraper doesn't get confused with the Welsh entry - "soft mutation of gwe"
  term, language, pos = "we", "Polish", "Noun"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  lemma = get_lemma(soup, pos, language)
  
  assert lemma == None


def test_get_polish_term_parts_of_speech():
  term, language = "piekło", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  term_parts_of_speech = get_term_parts_of_speech(soup, language)

  assert all(pos in term_parts_of_speech for pos in ['verb', 'noun'])


def test_get_polish_term_parts_of_speech_many_languages():
  # only adjective in Polish, but also a Noun in Romanian, Verb in Tarantino
  term, language = "stare", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  term_parts_of_speech = get_term_parts_of_speech(soup, language)

  assert 'adjective' in term_parts_of_speech
  assert all(pos not in term_parts_of_speech for pos in ['verb', 'noun'])


def test_get_polish_term_parts_of_speech_no_polish():
  # TODO raises exception when there is no section on the page for the given language - do I wan't exception or just empty list?
  term, language = "no_way", "Polish"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  
  with pytest.raises(ScrapingFormatError):
    get_term_parts_of_speech(soup, language)

  

#% main
def main():
  test_find_polish_lemma_on_lexeme_entry()


if __name__ == "__main__":
  main()