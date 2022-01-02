# tests for utilities for scraping tables from html
#% imports
# pytest testing that exceptions are raised - https://stackoverflow.com/a/29855337
import os, sys, json, pytest, requests, time
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from scraping.wiktionary_crawl_utils import get_search_result_links, has_entries, get_lexeme_page_soup
from scraping.scraping_errors import ScrapingFormatError
from scraping.wiktionary_extract_lexeme_utils import extract_lexeme
from scraping import get_soup_from_url, get_wiktionary_term_url, get_wiktionary_search_url

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
def test_verify_has_entries_true():
  term = "red"
  soup = get_soup_from_url(get_wiktionary_term_url(term))
  assert has_entries(soup)


def test_verify_has_entries_false():
  term = "babadook"
  soup = get_soup_from_url(get_wiktionary_term_url(term))
  assert not has_entries(soup)


def test_get_search_results():
  term = "niemożliwe"
  soup = get_soup_from_url(get_wiktionary_search_url(term))
  returned_links = get_search_result_links(soup)
  links = ['https://en.wiktionary.org/wiki/no_way','https://en.wiktionary.org/wiki/niemo%C5%BCliwy']
  assert all(link in returned_links for link in links)


def test_get_search_results_empty():
  term = "babadook"
  soup = get_soup_from_url(get_wiktionary_search_url(term))
  returned_links = get_search_result_links(soup)
  assert returned_links == []


def test_get_search_results_fail():
  term = 'potato'
  soup = get_soup_from_url(get_wiktionary_term_url(term))

  with pytest.raises(AssertionError): # TODO change exception type
    get_search_result_links(soup)


def test_get_lexeme_simple():
  form, pos, language = "czerwony", "adjective", "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  assert lexeme.lemma == "czerwony"


def test_get_lexeme_alternate_form():
  form, pos, language = "czerwona", "adjective", "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  assert lexeme.lemma == "czerwony"

  
def test_get_lexeme_special_characters():
  form, pos, language = "miłość", "Noun", "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  assert lexeme.lemma == "miłość"
  

def test_get_lexeme_special_characters_alternate_form():
  # TODO - address failing case - miłości's first few search results are wrong, maybe I should collect the lexeme result and verify that the initial form I queried with is in the inflection table
  # https://en.wiktionary.org/w/index.php?search=mi%C5%82o%C5%9B%C4%87i&title=Special:Search&profile=advanced&fulltext=1&searchengineselect=mediawiki&ns0=1
  form, pos, language = "miłośći", "Noun", "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  assert lexeme.lemma == "miłość"
  

def test_get_lexeme_special_characters_uses_search():
  form, pos, language = "niemożliwe", "Adjective", "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  assert lexeme.lemma == "niemożliwy"


def test_get_lexeme_no_pos():
  form, pos, language = "piekło", None, "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  assert lexeme.lemma == "piekło"
  assert lexeme.pos.value == "NOUN"
  

def test_get_lexeme_no_pos_alternate_form():
  # this can potentially find piec - VERB, or piekło - NOUN
  # TODO this is actually returning things stochastically - sometimes one form, sometimes the other
  # TODO how am I solving for this ambiguity? When I see a word in text, how am I assessing which POS I think it is?
  form, pos, language = "piekła", None, "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  assert lexeme.lemma == "piec"
  assert lexeme.pos.value == "VERB"


def test_get_lexeme_form_is_lemma_of_other_pos_in_page():
  form, pos, language = "piekło", "Verb", "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  assert lexeme.lemma == "piec"
  assert lexeme.pos.value == "VERB"


def test_get_lexeme_multiple_non_lemma_forms_in_page():
  form, pos, language = "piekła", "Verb", "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)
  
  assert lexeme.lemma == "piec"
  assert lexeme.pos.value == "VERB"


def test_get_lexeme_search_results_fail():
  form, pos, language = "zničeno", None, "Polish"
  assert not get_lexeme_page_soup(form, pos, language)


def test_get_lexeme_multiple_steps():
  form, pos, language = "swe", None, "Polish"
  soup, lemma, pos = get_lexeme_page_soup(form, pos, language)
  lexeme = extract_lexeme(soup, lemma, pos, language)

  assert lexeme.lemma == "swój"
  assert lexeme.pos.value == "PRONOUN"  


#% main
def main():
  pass
  

if __name__ == "__main__":
  main()