# imports
import os
import argparse
from typing import Optional
from bson.objectid import ObjectId
from enforce_typing import enforce_types

from language.chinese.word import Word
from language.chinese.character import Character
from training.sm2_anki.stats import Stats
from scraping.canto_dict.canto_dict_client import get_fact_from_characters
from pymongo.mongo_client import MongoClient
from storage.language_datastores.chinese_datastore import ChineseDatastore


@enforce_types
def main(path_to_data: str, dry_run: bool = False, user_id: Optional[ObjectId] = None, vocabulary_set: Optional[str] = None) -> None:
    # read entries from file
    words_list = open(path_to_data, 'r').read().split('\n')
    datastore_client = MongoClient(os.environ['MONGODB_URI'])
    chinese_datastore = ChineseDatastore(datastore_client)

    for word in words_list:
        entry = get_fact_from_characters(word)
        entry_ids = []

        if 'character' in entry:
            entry['stroke_counts']['simplified'] = 1
            entry['lemma'] = entry.pop('character')
            entry['variants'] = []
            entry_object = Character(**entry)
        elif 'word' in entry:
            entry['lemma'] = entry.pop('word')
            entry_object = Word(**entry)
            
        print(entry_object)

        if dry_run:
            continue
        else:
            # check if the lemma is already in the datastore, and if not, add it
            lexemes_dict = chinese_datastore.get_lexemes(lemma=entry['lemma'])

            if len(lexemes_dict) == 0:
                ids = chinese_datastore.add_lexemes([entry_object])
            else:
                ids = lexemes_dict.keys()

            entry_ids.append(ids[0])

            if user_id!=None and vocabulary_set!=None:
                vocabulary_entries = [
                        {'lexeme_id': id, 'user_id': user_id, 'stats': {'written': Stats().to_json()}}
                        for id in entry_ids
                    ]
                    
                chinese_datastore.add_vocabulary_entries(entries=vocabulary_entries)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load chinese text from a file to upload to the datastore', add_help=False)
    parser.add_argument('--path-to-data', dest='path_to_data', required=True,
                        help='The path to the file of lines with Chinese words to scrape')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true', help='use to perform dry run of uploading to datastore')
    parser.set_defaults(feature=False)
    parser.add_argument('--user-id', dest='user_id', required=False, default=None,
                        help="User ID to whom we will add the vocabulary terms")
    parser.add_argument('--vocabulary-set', dest='vocabulary_set', required=False,
                        help="User ID to whom we will add the vocabulary terms")
    
    
    args = parser.parse_args()

    main(
        path_to_data=args.path_to_data,
        user_id=ObjectId(args.user_id),
        dry_run=args.dry_run,
        vocabulary_set=args.vocabulary_set)
