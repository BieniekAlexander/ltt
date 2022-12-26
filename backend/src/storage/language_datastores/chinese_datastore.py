from bson.objectid import ObjectId
from pymongo import MongoClient
from typing import Any

from training.sm2_anki.stats import Stats
from language.chinese.character import Character
from storage.collection_connector import CollectionConnector
from utils.data_structure_utils import get_nested_iterable_values
from storage.datastore_utils import generate_query, generate_member_query

from storage.datastore_schemata.chinese_schemata import (
    character_schema as zh_character_schema,
    vocabulary_schema as zh_vocabulary_schema
)

# TODO currently manually getting BSON to get this going, but I should add deserialization support
def get_character_bson(character: Character):
    return {
        'lemma': character.lemma,
        'pos': character.pos,
        'definitions': character.definitions,
        'forms': character.forms,   
        'forms_list': list(set(get_nested_iterable_values(character.forms))), # TODO this isn't part of the data class, but I might need a list of values to make it searchable
        'romanizations': character.romanizations,
        'is_radical': character.is_radical,
        'stroke_counts': character.stroke_counts
    }


# %% Implementation
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
        self.character_connector = CollectionConnector(datastore_client, self.language, 'characters', zh_character_schema['$jsonSchema'])
        self.vocabulary_connector = CollectionConnector(datastore_client, self.language, 'vocabulary', zh_vocabulary_schema['$jsonSchema'])

    def add_character(self, character: Character) -> ObjectId:
        """
        Add a lexeme to the datastore, add related data (i.e. inflection mappings), and get the lexeme_id
        """
        assert isinstance(character, Character)

        character_bson = get_character_bson(character)
        return self.character_connector.push_document(character_bson)

    def add_characters(self, characters: list) -> list[ObjectId]:
        """
        Add a lexeme to the datastore, add related data (i.e. inflection mappings), and get the lexeme_id
        """
        assert isinstance(characters, list) and all(
            isinstance(character, Character) for character in characters)

        character_bsons = list(map(lambda x: get_character_bson(x), characters))
        return self.character_connector.push_documents(character_bsons)

    def delete_character(self, _id: ObjectId) -> None:
        """
        remove a lexeme from the language datastore by [_id]

        TODO is this even necessary?
        """
        self.character_connector.delete_document(generate_query(_id=_id))

    def get_character_from_form(self, form: str) -> Character:
        """
        Get a character, given some form of it
        """
        assert isinstance(form, str)

        characters = self.get_characters_from_form(form)
        
        if len(characters)>1:
            raise Exception(f"Found more than one character with form={form}")
        elif len(characters) == 1:
            return characters[0]
        else:
            return None

    def get_characters_from_form(self, form: str) -> list[Character]:
        """
        Get a character, given soem form of it
        """
        assert isinstance(form, str)

        return self.character_connector.collection.find(generate_member_query('forms_list', form))

    def get_characters(self, **kwargs) -> list[Character]:
        """
        Get a list of characters
        """
        return self.character_connector.get_documents(generate_query(**kwargs))

    def get_vocabulary_entry(self, character_id: str, user_id: str) -> dict:
        return self.vocabulary_connector.get_document(generate_query(character_id=character_id, user_id=user_id))

    def get_vocabulary_entries(self, character_ids: list, user_id: str) -> dict:
        return self.vocabulary_connector.get_document(generate_query(character_id=character_ids, user_id=user_id))

    def add_vocabulary_entry(self, character_id: ObjectId, stats: dict[str, Stats], user_id: ObjectId) -> str:
        """
        Add a [lexeme_id], [stats] entry to the vocabulary for [user_id]

        Args:
          character_id (ObjectId): the identifier of the character to be added to the vocabulary
          stats (dict[str, Stats]): the initial SRS stats of the vocabulary term for the user
          user_id (ObjectId): the identifier for the user that should receive the new vocabulary entry
        """
        stats = {k: stats[k].to_json() for k in stats}
        self.vocabulary_connector.push_document(dict(character_id=character_id, stats=stats, user_id=user_id))

    def add_vocabulary_entries(self, entries: list[dict]) -> list:
        """
        Add a list of vocabulary [entries] to the vocabulary for [user_id]

        Args:
          entries: a [list] of [dict]s containing character_id, stats, and user_id
        """
        for entry in entries:
            assert set(['character_id', 'stats', 'user_id']) == entry.keys()

        assert len(set(entry['user_id'] for entry in entries)) == 1

        return self.vocabulary_connector.push_vocabulary_entries(entries)

    def update_vocabulary_entry(self, character_id: str, stats: dict[str, Stats], user_id: str) -> None:
        """Update the vocabulary entry for [character_id] under [user_id] with the given stats

        Args:
          character_id (str): the identifier of the lexeme to be added to the vocabulary
          stats (str): the initial SRS stats of the vocabulary term for the user
          user_id (str): the identifier for the user that should receive the new vocabulary entry

        Returns:
            str: _description_
        """
        query = generate_query(user_id=user_id, character_id=character_id)
        stats = {k: stats[k].to_json() for k in stats}
        document = dict(user_id=user_id, character_id=character_id, stats=stats)
        self.vocabulary_connector.update_document(query=query, document=document)
 