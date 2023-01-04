import argparse
import pymongo

from storage.datastore_schemata.chinese_schemata import (
    character_index as zh_character_index,
    character_schema as zh_character_schema,
    word_index as zh_word_index,
    word_schema as zh_word_schema,
    vocabulary_index as zh_vocabulary_index,
    vocabulary_schema as zh_vocabulary_schema)
    # TODO maybe but these configurations in some sort of object and load them in with an abstraction

from storage.datastore_schemata.polish_schemata import (
    inflections_index as pl_inflections_index,
    inflections_schema as pl_inflections_schema,
    lexeme_index as pl_lexeme_index,
    lexeme_schema as pl_lexeme_schema,
    vocabulary_index as pl_vocabulary_index,
    vocabulary_schema as pl_vocabulary_schema)


def configure_mongodb_language(mongodb_uri: str, language: str):
    """
    Connect to the specified MongoDB instance and instantiate the schemata for the given language
    """
    client = pymongo.MongoClient(mongodb_uri)
 
    #################
    #    POLISH     #
    #################
    if language.lower() in ['pl', 'polish']:
        db = client["polish"]

        db['lexicon'].drop_indexes() # TODO update the name of the collection to just "lexemes"
        db['lexicon'].create_index(**pl_lexeme_index)
        if 'lexicon' not in db.list_collection_names():
            db.create_collection('lexicon')
        db.command({
            "collMod": "lexicon",
            "validator": pl_lexeme_schema,
            "validationLevel": "strict"
        })

        db['vocabulary'].drop_indexes()
        db['vocabulary'].create_index(**pl_vocabulary_index)
        if 'vocabulary' not in db.list_collection_names():
            db.create_collection('vocabulary') 
        db.command({
            "collMod": "vocabulary",
            "validator": pl_vocabulary_schema,
            "validationLevel": "strict"
        })

        db['inflections'].drop_indexes() # TODO remove inflections column, add list field to lexemes
        db['inflections'].create_index(**pl_inflections_index)
        if 'inflections' not in db.list_collection_names():
            db.create_collection('inflections')
        db.command({
            "collMod": "inflections",
            "validator": pl_inflections_schema,
            "validationLevel": "strict"
        })

    ##################
    #    CHINESE     #
    ##################
    elif language.lower() in ['zh', 'chinese']:
        db = client["chinese"]
        db['lexicon'].drop_indexes()
        db['lexicon'].create_index(**zh_character_index)
        if 'lexicon' not in db.list_collection_names():
            db.create_collection('lexicon')
        db.command({
            "collMod": "lexicon",
            "validator": zh_character_schema,
            "validationLevel": "strict"
        })

        db['vocabulary'].drop_indexes()
        db['vocabulary'].create_index(**zh_vocabulary_index)
        if 'vocabulary' not in db.list_collection_names():
            db.create_collection('vocabulary')
        db.command({
            "collMod": "vocabulary",
            "validator": zh_vocabulary_schema,
            "validationLevel": "strict"
        })

    else:
        raise ValueError(f"Unconfigured language: {language}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Initialize the indices and schemata of a language database in MongoDB')
    parser.add_argument('--mongodb-uri', dest='mongodb_uri', required=True,
                        help='URI used to connect to MongoDB')
    parser.add_argument('--language', dest='language', required=True,
                        help='The language for which we instantiate datastore schemata')

    args = parser.parse_args()
    configure_mongodb_language(args.mongodb_uri, args.language)