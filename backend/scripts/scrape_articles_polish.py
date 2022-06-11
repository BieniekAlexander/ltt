#%% imports
import sys, os, requests, time, json, re, logging
from bs4 import BeautifulSoup


from scraping.annotation_utils import annotate_text
from scraping.html_parse_utils import get_page_main_content
from storage.language_datastore import LanguageDatastore
from language.lexeme import LexemeEncoder

MONGODB_URL = "mongodb://localhost:27017/"
PATH_TO_ARTCLE_URL_FILE = 'run/data/polish/articles.txt'


# %% setup
# set up mongodb connection 
polish_language_datastore = LanguageDatastore(MONGODB_URL, "polish")


language = "Polish"
article_urls = open(PATH_TO_ARTCLE_URL_FILE, "r").read().splitlines() 


# %%
for article_url in article_urls:
  try:
    article_text = get_page_main_content(requests.get(article_url).text)
    annotate_text(article_text, polish_language_datastore, None, True)
    logging.info(f"Finished annotating article - {article_url}")
  except Exception as e:
    logging.error(f"Hit a bump while annotating text from {article_url} - {e}")

# %%