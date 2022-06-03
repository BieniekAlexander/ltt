'''
This script initializes a user's vocabulary with the set of terms from duolingo's wordbase
'''
#%% imports
import sys, os, logging
import pandas as pd


from storage.datastore_client import DatastoreClient
from storage.language_datastore import LanguageDatastore
from training.stats import Stats

MONGODB_URL = "mongodb://localhost:27017/"
PATH_TO_CSV = "/home/alex/projects/ltt/backend/run/data/polish/duolingo_vocab.csv"


# %% setup
# set up mongodb connection
language = "polish"
polish_terms_df = pd.read_csv(PATH_TO_CSV)
polish_terms = list(polish_terms_df['Polish'])
USER_ID = "a"*24

ds_client = DatastoreClient(MONGODB_URL)
language_datastore = LanguageDatastore(ds_client, language)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# %%
for term in polish_terms:  
  term = term.lower()
  potential_lexeme_dictionary_mappings = language_datastore.get_lexemes_from_form(form=term.lower())
  
  # get lexeme from lexicon
  if potential_lexeme_dictionary_mappings:
    lexeme_ids = [entry['_id'] for entry in potential_lexeme_dictionary_mappings]
    
    for lexeme_id in lexeme_ids:
      try:
        language_datastore.add_vocabulary_entry(lexeme_id, Stats(rating=1.0), USER_ID)
      except Exception as e: # eee storage exceptions
        logger.info("Skipping duplicate vocabulary entry")
  else:
    logger.error(f"Cound not find any lexemes for the term {term}")
