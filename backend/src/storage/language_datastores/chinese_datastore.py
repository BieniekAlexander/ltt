from bson.objectid import ObjectId
from pymongo import MongoClient
from typing import Any, Union

from enforce_typing import enforce_types
from training.ebisu.stats import Stats
from language.chinese.character import Character
from language.chinese.word import Word
from storage.collection_connector import CollectionConnector
from utils.data_structure_utils import get_nested_iterable_values
from storage.datastore_utils import generate_query, generate_member_query

from storage.datastore_schemata.chinese_schemata import (
    lexeme_schema as zh_character_schema,
    vocabulary_schema as zh_vocabulary_schema
)


def deserialize_chinese_from_bson(entry_bson: dict) -> Union[Word, Character]:
    """
    TODO
    """
    if len(entry_bson['lemma']) == 1:
        return Character.from_bson(entry_bson)
    else:
        return Word.from_bson(entry_bson)

class ChineseDatastore:
    """
    A datastore interface that abstracts storage of language data
    """
    language = 'chinese'

    def __init__(self, datastore_client: MongoClient):
        """ A connector that handles interaction with a language, as it exists in the datastore

        Args:
            datastore_client (MongoClient): the MongoDB client used to interact with the datastore
        """
        self.datastore_client = datastore_client
        self.lexicon_connector = CollectionConnector(datastore_client, self.language, 'lexicon', zh_character_schema['$jsonSchema'])
        self.vocabulary_connector = CollectionConnector(datastore_client, self.language, 'vocabulary', zh_vocabulary_schema['$jsonSchema'])

    @enforce_types
    def add_lexemes(self, entries: list[Union[Character, Word]]) -> list[ObjectId]:
        """
        Add a lexeme to the datastore (chinese character or word), add related data (i.e. inflection mappings), and get the lexeme_id
        """

        entry_bsons = []
        
        for entry in entries:
            entry_bson = entry.to_bson()

            # if this is a word, join the _ids of the characters it's composed of
            if isinstance(entry, Word):
                character_list = list(entry_bson['lemma'])
                entry_bson['character_ids'] = []

                for character in character_list:
                    # TODO probably update wrappers so I can get this mapping more easily
                    character_bson_list = list(self.lexicon_connector.collection.find(generate_query(lemma=character)))

                    if len(character_bson_list) != 0:
                        character_bson = character_bson_list[0]
                        entry_bson['character_ids'].append(character_bson['_id'])

            entry_bsons.append(entry.to_bson())

        return self.lexicon_connector.push_documents(entry_bsons)

    @enforce_types
    def delete_lexeme(self, _id: ObjectId) -> None:
        """
        remove a lexeme from the language datastore by [_id]

        TODO is this even necessary?
        """
        self.lexicon_connector.delete_document(generate_query(_id=_id))

    @enforce_types
    def get_lexemes_from_form(self, form: str) -> dict[ObjectId, Union[Character, Word]]:
        """
        Get a character or word, given some form of it
        """
        bson_list = list(self.lexicon_connector.collection.find(generate_member_query('forms_list', form)))
        
        if bson_list != []:
            return {lexeme_bson.pop("_id"): deserialize_chinese_from_bson(lexeme_bson) for lexeme_bson in bson_list}
        else:
            return {}

    def get_lexemes(self, **kwargs) -> dict[ObjectId, Union[Character, Word]]:
        """
        Get a list of characters
        """
        lexeme_list = self.lexicon_connector.get_documents(generate_query(**kwargs))
        lexeme_dict = {}

        lexeme_dict = {lexeme_bson.pop("_id"): deserialize_chinese_from_bson(lexeme_bson) for lexeme_bson in lexeme_list}
        return lexeme_dict
        
    @enforce_types
    def add_vocabulary_entries(self, entries: list[dict]) -> list[ObjectId]:
        """
        Add a list of vocabulary [entries] to the vocabulary for [user_id]

        Args:
          entries: a [list] of [dict]s containing lexeme_id, stats, and user_id
        """
        for entry in entries:
            assert set(['lexeme_id', 'stats', 'user_id']) == entry.keys()
            entry['stats'] = {k: entry['stats'][k].to_json() for k in entry['stats']} # TODO clean up all of this shit

        assert len(set(entry['user_id'] for entry in entries)) == 1

        return self.vocabulary_connector.push_documents(entries)

    @enforce_types
    def get_vocabulary_entries(self, user_id: ObjectId, lexeme_id: list[ObjectId] = []) -> list[dict]:
        """
        Add a list of vocabulary [entries] to the vocabulary for [user_id]

        Args:
          entries: a [list] of [dict]s containing lexeme_id, stats, and user_id
        """
        query = generate_query(lexeme_id=lexeme_id, user_id=user_id)
        # TODO results is returning empty for lexemes, but it should be finding matches
        agg_pipeline = [
            {"$match": query},
            {"$lookup": { "from": 'lexicon', "localField": 'lexeme_id', "foreignField": '_id', "as": 'lexemes' } }]
        results = list(self.datastore_client['chinese']['vocabulary'].aggregate(agg_pipeline))
        import time

        for result in results:
            result['lexeme'] = deserialize_chinese_from_bson(result.pop('lexemes')[0])
            result['vocabulary_id'] = result.pop('_id')
            result['stats'] = {key: Stats(**result['stats'][key]) for key in result['stats']}

        return results

    def update_vocabulary_entry(self, lexeme_id: ObjectId, stats: dict[str, Stats], user_id: str) -> None:
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

    def delete_vocabulary_entry(self, vocabulary_id) -> None:
        """Delete the vocabulary entry, as identified by [vocabulary_id]
        
        Args:
            vocabulary_id: The ID of the vocabulary entry to delete
        """
        self.vocabulary_connector.delete_document({"_id": vocabulary_id})


if __name__ == "__main__":
    import os

    user_id = ObjectId("62a57d5bfa96028f59ac1d75")
    MONGODB_URI = os.getenv("MONGODB_URI")
    ds_client = MongoClient(MONGODB_URI)
    chinese_datastore = ChineseDatastore(ds_client)

    print(chinese_datastore.get_vocabulary_entries(user_id=user_id))