# %% imports
from typing import Union
from bson.objectid import ObjectId
from pymongo import MongoClient

from language.lexeme import Lexeme
from training.sm2_anki.stats import Stats
from utils.data_structure_utils import get_nested_iterable_values
from storage.datastore_utils import generate_member_query, generate_query
from storage.collection_connector import CollectionConnector
from storage.datastore_schemata.polish_schemata import (
    vocabulary_schema,
    lexeme_schema)


# TODO currently manually getting BSON to get this going, but I should add deserialization support
def get_lexeme_bson(lexeme: Lexeme):
    result = lexeme.to_json()

    if 'inflections' in result:
        result['inflections_list'] = list(get_nested_iterable_values(result['inflections']))

    return result

# %% Implementation
class PolishDatastore:
    """
    A datastore interface for polish language data
    """

    def __init__(self, datastore_client: MongoClient):
        """ A connector that handles interaction with a language, as it exists in the datastore

        Args:
            datastore_client (MongoClient): the MongoDB client used to interact with the datastore
            language (str): the language that we're dealing with
        """
        self.language = "polish"
        self.lexicon_connector = CollectionConnector(datastore_client, self.language, "lexicon", lexeme_schema["$jsonSchema"])
        self.vocabulary_connector = CollectionConnector(datastore_client, self.language, "vocabulary", vocabulary_schema["$jsonSchema"])

    def add_lexeme(self, lexeme: Lexeme) -> ObjectId:
        """
        Add a lexeme to the datastore, add related data (i.e. inflection mappings), and get the lexeme_id
        """
        assert isinstance(lexeme, Lexeme)

        lexeme_bson = get_lexeme_bson(lexeme)
        return self.lexicon_connector.push_document(lexeme_bson)

    def add_lexemes(self, lexemes: list[Lexeme]) -> list[ObjectId]:
        """
        Add a lexeme to the datastore, add related data (i.e. inflection mappings), and get the lexeme_id
        """
        assert isinstance(lexemes, list) and all(
            isinstance(lexeme, Lexeme) for lexeme in lexemes)

        lexeme_bsons = [get_lexeme_bson(lexeme) for lexeme in lexemes]
        return self.lexicon_connector.push_documents(lexeme_bsons)

    def delete_lexeme(self, _id: ObjectId):
        """
        remove a lexeme from the language datastore by [_id]

        TODO is this even necessary?
        """
        raise NotImplementedError(
            "Not implementing language lexeme deletion - do I need this?")

    def get_lexeme(self, **kwargs) -> Lexeme:
        lexemes = self.get_lexemes(**kwargs)

        if len(lexemes) == 0:
            return None
        elif len(lexemes) == 1:
            return lexemes[0]
        else:
            raise Exception("found more than one lexeme for this condition")

    def get_lexemes(self, **kwargs) -> list[Lexeme]:
        lexeme_bsons = self.lexicon_connector.get_documents(generate_query(**kwargs))

        for lexeme_bson in lexeme_bsons:
            lexeme_bson.pop('inflections_list', None)

        return [Lexeme(**lexeme_bson) for lexeme_bson in lexeme_bsons]

    def get_lexeme_from_form(self, form: str, pos: str):
        """
        Get a lexeme, given the form form and pos

        This function will return one entry if it exists, [None] if none are found, or raise an exception if multiple are found
        """
        lexemes = self.get_lexemes_from_form(form=form, pos=pos)

        if len(lexemes) == 1:
            return lexemes[0]
        elif len(lexemes) == 0:
            return None
        else:
            raise Exception(f"Found more than one lexeme for form={form}, pos={pos}")

    def get_lexemes_from_form(self, form: str, pos: Union[list, str] = []) -> dict:
        """
        Get the lexemes of [form] in the specified [poses]

        This function will return one entry if it exists, [None] if none are found, or raise an exception if multiple are found
        """
        assert isinstance(form, str) or isinstance(form, list)

        inflections_list_query = generate_member_query('inflections_list', form)
        pos_query = generate_query(pos=pos)
        query = {**inflections_list_query, **pos_query}
        return self.lexicon_connector.get_documents(query)

    def get_vocabulary_entry(self, lexeme_id: ObjectId, user_id: ObjectId) -> dict:
        """
        TODO
        """
        query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
        return self.vocabulary_connector.get_document(query)

    def get_vocabulary_entries(self, lexeme_ids: list, user_id: ObjectId) -> dict:
        """
        TODO
        """
        assert isinstance(user_id, str)
        return self.vocabulary_connector.get_documents(generate_query(lexeme_id=lexeme_ids, user_id=user_id))

    def add_vocabulary_entry(self, lexeme_id: ObjectId, stats: dict, user_id: ObjectId) -> str:
        """
        Add a [lexeme_id], [stats] entry to the vocabulary for [user_id]

        Args:
          lexeme_id
          stats
          user_id
        """
        stats = {key: stats[key].to_json() for key in stats}
        document = dict(lexeme_id=lexeme_id, stats=stats, user_id=user_id)
        self.vocabulary_connector.push_document(document)

    def add_vocabulary_entries(self, entries: list[dict]) -> list:
        """
        Add a list of vocabulary [entries] to the vocabulary for [user_id]

        Args:
          entries: a [list] of [dict]s containing a lexeme_id and stats
        """
        for entry in entries:
            assert set(['lexeme_id', 'stats', 'user_id']) == entry.keys()

        assert len(set(entry['user_id'] for entry in entries)) == 1

        return self.vocabulary_connector.push_documents(entries)

    def update_vocabulary_entry(self, lexeme_id: ObjectId, stats: dict[str, Stats], user_id: ObjectId) -> None:
        """Update the vocabulary entry for [lexeme_id] under [user_id] with the given stats

        Args:
          lexeme_id (str): the identifier of the lexeme to be added to the vocabulary
          stats (str): the initial SRS stats of the vocabulary term for the user
          user_id (str): the identifier for the user that should receive the new vocabulary entry

        Returns:
            str: _description_
        """
        query = generate_query(user_id=user_id, lexeme_id=lexeme_id)
        stats = {k: stats[k].to_json() for k in stats}
        document = dict(user_id=user_id, lexeme_id=lexeme_id, stats=stats)
        self.vocabulary_connector.update_document(query=query, document=document)