import os

from pymongo import MongoClient
from storage.language_datastore import LanguageDatastore
from storage.lexicon_connector import LexiconConnector
from training.sm2_anki.stats import STEP_INTERVALS

# constants
MONGODB_URI = os.environ['MONGODB_URI']


def push_study_entry(study_queue: list, entry: dict) -> None:
    """
    Puts the study entry back into the queue if it's still in learning mode and the interval is more than 0 days
    """
    step = entry['stats']['definition'].step
    interval = STEP_INTERVALS[step]

    if interval == 0:
        study_queue.append(entry)


def get_study_entries(user_id: str, language: str, datastore_client: MongoClient, interval: int = 1, count: int = 50):
    """
    Collects the vocabulary being used by the user in the training session
    TODO this isn't technically true to the sm2 implementation, because sm2 will just give you the terms each day according to the interval
    """
    # init DAOs
    language_datastore = LanguageDatastore(datastore_client, language)
    lexicon_connector = LexiconConnector(datastore_client, language)

    # get the entries and the user's vocab entries
    vocabulary = sorted(language_datastore.get_vocabulary_entries(
        lexeme_ids=[], user_id=user_id), key=lambda x: x['lexeme_id'])
    lexeme_ids = list(map(lambda x: x['lexeme_id'], vocabulary))
    lexemes = sorted(lexicon_connector.get_lexeme_entries(
        _ids=lexeme_ids), key=lambda x: x['_id'])
    study_entries = []

    # join the entries and vocab entries on the id
    for v, l in zip(vocabulary, lexemes):
        assert str(v['lexeme_id']) == str(
            l['_id']), f"'{v['lexeme_id']}' != '{l['_id']}'"

        vocab = {
            'lexeme_id': (v['lexeme_id']),
            "vocab_id": str(l['_id']),
            "lexeme": l,
            "stats": v['stats']
        }

        study_entries.append(vocab)

    study_entries = sorted(study_entries, key=lambda x: x['stats']['definition'].interval)
    return study_entries[:count]


def put_studied_entries(user_id: str, language: str, datastore_client: MongoClient, studied_entries: list):
    """
    Updates and pushes a studied set of vocabulary entries to the database 
    """
    # init DAOs
    language_datastore = LanguageDatastore(datastore_client, language)

    # get the entries and the user's vocab entries
    for entry in studied_entries:
        if entry['stats']['definition'].recall is not None:
            language_datastore.update_vocabulary_entry(
                lexeme_id=entry['lexeme_id'], stats=entry['stats'], user_id=user_id)
        else:
            print('bounce')
