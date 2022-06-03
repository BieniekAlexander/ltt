# TODO for a given term as remembered by a given user, what metrics are we using to calculate the priority of this term being reviewed?
import sys, os
import json
from xmlrpc.client import Boolean


from language.inflected_lexeme import InflectedLexeme
from language.polish.feat.degree import Degree
from language.model_errors import LexemeError


class Stats(object):
  def __init__(self, rating: float):
    """
    A struct that represents a user's ability to remember a term

    Args:
        rating (float): temporary implementation of how a user is doing with a fact
    """
    self.rating = rating


  def to_json_dictionary(self):
    """
    Convert the [Stats] into a JSON dictionary 
    """
    return {"rating": self.rating}

    
  def to_json_str(self):
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

  
  def mod(self, mult: float) -> None:
    """TODO probably a temp function, modify the rating of this stat with the given multiplier

    Args:
        mult (float): the given multiplier
    """
    self.rating *= mult


class StatsComparison(object): # TODO I need to find priority queues that take comparison functions - sort uses a key
  def __init__(self):
    """
    Constructor for Stats comparison function
    """
    pass


  def __call__(self, stats_left: Stats, stats_right: Stats) -> bool:
    """
    Compare two stats, and return True if [stats_left] is less than [stats_right]

    Args:
        stats_left (Stats): lefthand side stats value
        stats_right (Stats): righthand side stats value

    Returns:
        bool: True if the lefthand side is lower than the righthand side
    """
    return stats_left.rating < stats_right.rating