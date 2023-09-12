import pymongo

lexeme_index = {
    'keys': [("lemma", pymongo.ASCENDING)],
    'name': "lexeme index",
    'unique': True
}

lexeme_schema = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["_id", "lemma", "pos", "definitions", "written_forms", "romanizations"],
    "properties": {
        "_id": {
            "bsonType": "objectId",
        },
        "lemma": {
            "bsonType": "string"
        },
        "character_ids": {
            "bsonType": "array"
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
            "bsonType": "array"
        },
        "romanizations": {
            "bsonType": "object"
        },
        "radical": {
            "bsonType": "bool"
        },
        "stroke_counts": {
            "bsonType": "object"
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
    "required": ["_id", "user_id", "stats", "lexeme_id"],
    "properties": {
        "_id": {
            "bsonType": "objectId"
        },
        "lexeme_id": {
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