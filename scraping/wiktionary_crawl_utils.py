#%% imports
from bs4 import BeautifulSoup
import requests, os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scraping.wiktionary_scrape_lexeme_utils import get_lemma
from scraping.scraping_errors import ScrapingAssertionError
from scraping import get_wiktionary_term_url, get_soup_from_url


#%% utils
def has_entries(soup):
  """
  Returns true if the page has entries
  """
  return not bool(soup.find('div', {'class': 'noarticletext'}))


def get_search_result_links(soup, domain_name="https://en.wiktionary.org"):
  """
  Returns the linked articles in a wiktionary search results page
  """
  search_results_ul = soup.find('ul', {'class': 'mw-search-results'})
  none_found_p = soup.find('p', {'class': 'mw-search-nonefound'})

  if none_found_p:
    return []
  elif search_results_ul:  
    search_results_lis = list(search_results_ul.find_all('li', recursive=False))
    print(search_results_lis)
    return [domain_name+li.find('a')['href'] for li in search_results_lis]
  else:
    raise ScrapingAssertionError(soup, {}, "failed to find search results on this page - maybe the page isn't a wiktionary search results page?")


def navigate_to_lexeme_page(form: str, pos: str, language: str) -> BeautifulSoup:
  """
  Given some (potentially) inflected form of a word, find the page which contains the main lexeme entry
  """
  # check if the [form] is the lemma
  # TODO
  soup = get_soup_from_url(get_wiktionary_term_url(form))

  if has_entries(soup): # this page has wiktionary entries
    lemma = get_lemma(soup, pos, language)
     
    if form == lemma: # the webpage contains the lexeme
      return soup


#%% main
def main():
  soup = get_soup_from_url(get_wiktionary_term_url('czerwony'))
  print(type(soup))

if __name__ == "__main__":
  main()