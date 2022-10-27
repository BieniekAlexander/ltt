# %% imports
import pandas as pd
import logging
import os

from pymongo import MongoClient
from scraping.annotation_utils import annotate_text
from storage.language_datastore import LanguageDatastore

MONGODB_URI = os.environ['MONGODB_URI']
DUOLINGO_CSV = f"{os.getcwd()}/data/polish/duolingo_vocab.csv"

# set up mongodb connection, get string of text from duolingo dump
ds_client = MongoClient(MONGODB_URI)
polish_language_datastore = LanguageDatastore(ds_client, "polish")
duolingo_string = ' '.join(list(pd.read_csv(DUOLINGO_CSV, comment="#")['Polish']))

# use annotation discovery mode to collect terms
try:
    annotate_text(duolingo_string, polish_language_datastore, None, True)
except Exception as e:
    logging.error(
        f"Error discovering duolingo dump term - {e}")
