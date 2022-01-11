'''
This script collects information on the 2000 most common polish words,
collected from this article: https://www.101languages.net/polish/most-common-polish-words/
'''
#%% imports
import sys, os, requests, time, json, re, logging
from bs4 import BeautifulSoup
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.scraping.wiktionary_scrape_summary_utils import wiktionary_get_all_lang_pos_lemmas
from backend.scraping.wiktionary_extract_lexeme_utils import extract_lexeme
from backend.scraping.wiktionary_crawl_utils import get_lexeme_page_soup
from backend.storage.datastore_client import DatastoreClient
from backend.storage.language_datastore import LanguageDatastore
from backend.model.lexeme import LexemeEncoder


MONGODB_URL = "mongodb://localhost:27017/"
PATH_TO_CSV = "/home/alex/projects/ltt/run/data/polish/2k.csv"


# %% setup
# set up mongodb connection
language = "polish"
polish_terms_df = pd.read_csv(PATH_TO_CSV)
polish_terms = list(polish_terms_df['Polish'])

ds_client = DatastoreClient(MONGODB_URL)
language_datastore = LanguageDatastore(ds_client, language)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
      term_soup, lemma, pos = get_lexeme_page_soup(term, None, language)
      lexeme = extract_lexeme(term_soup, lemma, pos, language)
      lexeme_id = language_datastore.add_lexeme(lexeme)
      logger.info(f"Saved lemma {lemma} to datastore (found using term {term})")
    except Exception as e:
      logger.error(f"Tried & failed to scrape the term {term} - {type(e).__name__}: {e}")
