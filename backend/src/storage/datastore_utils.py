from enum import Enum
import datetime
import dataclasses
import re
from typing import Any

import pymongo
from bson.objectid import ObjectId

BSON_BUILT_IN_TYPE_MAPPING = {
    # I haven't added absolutely everything, I don't think I'll need it
    type(None): "null",
    bool: "bool",
    int: "int",
    float: "number",
    str: "string",
    list: "array",
    dict: "object",
    datetime.datetime: "date",
    ObjectId: "objectId",
    bytes: "binary"
}


def get_type_mapping(typ: type):
    """
    Get the BSON type associated with a python type, or "objectId" if the type is an application class

    https://pymongo.readthedocs.io/en/stable/api/bson/index.html
    https://www.mongodb.com/docs/manual/reference/bson-types/
    """
    if typ in BSON_BUILT_IN_TYPE_MAPPING:
        return BSON_BUILT_IN_TYPE_MAPPING[typ]
    elif type(typ) == type:
        return ObjectId
    else:
        raise TypeError("The argument is not a type")

def get_dataclass_bson_property_mapping(cls: type):
    """
    Get the mapping of a dataclass's fields to the bson type strings
    """
    assert dataclasses.is_dataclass(cls)

    return {field: get_type_mapping(cls.__data_class_fields__[field].type) for field in cls.__data_class_fields__}

def get_dataclass_mongodb_schema(cls: type):
    """
    Get a bson schema for a dataclass object

    TODO current implementation isn't generic enough for my needs, maybe work on implementation more
    """
    assert dataclasses.is_dataclass(cls)

    dataclass_bson_property_mapping = get_dataclass_bson_property_mapping(cls)

    return {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id"] + list(dataclass_bson_property_mapping.keys()),
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                **{key: {'bsonType': dataclass_bson_property_mapping[key]} for key in dataclass_bson_property_mapping}
            }
        }
    }

def get_dataclass_mongodb_index(cls: type, name: str = None, fields: list = None, unique: bool = True):
    """
    Generate an index for a dataclass object

    TODO current implementation isn't generic enough for my needs, maybe work on implementation more
    """
    assert dataclasses.is_dataclass(cls)

    name = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', cls.__name__).lower() if name is None else name
    fields = list(cls.__data_class_fields__) if fields is None else fields

    return {
        'keys': [(field, pymongo.ASCENDING) for field in fields],
        'name': f"{name} index",
        'unique': unique
    }

def cast_enum_to_str(e):
    """
    Cast an enumerated type to string
    """
    if issubclass(type(e), Enum):
        assert issubclass(type(e), str), "This enum should inherit str"
        return e.value
    elif isinstance(e, str):
        return e.upper()
    else:
        raise ValueError("Expected [Enum] or [str]")

def generate_query(**kwargs):
    """
    Create a MongoDB query
    """
    query = {}

    for key, value in kwargs.items():
        if any(isinstance(value, t) for t in [str, int, float, bool, ObjectId]):
            query[key] = value
        elif isinstance(value, list) and value:
            query[key] = {"$in": value}
        elif not value:
            pass
        else:
            # TODO create exception type
            raise Exception("Unhandled value type for datastore query")

    return query

def generate_member_query(list_field: str, element: Any):
    """
    Get a query that returns objects for which the [list_field] contains [element]
    """
    return {list_field: { "$elemMatch": {"$eq": element }}}


if __name__ == "__main__":
    from language.lexeme import Lexeme
    print(get_dataclass_mongodb_schema(Lexeme))
