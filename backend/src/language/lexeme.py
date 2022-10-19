import json

from utils.json_utils import JSONSerializable

from .part_of_speech import PartOfSpeech

# TODO add definitions and translations


class Lexeme(JSONSerializable):
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

    def to_json_str(self):
        """
        Convert the [Lexeme] into a JSON string
        """
        return json.dumps(self.to_json(), sort_keys=True, indent=4)

    def __eq__(self, other) -> bool:
        """
        Compare two terms for equality
        """
        assert issubclass(type(other), Lexeme)

        jsonSelf = self.to_json()
        jsonOther = other.to_json()
        return jsonSelf == jsonOther
