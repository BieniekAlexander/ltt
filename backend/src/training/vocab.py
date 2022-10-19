import json

from training.sm2.stats import Stats, StatsDecoder


class Vocabulary(object):
  """
  An object that represents a vocab term being studied
  """
  def __init__(self, lexeme_id: str, vocab_id: str, lexeme: dict, stats: Stats):
    self.lexeme_id = lexeme_id
    self.vocab_id = vocab_id
    self.lexeme = lexeme
    self.stats = stats


class VocabularyDecoder(json.JSONDecoder):
  """ 
  Decodes a JSON object into a [Term]
  """
  def decode(self, input_str):
    json_dict = json.loads(input_str)
    json_dict['stats'] = json.loads(str(json_dict['stats']), cls=StatsDecoder)

    return Vocabulary(**json_dict)