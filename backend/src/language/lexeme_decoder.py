import json

from . import MODEL_CLASS_MAP


class LexemeDecoder(json.JSONDecoder):
    """ 
    Decodes a JSON object into a [Lexeme]
    """

    def decode(self, input_str):
        json_dict = json.loads(input_str)
        # TODO address how we're identifying the language of the object
        cls = MODEL_CLASS_MAP["POLISH"][json_dict['pos']]
        return cls(**json_dict)
