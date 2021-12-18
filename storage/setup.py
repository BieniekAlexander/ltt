#%% imports
import pymongo, logging


# %% connect
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.admin
if db.command("serverStatus"):
  logging.info("Connected to mongodb and got server status")


# %% setup index for polish lexicon
db = client['lexicon']
db['polish'].create_index([("lemma", pymongo.ASCENDING)], name="lemma index")


# %% setup index for user vocabulary
db = client['vocabulary']
db['polish'].create_index([("user", pymongo.ASCENDING), ("lexeme_id", pymongo.ASCENDING)], name="user vocabulary index")