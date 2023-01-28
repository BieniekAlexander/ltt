import os
from random import shuffle
from pymongo import MongoClient
from enforce_typing import enforce_types
from bson.objectid import ObjectId

from training.sm2_anki.stats import STEP_INTERVALS
from storage.language_datastores import LANGUAGE_DATASTORE_MAP

# constants
MONGODB_URI = os.environ['MONGODB_URI']


@enforce_types
def push_study_entry(study_queue: list, entry: dict, fact: str) -> None:
    """
    Puts the study entry back into the queue if it's still in learning mode and the interval is more than 0 days
    """
    step = entry['stats'][fact].step
    interval = STEP_INTERVALS[step]

    if interval == 0:
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
    entries = list(filter(lambda x: not all(x['stats'][fact].suspended for fact in facts), entries)) # filter out terms for which the facts of interest are all suspended

    # sort the fact dictionaries internally, according to whether the fact is being studied, whether it's suspended, and the interval length
    for entry in entries:
        keys = list(entry['stats'].keys())
        keys = sorted(keys, key=lambda k: (k not in facts, entry['stats'][k].suspended, entry['stats'][k].interval))
        entry['stats'] = {k: entry['stats'][k] for k in keys}

    # sort and return the study entries according to the study fact with the lowest interval
    study_entries = sorted(entries, key=lambda x: list(x['stats'].values())[0].interval)[:count]
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
        language_datastore.update_vocabulary_entry(
            lexeme_id=ObjectId(entry['lexeme_id']), stats=entry['stats'], user_id=ObjectId(user_id))
        
if __name__ == "__main__":
    import os

    user_id = ObjectId("62a57d5bfa96028f59ac1d75")
    MONGODB_URI = os.getenv("MONGODB_URI")
    ds_client = MongoClient(MONGODB_URI)
    language = "chinese"

    print(get_study_entries(user_id, language, ds_client, ['spoken_to_definition']))