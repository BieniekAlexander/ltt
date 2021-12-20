#%% imports
import requests, os, sys
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.function_decorators import delay


#%% utils 
get_wiktionary_term_url = lambda term: f"https://en.wiktionary.org/wiki/{term}"
get_wiktionary_search_url = lambda term: f"https://en.wiktionary.org/w/index.php?search={term}"


@delay(5)
def get_soup_from_url(url: str):
  """
  Helper function to get the [BeautifulSoup] object from a URL 
  """
  # TODO add checks in here
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")
  return soup