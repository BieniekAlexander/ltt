import json
from bson import ObjectId
from typing import Optional
from enforce_typing import enforce_types
from dataclasses import dataclass

from language.lexeme import Lexeme
from training.sm2_anki.stats import Stats, StatsDecoder

@enforce_types
@dataclass
class Vocabulary:
    """
    An object that represents a vocab term being studied
    """
    lexeme_id: str
    vocab_id: str
    lexeme: Lexeme
    stats: dict
    

class VocabularyDecoder(json.JSONDecoder):
    """ 
    Decodes a JSON object into a [Term]
    """
    def decode(self, input_str):
        json_dict = json.loads(input_str)
        json_dict['stats'] = {
            key: json.loads(str(json_dict['stats']), cls=StatsDecoder)
            for key in json_dict['stats']}

        return Vocabulary(**json_dict)
