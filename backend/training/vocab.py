from training.sm2.stats import Stats


class Vocab(object):
  """
  An object that represents a vocab term being studied
  """
  def __init__(self, lexeme_id: str, vocab_id: str, lexeme: dict, stats: Stats):
    self.lexeme_id = lexeme_id
    self.vocab_id = vocab_id
    self.lexeme = lexeme
    self.stats = stats