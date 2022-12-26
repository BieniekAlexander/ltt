'''
Initialize a user's vocabulary with the set of terms from duolingo's wordbase
'''
import logging
import argparse
import os
import pandas as pd

from bson.objectid import ObjectId
from pymongo import MongoClient
from storage.language_datastores.polish_datastore import PolishDatastore
from training.sm2_anki.stats import Stats

# constants
MONGODB_URI = os.environ['MONGODB_URI']
DUOLINGO_CSV = f"{os.getcwd()}/data/polish/duolingo_vocab.csv"
language = "polish"

# parse runtime args from command line
parser = argparse.ArgumentParser(description="Initialize a user's vocabulary with the set of terms from duolingo's wordbase")
parser.add_argument('--user_id', type=str, required=True, help='The user to add the vocab to')
args = parser.parse_args()

# 
user_id = args.user_id
duolingo_terms_polish = list(pd.read_csv(DUOLINGO_CSV, comment="#")['Polish'])

ds_client = MongoClient(MONGODB_URI)
language_datastore = PolishDatastore(ds_client, language)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# loop over the terms, find them in the lexicon, and add them to the user's vocab
for term in duolingo_terms_polish:
    term = term.lower()
    potential_lexeme_dictionary_mappings = language_datastore.get_lexemes_from_form(
        form=term.lower())

    # get lexeme from lexicon
    if potential_lexeme_dictionary_mappings:
        lexeme_ids = [entry['_id']
                      for entry in potential_lexeme_dictionary_mappings]

        for lexeme_id in lexeme_ids:
            try:
                language_datastore.add_vocabulary_entry(
                    ObjectId(lexeme_id), {'definition': Stats()}, ObjectId(user_id))
            except Exception as e:  # eee storage exceptions
                # TODO I'm not seeing this get logged, I'm not sure why
                logger.info("Skipping duplicate vocabulary entry")
    else:
        logger.error(f"Cound not find any lexemes for the term {term}")


