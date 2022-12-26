import pymongo

character_index = {
    'keys': [("lemma", pymongo.ASCENDING)],
    'name': "character index",
    'unique': True
}

character_schema = {"$jsonSchema": {
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
            "bsonType": "array",
        },
        "definitions": {
            "bsonType": "array"
        },
        "forms": {
            "bsonType": "object"
        },
        "romanizations": {
            "bsonType": "object"
        },
        "radical": {
            "bsonType": "bool"
        },
        "strokes": {
            "bsonType": "int"
        }
    }
}}

vocabulary_index = {
    'keys': [("character_id", pymongo.ASCENDING)],
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
        "character_id": {
            "bsonType": "objectId"
        },
        "word_id": { # TODO phrases? words? tbd
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