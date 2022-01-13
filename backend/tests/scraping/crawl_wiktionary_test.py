# tests for utilities for scraping tables from html
#% imports
# pytest testing that exceptions are raised - https://stackoverflow.com/a/29855337
import os, sys, json, pytest, requests, time
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from scraping.wiktionary_crawl_utils import get_search_result_links, is_no_entries_page, get_lexeme_page_soup
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


def test_verify_has_entries_true():
  term = "red"
  soup = get_soup_from_url(get_wiktionary_term_url(term))
  assert not is_no_entries_page(soup)


def test_verify_has_entries_false():
  term = "babadook"
  soup = get_soup_from_url(get_wiktionary_term_url(term))
  assert is_no_entries_page(soup)


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


#% main
def main():
  pass
  

if __name__ == "__main__":
  main()