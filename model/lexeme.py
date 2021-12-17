import enum
import json, sys, os
from enum import Enum, auto

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .part_of_speech import PartOfSpeech


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
        dump_dict = self.__dict__

        for key, val in dump_dict.items():
            if isinstance(val, Enum):
                dump_dict[key] = val.name.upper()

        return dump_dict

    
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
        

class LexemeEncoder(json.JSONEncoder):
    """
    Encodes a model [Lexeme] into a JSON object
    """
    def default(self, o):
        if isinstance(o, Enum):
            return o.name.upper()
        elif issubclass(type(o), Lexeme):
            return o.to_json_dict()
        else:
            return json.JSONEncoder.default(self, o)


class LexemeDecoder(json.JSONDecoder):
    """ 
    Decodes a JSON object into a [Lexeme]
    """
    def decode(self, str):
        json_dict = json.loads(str)
        from model import model_class_map
        cls = model_class_map["POLISH"][json_dict['pos']] # TODO address how we're identifying the language of the object
        return cls(**json_dict)