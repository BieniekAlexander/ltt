import pymongo

character_index = {
    'keys': [("characters", pymongo.ASCENDING)],
    'name': "character index",
    'unique': True
}

character_schema = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["_id", "lemma", "pos", "definitions", "is_radical", "radicals", "variants", "written_forms", "romanizations", "stroke_counts"],
    "properties": {
        "_id": {
            "bsonType": "objectId",
        },
        "characters": {
            "bsonType": "string"
        },
        "character_ids": {
            "bsonType": "list"
        },
        "pos": {
            "bsonType": "array",
        },
        "definitions": {
            "bsonType": "array"
        },
        "written_forms": {
            "bsonType": "object"
        },
        "written_forms_list": {
            "bsonType": "object"
        },
        "romanizations": {
            "bsonType": "object"
        },
        "radical": {
            "bsonType": "bool"
        },
        "stroke_counts": {
            "bsonType": "int"
        }
    }
}}

vocabulary_index = {
    'keys': [("character_id", pymongo.ASCENDING), ("word_id", pymongo.ASCENDING)],
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