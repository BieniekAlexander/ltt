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
        