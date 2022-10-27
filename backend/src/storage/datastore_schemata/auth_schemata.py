auth_schema = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["_id", "username", "password"],
    "properties": {
        "_id": {
            "bsonType": "objectId",
        },
        "username": {
            "bsonType": "string",
        },
        "password": {
            "bsonType": "string",
        }
    }
}}