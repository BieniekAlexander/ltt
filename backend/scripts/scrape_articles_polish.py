# %% imports
import sys
import os
import requests
import time
import json
import re
import logging
from bs4 import BeautifulSoup

from scraping.annotation_utils import annotate_text
from scraping.html_parse_utils import get_page_main_content
from storage.language_datastore import LanguageDatastore

MONGODB_URI = os.environ['MONGODB_URI']
PATH_TO_ARTCLE_URL_FILE = 'run/data/polish/articles.txt'


# %% setup
# set up mongodb connection
polish_language_datastore = LanguageDatastore(MONGODB_URI, "polish")

language = "Polish"
article_urls = open(PATH_TO_ARTCLE_URL_FILE, "r").read().splitlines()


# %%
for article_url in article_urls:
    try:
        article_text = get_page_main_content(requests.get(article_url).text)
        annotate_text(article_text, polish_language_datastore, None, True)
        logging.info(f"Finished annotating article - {article_url}")
    except Exception as e:
        logging.error(
            f"Hit a bump while annotating text from {article_url} - {e}")

# %%
