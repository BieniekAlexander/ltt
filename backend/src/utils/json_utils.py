"""
Utils for object serialization and deserialization with python. For portability, any object that gets persisted to a NoSQL database
should implement JSONSerializable to make this portability easier.

references:
https://stackoverflow.com/a/58683139
https://stackoverflow.com/questions/24481852/serialising-an-enum-member-to-json
https://realpython.com/python-interface/
"""
import abc
import json
from enum import Enum

# from language import model_class_map


def jsonify(obj):
    """
    Helper method, recursively turn objects or items into a JSON-serializable format
    """
    if isinstance(obj, JSONSerializable):
        return obj.to_json()
    elif isinstance(obj, str) and isinstance(obj, Enum):
        return str(obj.value)
    elif isinstance(obj, list):
        return list(map(lambda x: jsonify(x), obj))
    elif isinstance(obj, dict):
        return {k: jsonify(v) for k, v in obj.items()}
    else:
        return obj


class JSONSerializable(metaclass=abc.ABCMeta):
    def to_json(self) -> dict:
        """
        Convert the [Lexeme] into a JSON dictionary 
        """
        return jsonify(self.__dict__)

    def to_json_str(self):
        """
        Convert the [Lexeme] into a JSON string
        """
        return json.dumps(self.to_json(), sort_keys=True, indent=4)


class JSONSerializableEncoder(json.JSONEncoder):
    """
    Encodes an object, which implements [JSONSerializable], into a JSON object
    """

    def default(self, obj):
        if isinstance(obj, JSONSerializable):
            return obj.to_json()
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":

    class A():
        pass

    class B(JSONSerializable):
        pass

    class C(JSONSerializable):
        def to_json() -> dict:
            return {'key': 'value'}

    for cls in [A, B, C]:
        print(
            f"{cls} is a subclass of {JSONSerializable}?: {issubclass(cls, JSONSerializable)}")

        try:
            cls()
        except Exception as e:
            print(f"\t{e}")
