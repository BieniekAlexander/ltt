import enum
import json, sys, os
from json.encoder import JSONEncoder
from enum import Enum, auto

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .part_of_speech import PartOfSpeech
from utils.data_structure_utils import json_preprocess

# TODO add definitions and translations
class Lexeme():
    """
    A representation of a basic word of a language from which ideas are derived.

    https://en.wikipedia.org/wiki/Lexeme

    Attributes:
        lemma (str): The most basic form of the word.
        pos (PartOfSpeech): The part of speech of the word.
    """

    def __init__(self, lemma, pos, definitions):
        """
        Term constructor, which instantiates the object and checks its validity in the language's semantic model.
        """
        # check input types
        assert isinstance(pos, PartOfSpeech) or isinstance(pos, str)
        assert isinstance(pos, str)
        assert isinstance(definitions, list)

        if type(pos) != PartOfSpeech:
            pos = PartOfSpeech[pos.upper()]

        self.lemma = lemma
        self.pos = pos
        self.definitions = definitions


    def to_json_dict(self):
        """
        Convert the [Lexeme] into a JSON dictionary 
        """
        # TODO maybe this needs to be recursive, in the case that dicts and lists contain JSON-compliant primitives
        # TODO also find if there's something compatible with implicit serializer thingies? What if the object has 
        # fields containing objects that recursively need to be serialized to JSON-compliant primitives?
        # return self.__dict__
        dump_dict = self.__dict__

        def jsonify(obj):
            if isinstance(obj, str) and isinstance(obj, Enum):
                return str(obj.value)
            elif isinstance(obj, list):
                return list(map(lambda x: jsonify(x), obj))
            elif isinstance(obj, dict):
                return {k: jsonify(v) for k, v in obj.items()}
            else:
                return obj

        return jsonify(dump_dict)

    
    def to_json_str(self):
        """
        Convert the [Lexeme] into a JSON string
        """
        return json.dumps(self.to_json_dict(), sort_keys=True, indent=4)

    
    def __eq__(self, other) -> bool:
        """
        Compare two terms for equality, ignoring irrelevant parts of the Lexeme
        """
        jsonSelf = self.to_json_dict()
        jsonOther = other.to_json_dict()
        return jsonSelf == jsonOther
        

# https://stackoverflow.com/a/58683139
class LexemeEncoder(json.JSONEncoder):
    """
    Encodes a model [Lexeme] into a JSON object
    """
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name.upper()
        elif issubclass(type(obj), Lexeme):
            return obj.to_json_dict()
        else:
            return json.JSONEncoder.default(self, o)
            # return self.default(obj)


class LexemeDecoder(json.JSONDecoder):
    """ 
    Decodes a JSON object into a [Lexeme]
    """
    def decode(self, str):
        json_dict = json.loads(str)
        from model import model_class_map
        cls = model_class_map["POLISH"][json_dict['pos']] # TODO address how we're identifying the language of the object
        return cls(**json_dict)