# https://www.mongodb.com/docs/manual/reference/operator/query/jsonSchema/#mongodb-query-op.-jsonSchema
# https://stackoverflow.com/questions/55025621/mongodb-add-schema-for-existing-collection
# https://www.mongodb.com/docs/manual/reference/bson-types/
import pymongo


from language.part_of_speech import PartOfSpeech


lexeme_index = {
    'keys': [("lemma", pymongo.ASCENDING), ("pos", pymongo.ASCENDING)],
    'name': "lemma index",
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

user_vocabulary_index = {
    'keys': [("user_id", pymongo.ASCENDING), ("lexeme_id", pymongo.ASCENDING)],
    'name': "user vocabulary index",
    'unique': True
}

user_vocabulary_schema = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["_id", "lexeme_id", "user_id", "stats"],
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

inflections_index = {
    'keys': [("form", pymongo.ASCENDING), ("pos", pymongo.ASCENDING), ("lexeme_id", pymongo.ASCENDING)],
    'name': "inflections index",
    'unique': True
}

inflections_schema = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["_id", "lexeme_id", "form", "pos"],
    "properties": {
        "_id": {
            "bsonType": "objectId"
        },
        "lexeme_id": {
            "bsonType": "objectId"
        },
        "form": {
            "bsonType": "string"
        },
        "pos": {
            "enum": list(PartOfSpeech)
        }
    }
}}
