import json

from . import model_class_map


class LexemeDecoder(json.JSONDecoder):
  """ 
  Decodes a JSON object into a [Lexeme]
  """

  def decode(self, input_str):
    json_dict = json.loads(input_str)
    # TODO address how we're identifying the language of the object
    cls = model_class_map["POLISH"][json_dict['pos']]
    return cls(**json_dict)