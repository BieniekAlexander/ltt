#%% imports
import pymongo, logging
from datastore_utils import lexeme_index, user_vocabulary_index, inflections_index


# %% connect
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.admin

if db.command("serverStatus"):
  logging.info("Connected to mongodb and got server status")


# %% setup index for polish lexicon
db = client['polish']
db['lexicon'].drop_indexes()
db['lexicon'].create_index(**lexeme_index)


# %% setup index for user vocabulary
db = client['polish']
db['vocabulary'].drop_indexes()
db['vocabulary'].create_index(**user_vocabulary_index)


# %% setup index for inflections
db = client['polish']
db['inflections'].drop_indexes()
db['inflections'].create_index(**inflections_index)


# %%
