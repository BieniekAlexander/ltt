# imports
import json
import os
from pymongo.mongo_client import MongoClient
from storage.language_datastores.chinese_datastore import ChineseDatastore
from language.chinese.character import Character
from language.chinese.word import Word
from language.part_of_speech import PartOfSpeech

# read radical data from JSON
hsk1_dict = json.load(open('data/hsk1.json', 'r'))
entries = list(hsk1_dict.values())

datastore_client = MongoClient(os.environ['MONGODB_URI'])
chinese_datastore = ChineseDatastore(datastore_client)

for entry in entries:
    # cleaning entries
    if 'place' in entry['pos']:
        entry['pos'][entry['pos'].index('place')] = 'noun'

    if 'character' in entry:
        entry['lemma'] = entry.pop('character')
        entry['variants'] = []
        entry['stroke_counts']['simplified'] = 1

        # check if the character is already in the datastore, and if not, add it
        if len(chinese_datastore.get_lexemes(lemma=entry['lemma'])) == 0:
            character = Character(**entry)
            chinese_datastore.add_lexemes([character])
        
    elif 'word' in entry:
        entry['characters'] = entry.pop('word')

        # check if the word is already in the datastore, and if not, add it
        if len(chinese_datastore.get_words(characters=entry['characters'])) == 0:
            word = Word(**entry)
            chinese_datastore.add_words([word])