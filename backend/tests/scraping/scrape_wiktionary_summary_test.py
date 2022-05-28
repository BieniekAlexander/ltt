#% imports
# pytest testing that exceptions are raised - https://stackoverflow.com/a/29855337
import os, sys, json, pytest, requests, time
from bs4 import BeautifulSoup


from scraping.wiktionary_scrape_summary_utils import wiktionary_get_all_lang_pos_lemmas

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
def test_get_all_polish_prepositions():
  summary_url = 'https://en.wiktionary.org/wiki/Category:Polish_prepositions'
  page = requests.get(summary_url)
  soup = BeautifulSoup(page.content, "html.parser")
  lemmas = wiktionary_get_all_lang_pos_lemmas(soup)
  
  for lemma in ['dla', 'miast', 'niby', 'w celu']:
    assert lemma in lemmas


#% main
def main():
  test_get_all_polish_prepositions()


if __name__ == "__main__":
  main()