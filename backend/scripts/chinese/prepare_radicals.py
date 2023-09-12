 # imports
import json
import os
from pymongo.mongo_client import MongoClient
from storage.language_datastores.chinese_datastore import ChineseDatastore
from language.chinese.character import Character
from language.part_of_speech import PartOfSpeech

# read radical data from JSON
radical_dict = json.load(open('data/radicals.json', 'r'))
radicals = list(radical_dict.values())

datastore_client = MongoClient(os.environ['MONGODB_URI'])
chinese_datastore = ChineseDatastore(datastore_client)

for radical in radicals: radical['pos'] = [PartOfSpeech.NOUN]
characters = [Character(**radical) for radical in radicals]
chinese_datastore.add_lexemes(entries=characters)