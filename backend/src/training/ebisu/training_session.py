import os
from random import shuffle
from pymongo import MongoClient
from enforce_typing import enforce_types
from bson.objectid import ObjectId
from storage.language_datastores import LANGUAGE_DATASTORE_MAP
import ebisu
from datetime import datetime

# constants
MONGODB_URI = os.environ['MONGODB_URI']


@enforce_types
def push_study_entry(study_queue: list, entry: dict, fact: str) -> None:
    """
    Puts the study entry back into the queue if the specified fact was recalled with a score below .5
    """
    if entry['stats'][fact].score < .5:
        study_queue.append(entry)


@enforce_types
def get_study_entries(user_id: ObjectId, language: str, datastore_client: MongoClient, facts: list[str], interval: int = 1, count: int = 50) -> list:
    """
    Collects the vocabulary being used by the user in the training session
    """
    # init DAOs, get vocabulary entries
    # TODO request crashes when fact is not present in language vocabulary, fix - e..g. spoken_to_definition used for polish
    language_datastore_class = LANGUAGE_DATASTORE_MAP[language.lower()]
    language_datastore = language_datastore_class(datastore_client)
    entries = language_datastore.get_vocabulary_entries(lexeme_id=[], user_id=user_id)
    entries = list(filter(lambda x: len(set(facts) & set(x['stats'].keys()))>0, entries)) # filter out terms without the fact of interest
    entries = list(filter(lambda x: not all(fact in x['stats'] and x['stats'][fact].suspended for fact in facts), entries)) # filter out terms for which the facts of interest are all suspended

    # sort the fact dictionaries internally, according to whether the fact is being studied, whether it's suspended, and the Ebisu recall probability
    dt_now_in_seconds = datetime.now().timestamp()

    for entry in entries:
        keys = list(entry['stats'].keys())
        keys = sorted(keys, 
        key = lambda k: (
            k not in facts,
            entry['stats'][k].suspended,
            ebisu.predictRecall(entry['stats'][k].get_prior(),
            dt_now_in_seconds - entry['stats'][k].last_study_time)
        ))

        entry['stats'] = {k: entry['stats'][k] for k in keys}

    # sort and return the study entries according to the study fact with the lowest interval
    study_entries = sorted(
        entries, 
        key=lambda x: ebisu.predictRecall(list(x['stats'].values())[0].get_prior(), dt_now_in_seconds - list(x['stats'].values())[0].last_study_time))[:count] # TODO computing recall twice, slghtly ineffecient
    shuffle(study_entries)
    return study_entries


@enforce_types
def put_studied_entries(user_id: str, language: str, datastore_client: MongoClient, studied_entries: list[dict]):
    """
    Updates and pushes a studied set of vocabulary entries to the database 
    """
    # init DAOs
    language_datastore_class = LANGUAGE_DATASTORE_MAP[language.lower()]
    language_datastore = language_datastore_class(datastore_client)

    # get the entries and the user's vocab entries
    for entry in studied_entries:
        if len(entry['stats']) > 0:
            language_datastore.update_vocabulary_entry(
                lexeme_id=ObjectId(entry['lexeme_id']), stats=entry['stats'], user_id=ObjectId(user_id))
        else:
            language_datastore.delete_vocabulary_entry(ObjectId(entry['vocabulary_id']))
            
if __name__ == "__main__":
    import os

    user_id = ObjectId("62a57d5bfa96028f59ac1d75")
    MONGODB_URI = os.getenv("MONGODB_URI")
    ds_client = MongoClient(MONGODB_URI)
    language = "chinese"

    print(get_study_entries(user_id, language, ds_client, ['spoken_to_definition']))