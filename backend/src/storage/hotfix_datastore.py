# A script that I'll use to update data in my datastore when I change my schema
import json
import os
from copy import deepcopy

from pymongo import MongoClient
from storage.language_datastore import LanguageDatastore
from training.sm2.stats import Stats

MONGODB_URI = os.environ['MONGODB_URI']
language = "polish"


datastore_client = MongoClient(MONGODB_URI)
language_datastore = LanguageDatastore(datastore_client, language)

q = {"stats.interval": 0}
terms = list(language_datastore.vocabulary_connector.collection.find(q))
backup_terms = deepcopy(terms)
print(terms)

for term in backup_terms:
    for item in term:
        term[item] = str(term[item])

json.dump(backup_terms, open("hotfix_backup.json", "w"))

for term in terms:
    term['stats'] = Stats().to_json()

language_datastore.vocabulary_connector.collection.delete_many(q)
language_datastore.vocabulary_connector.collection.insert_many(terms)
