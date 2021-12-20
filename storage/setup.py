#%% imports
import pymongo, logging
from storage.datastore_utils import lexeme_index, user_vocabulary_index, inflections_index


# %% connect
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.admin

if db.command("serverStatus"):
  logging.info("Connected to mongodb and got server status")


# %% setup index for polish lexicon
db = client['lexicon']
db['polish'].drop_indexes()
db['polish'].create_index(lexeme_index)


# %% setup index for user vocabulary
db = client['vocabulary']
db['polish'].drop_indexes()
db['polish'].create_index(user_vocabulary_index)


# %% setup index for inflections
db = client['inflections']
db['polish'].drop_indexes()
db['polish'].create_index(inflections_index)


# %%
