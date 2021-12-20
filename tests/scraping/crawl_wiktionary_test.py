# tests for utilities for scraping tables from html
#% imports
# pytest testing that exceptions are raised - https://stackoverflow.com/a/29855337
import os, sys, json, pytest, requests, time
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from scraping.wiktionary_crawl_utils import get_search_result_links, has_entries
from scraping.scraping_errors import ScrapingAssertionError

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
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  assert has_entries(soup)


def test_verify_has_entries_false():
  term = "babadook"
  termUrl = f"https://en.wiktionary.org/wiki/{term}"
  page = requests.get(termUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  assert not has_entries(soup)


def test_get_search_results():
  term = "niemożliwe"
  searchUrl = f"https://en.wiktionary.org/w/index.php?search={term}"
  page = requests.get(searchUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  returned_links = get_search_result_links(soup)
  links = ['https://en.wiktionary.org/wiki/no_way','https://en.wiktionary.org/wiki/niemo%C5%BCliwy']
  print(returned_links)
  assert all(link in returned_links for link in links)


def test_get_search_results_empty():
  term = "babadook"
  searchUrl = f"https://en.wiktionary.org/w/index.php?search={term}"
  page = requests.get(searchUrl)
  soup = BeautifulSoup(page.content, "html.parser")
  returned_links = get_search_result_links(soup)
  assert returned_links == []


def test_get_search_results_fail():
  searchUrl = f"https://en.wiktionary.org/wiki/potato"
  page = requests.get(searchUrl)
  soup = BeautifulSoup(page.content, "html.parser")

  with pytest.raises(ScrapingAssertionError): # TODO change exception type
    get_search_result_links(soup)
  


#% main
def main():
  pass
  

if __name__ == "__main__":
  main()