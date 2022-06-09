import json


from training.sm2.recall import Recall
from training.sm2.utils import get_easiness_factor


class Stats(object):
  def __init__(self, repetition: int = 1, interval: int = 1, ef: float = 2.5, recall: Recall = None):
    """
    A struct that represents when a user will next review a term

    based on the Supermemory 2 Algorithm

    Args:
        ef (float): easiness factor
        repetition (int): the number of times this term has been studied
    """
    assert repetition > 0

    self.repetition = repetition
    self.interval = interval
    self.ef = ef
    self.recall = recall

  
  def update(self, recall: Recall) -> None:
    """
    Recalculate the memory stats of a term

    Args:
        recall (Recall): the recall quality of the term
    """
    self.ef = get_easiness_factor(self.ef, recall)
    self.recall = recall


  def session_update(self) -> None:
    """
    Initialize the stats of a study term at the start of a study session
    """
    self.ef = 2.5
    self.recall = Recall.UNKNOWN


  def to_json_dictionary(self) -> dict:
    """
    Convert the [Stats] into a JSON dictionary 
    """
    return {"repetition": self.repetition, "interval": self.interval, "ef": self.ef, "recall": self.recall}

    
  def to_json_str(self) -> str:
    """
    Convert the [Stats] into a JSON string
    """
    return json.dumps(self.to_json_dictionary(), sort_keys=True, indent=4)

    
  def __eq__(self, other) -> bool:
    """
    Compare two [Stats] for equality
    """
    assert issubclass(type(other), Stats)

    jsonSelf = self.to_json_dictionary()
    jsonOther = other.to_json_dictionary()
    return jsonSelf == jsonOther


  def __str__(self) -> str:
    """
    Represent the [Stats] as JSON string 
    """
    return self.to_json_str()