import pymongo
from language.lexeme import Lexeme
from language.part_of_speech import PartOfSpeech
from storage.datastore_utils import get_dataclass_mongodb_schema, get_dataclass_mongodb_index

lexeme_index = {
    'keys': [("lemma", pymongo.ASCENDING), ("pos", pymongo.ASCENDING)],
    'name': "lexeme index",
    'unique': True
}

lexeme_schema = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["_id", "lemma", "pos", "definitions"],
    "properties": {
        "_id": {
            "bsonType": "objectId",
        },
        "lemma": {
            "bsonType": "string",
        },
        "pos": {
            "bsonType": "string",
        },
        "definitions": {
            "bsonType": "array"
        }
    }
}}

inflection_index = {
    'keys': [("form", pymongo.ASCENDING), ("pos", pymongo.ASCENDING), ("lexeme_id", pymongo.ASCENDING)],
    'name': "inflection index",
    'unique': True
}

inflection_schema = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["_id", "form", "pos", "lexeme_id"],
    "properties": {
        "_id": {
            "bsonType": "objectId",
        },
        "form": {
            "bsonType": "string",
        },
        "pos": {
            "bsonType": "string",
        },
        "lexeme_id": {
            "bsonType": "objectId"
        }
    }
}}

vocabulary_index = {
    'keys': [("lexeme_id", pymongo.ASCENDING), ("user_id", pymongo.ASCENDING)],
    'name': "vocabulary index",
    'unique': True
}

vocabulary_schema = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["_id", "user_id", "stats"],
    "properties": {
        "_id": {
            "bsonType": "objectId"
        },
        "lexeme_id": {
            "bsonType": "objectId"
        },
        "phrase_id": { # TODO implement phrases
            "bsonType": "objectId"
        },
        "user_id": {
            "bsonType": "objectId"
        },
        "stats": {
            "bsonType": "object"
        }
    }
}}