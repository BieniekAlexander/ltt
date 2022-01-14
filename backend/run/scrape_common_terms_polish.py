'''
This script collects information on the 2000 most common polish words,
collected from this article: https://www.101languages.net/polish/most-common-polish-words/
'''
#%% imports
import sys, os, requests, time, json, re, logging
from bs4 import BeautifulSoup
import pandas as pd

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from backend.scraping.wiktionary_spider import WiktionarySpider
# from backend.storage.datastore_client import DatastoreClient
# from backend.storage.language_datastore import LanguageDatastore
# from backend.scraping.scraping_errors import ScrapingError, ScrapingFindError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scraping.wiktionary_spider import WiktionarySpider
from scraping.scraping_errors import ScrapingError, ScrapingFindError
from storage.datastore_client import DatastoreClient
from storage.language_datastore import LanguageDatastore
from model.model_errors import ModelError


MONGODB_URL = "mongodb://localhost:27017/"
PATH_TO_CSV = "/home/alex/projects/ltt/backend/run/data/polish/2k.csv"

# try:
#   raise ScrapingFindError(None, {}, 'wow')
# except ScrapingError as e:
#   print(e)
# exit()

# %% setup
# set up mongodb connection
language = "polish"
polish_terms_df = pd.read_csv(PATH_TO_CSV)
polish_terms = list(polish_terms_df['Polish'])

ds_client = DatastoreClient(MONGODB_URL)
language_datastore = LanguageDatastore(ds_client, language)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# %% helper functions
def get_error_summary(term: str, exception: Exception, spider: WiktionarySpider, num_urls: int = 3) -> str:
    # TODO this is a start - find a better way to get the term and pos relevant to the error
    assert num_urls > 0

    urls_to_show = spider.steps[-num_urls:]
    url_str = '\n'.join(urls_to_show)

    return ("Error Summary\n"
    f"term: {term}\n"
    f"query: {exception.query_args}\n" if issubclass(type(exception), ScrapingError) else ""
    f"exception: {type(exception).__name__}\n"
    f"message: {exception}\n"
    "urls:\n"
    f"{url_str}")


# %%
for term in polish_terms:  
  term = term.lower() # lowercase the term for reading from database and scraping from wiktionary - TODO what to do about proper nouns?
  potential_lexeme_dictionary_mappings = language_datastore.get_lexemes_from_form(form=term.lower())

  # get lexeme from lexicon
  if potential_lexeme_dictionary_mappings:
    entry = potential_lexeme_dictionary_mappings[0]
    lemma = entry['lemma']
    logger.debug(f"Found lemma {lemma} in datastore (found using term {term})")
  else:
    try:
      spider = WiktionarySpider()
      lexemes = spider.query_lexemes(term, language)

      for lexeme in lexemes:
        lexeme_id = language_datastore.add_lexeme(lexeme)
        logger.info(f"Saved {lexeme.lemma, lexeme.pos.value} to datastore (found using term {term})")
    except Exception as e:
      logger.error(f"Tried & failed to scrape the term {term} - {type(e).__name__}: {e}")

      with open(f'logs/2k/{term}.log', 'w') as f:
        f.write(get_error_summary(term, e, spider, 3))
