#%% imports
import requests, os, sys, logging
from bs4 import BeautifulSoup
from urllib.parse import unquote

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scraping.wiktionary_scrape_lexeme_utils import get_lemma, get_term_parts_of_speech
from scraping.scraping_errors import ScrapingFormatError
from scraping import get_wiktionary_term_url, get_soup_from_url, get_wiktionary_search_url


#%% utils
def has_entries(soup):
  """
  Returns true if the page has entries
  """
  return not bool(soup.find('div', {'class': 'noarticletext'}))


def is_search_results_page(soup):
  """
  Returns true if this wiktionary webpage is a search results webpage
  """
  return bool(soup.find('ul', {'class': 'mw-search-results'})) \
    or bool(soup.find('p', {'class': 'mw-search-nonefound'}))


def get_search_result_links(soup, domain_name="https://en.wiktionary.org"):
  """
  Returns the linked articles in a [soup] wiktionary search results page

  Asserts that the page is a wiktionary search results page
  """
  assert is_search_results_page(soup)

  search_results_ul = soup.find('ul', {'class': 'mw-search-results'})
  
  if search_results_ul: # this is a searh results page with no entries
    search_results_lis = list(search_results_ul.find_all('li', recursive=False))
    return [domain_name+li.find('a')['href'] for li in search_results_lis]
  else: # this is a searh results page with no entries
    return []


# TODO - should this function be the one requesting another soup? maybe refactor
def get_lexeme_page_soup(form: str, pos: str, language: str) -> BeautifulSoup:
  """
  Given some (potentially) inflected form of a word, find the page which contains the main lexeme entry, its lemma, and its pos

  Returns: (soup, lemma, pos)

  if we aren't given a part of speech, let's collect lemmas for each part of speech - if [lemma]==[form], take that one, and if not, take the first entry we see
  I'm assuming that [get_terms_parts_of_speech] will give me the parts of speech in the order that they're seen under the entries
  """
  term_soup = get_soup_from_url(get_wiktionary_term_url(form))

  # we might need to guess which word we were going for, so 
  if has_entries(term_soup): # this page has wiktionary entries
    potential_lemma_pos_pairs = []

    if not pos: # we don't know what part of speech we're looking for, so let's guess (see docstring)
      poses = get_term_parts_of_speech(term_soup, language)
    else:
      poses = [pos] # TODO this is really bad, fix

    for potential_pos in poses:
      lemma = get_lemma(term_soup, potential_pos, language)
      
      if form == lemma: # early return, because the inflection we initially got is a lemma form
        return (term_soup, lemma, potential_pos)
      else:
        potential_lemma_pos_pairs.append((lemma, potential_pos))
    
    if potential_lemma_pos_pairs: # we've identified the lemma
      lemma, pos = potential_lemma_pos_pairs[0]
      term_soup = get_soup_from_url(get_wiktionary_term_url(lemma))
      return (term_soup, lemma, pos) # TODO what if the lemma is mentioned, but it has no wiktionary entry and the link is dead?
    else: # we didn't find an entry with the form in the part of speech that we specified, so return None
      return None
  else: # this page has no entries, search wiktionary for related terms
    search_soup = get_soup_from_url(get_wiktionary_search_url(form))
    search_result_links = get_search_result_links(search_soup)
     
    for link in search_result_links:
      try:
        # the arg form isn't on this page, so we assume that the arg form pertains to the first pos of the first page describing our language
        lemma = unquote(link.split('/')[-1].replace("_", " ")) # TODO clean this up, I didn't think I'd have to pull the lemma from th link
        term_soup = get_soup_from_url(link)
        probable_pos = get_term_parts_of_speech(term_soup, language)[0]
        return (term_soup, lemma, probable_pos)
      except:
        logging.warning("Failed to find lexeme on this page")
  
  return None # we were never able to find a page that probably describes the lexeme, return None




#%% main
def main():
  soup = get_soup_from_url(get_wiktionary_term_url('czerwony'))
  print(type(soup))

if __name__ == "__main__":
  main()