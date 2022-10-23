# imports
import logging
import os

import requests
from pymongo import MongoClient
from scraping.annotation_utils import annotate_text
from scraping.html_parse_utils import get_page_main_content
from storage.language_datastore import LanguageDatastore

# constants
MONGODB_URI = os.environ['MONGODB_URI']
ARTICLE_URLS_PATH = f"{os.getcwd()}/data/polish/articles.txt"

ds_client = MongoClient(MONGODB_URI)
polish_language_datastore = LanguageDatastore(ds_client, "polish")

language = "Polish"
article_urls = open(ARTICLE_URLS_PATH, "r").read().splitlines()


for article_url in article_urls:
    try:
        article_text = get_page_main_content(requests.get(article_url).text)
        annotate_text(article_text, polish_language_datastore, None, True)
        logging.info(f"Finished annotating article - {article_url}")
    except Exception as e:
        logging.error(
            f"Hit a bump while annotating text from {article_url} - {e}")