import argparse
import os

from configure_datastore_auth import configure_mongodb_auth
from configure_datastore_language import configure_mongodb_language


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Initialize all of the mongodb configurations for the application')
    parser.add_argument('--mongodb-uri', dest='mongodb_uri', required=True,
                        help='URI used to connect to MongoDB')
    parser.add_argument('--languages', dest='languages', required=False, default="polish",
                        help='The language for which we instantiate datastore schemata')

    args = parser.parse_args()

    configure_mongodb_auth(args.mongodb_uri)

    for language in args.languages.split(','):
        configure_mongodb_language(args.mongodb_uri, language)