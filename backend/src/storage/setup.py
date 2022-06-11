#%% imports
import pymongo
import argparse

from storage.datastore_schemata.polish_schemata import \
  lexeme_index, lexeme_schema, \
  user_vocabulary_index, user_vocabulary_schema, \
  inflections_index, inflections_schema


def setup_mongodb(mongodb_uri: str, language: str):
  # %% connect
  client = pymongo.MongoClient(mongodb_uri)
  
  db = client[language.lower()]
  db['lexicon'].drop_indexes()
  db['lexicon'].create_index(**lexeme_index)
  db.command({
   "collMod": "lexicon",
   "validator": lexeme_schema,
   "validationLevel": "strict"
  })

  db = client[language.lower()]
  db['vocabulary'].drop_indexes()
  db['vocabulary'].create_index(**user_vocabulary_index)
  db.command({
   "collMod": "vocabulary",
   "validator": user_vocabulary_schema,
   "validationLevel": "strict"
  })

  db = client[language.lower()]
  db['inflections'].drop_indexes()
  db['inflections'].create_index(**inflections_index)
  db.command({
   "collMod": "inflections",
   "validator": inflections_schema,
   "validationLevel": "strict"
  })


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Initialize the indices and schemata of a language database in mongodb')
  parser.add_argument('--mongodb-uri', dest='mongodb_uri', default="mongodb://localhost:27017/", required=False,
      help='URI used to connect to MongoDB')
  parser.add_argument('--language', dest='language', required=False, default="polish", help='language schemata and indices being updated')
  # TODO language arg

  args = parser.parse_args()
  setup_mongodb(args.mongodb_uri, args.language)