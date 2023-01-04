import os
from random import shuffle
from pymongo import MongoClient
from bson.objectid import ObjectId

from training.sm2_anki.stats import STEP_INTERVALS
from storage.language_datastores import LANGUAGE_DATASTORE_MAP

# constants
MONGODB_URI = os.environ['MONGODB_URI']


def push_study_entry(study_queue: list, entry: dict, fact: str) -> None:
    """
    Puts the study entry back into the queue if it's still in learning mode and the interval is more than 0 days
    """
    step = entry['stats'][fact].step
    interval = STEP_INTERVALS[step]

    if interval == 0:
        study_queue.append(entry)


def get_study_entries(user_id: ObjectId, language: str, datastore_client: MongoClient, fact: str, interval: int = 1, count: int = 50) -> list:
    """
    Collects the vocabulary being used by the user in the training session
    TODO this isn't technically true to the sm2 implementation, because sm2 will just give you the terms each day according to the interval
    """
    # init DAOs
    language_datastore_class = LANGUAGE_DATASTORE_MAP[language.lower()]
    language_datastore = language_datastore_class(datastore_client)
    entries = language_datastore.get_vocabulary_entries(lexeme_id=[], user_id=user_id)
    entries = list(filter(lambda x: fact in x['stats'], entries))
    study_entries = sorted(entries, key=lambda x: x['stats'][fact].interval)[:count]
    shuffle(study_entries)
    return study_entries


def put_studied_entries(user_id: str, language: str, datastore_client: MongoClient, fact: str, studied_entries: list[dict]):
    """
    Updates and pushes a studied set of vocabulary entries to the database 
    """
    # init DAOs
    language_datastore_class = LANGUAGE_DATASTORE_MAP[language.lower()]
    language_datastore = language_datastore_class(datastore_client)

    # get the entries and the user's vocab entries
    for entry in studied_entries:
        if entry['stats'][fact].recall is not None:
            language_datastore.update_vocabulary_entry(
                lexeme_id=ObjectId(entry['lexeme_id']), stats=entry['stats'], user_id=ObjectId(user_id))
        else:
            print('bounce')

if __name__ == "__main__":
    import os

    user_id = ObjectId("62a57d5bfa96028f59ac1d75")
    MONGODB_URI = os.getenv("MONGODB_URI")
    ds_client = MongoClient(MONGODB_URI)
    language = "chinese"

    print(get_study_entries(user_id, language, ds_client, 'spoken'))