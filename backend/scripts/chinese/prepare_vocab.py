'''
Initialize a user's vocabulary with the set of terms from duolingo's wordbase
'''
import logging
import argparse
import os

from pymongo import MongoClient
from bson.objectid import ObjectId
from storage.language_datastores.chinese_datastore import ChineseDatastore
from training.sm2_anki.stats import Stats

# constants
MONGODB_URI = os.environ['MONGODB_URI']
language = "chinese"

# parse runtime args from command line
parser = argparse.ArgumentParser(description="Initialize a user's chinese vocabulary with radicals")
parser.add_argument('--user_id', type=str, required=True, help='The user to add the vocab to')
args = parser.parse_args()

user_id = args.user_id

ds_client = MongoClient(MONGODB_URI)
chinese_datastore = ChineseDatastore(ds_client)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# loop over the terms, find them in the lexicon, and add them to the user's vocab
radicals = list(chinese_datastore.get_lexemes(is_radical=True))

for radical in radicals:
    stats = {'written': Stats().to_json()}
    chinese_datastore.add_vocabulary_entries([dict(character_id=radical['_id'], user_id=ObjectId(user_id), stats=stats)])