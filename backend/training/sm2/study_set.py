from training.sm2.utils import get_repetition_interval
from training.sm2.recall import Recall


class StudySet(object):
  """
  A set of study terms to manage and study in a training session
  """
  def __init__(self, vocabulary: list, count: int = 50):
    """
    Initialize the collection of terms that we're gonna use to study.

    Args:
        vocabulary (list): list of vocabulary terms
        count (int, optional): The maximum number of terms to collect for studying. Defaults to 50.
    """
    self.vocabulary = sorted(vocabulary, key=lambda x: x.stats.interval)[:count]
    
    for vocab in self.vocabulary:
      vocab.stats.session_update()


  def get_study_term(self) -> dict:
    """
    Pop a term from the vocabulary list, removing terms when they have a recall better than 4 (Recall.GREAT)

    Returns:
        dict: term to study
    """
    while self.vocabulary:
      term = self.vocabulary.pop(0)

      if term.stats.recall.value < Recall.GREAT.value:
        self.vocabulary.append(term)
        return term

    return None


  def __sizeof__(self) -> int:
    return len(self.vocabulary)