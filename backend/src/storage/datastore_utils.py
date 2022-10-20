# %% imports
from enum import Enum

from bson.objectid import ObjectId


# %% utils
def cast_enum_to_str(e):
    if issubclass(type(e), Enum):
        assert issubclass(type(e), str), "This enum should inheret str"
        return e.value
    elif isinstance(e, str):
        return e.upper()
    else:
        raise ValueError("Expected [Enum] or [str]")


def generate_query(**kwargs):
    """
    Create a query 
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


if __name__ == "__main__":
    print(generate_query(lemma=100, _id=[1, 2, 3]))
