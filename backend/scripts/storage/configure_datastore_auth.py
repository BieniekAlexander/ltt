import argparse

import pymongo

from storage.datastore_schemata.auth_schemata import (auth_schema)


def configure_mongodb_auth(mongodb_uri: str):
    """
    Connect to the specified MongoDB instance and instantiate the auth schemata
    """
    client = pymongo.MongoClient(mongodb_uri)

    db = client['auth']
    db['lexicon'].drop_indexes()
    db.command({
        'collMod': 'users',
        'validator': auth_schema,
        'validationLevel': 'strict'
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Initialize the schema for Auth in MongoDB')
    parser.add_argument('--mongodb-uri', dest='mongodb_uri', required=True,
                        help='URI used to connect to MongoDB')
    parser.add_argument('--languages', dest='languages', default="polish", required=True,
                        help='A CSV string listing the languages for which we want to instantiate schemata')

    args = parser.parse_args()
    configure_mongodb_auth(args.mongodb_uri)
