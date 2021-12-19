#%% imports
import pymongo, logging


# %% connect
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.admin

if db.command("serverStatus"):
  logging.info("Connected to mongodb and got server status")


# %% setup index for polish lexicon
db = client['lexicon']
db['polish'].create_index([("lemma", pymongo.ASCENDING), ("pos", pymongo.ASCENDING)], name="lemma index", unique=True)


# %% setup index for user vocabulary
db = client['lexicon']
db['polish'].create_index([("user", pymongo.ASCENDING), ("lexeme_id", pymongo.ASCENDING)], name="user vocabulary index", unique=True)


# %% get some contents of the vocabulary
db = client['lexicon']
results = list(db['polish'].find({}))


# %%
