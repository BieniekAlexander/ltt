import json
from typing import Union

from training.sm2.recall import Recall
from training.sm2.utils import (get_easiness_factor, get_repetition,
                                get_repetition_interval)
from utils.json_utils import JSONSerializable

class Stats(JSONSerializable):
    def __init__(self, repetition: int = 0, interval: int = 1, ef: float = 2.5, recall: Union[Recall, int] = None):
        """
        A struct that represents when a user will next review a term

        based on the Supermemory 2 Algorithm

        Args:
            ef (float): easiness factor
            repetition (int): the number of times this term has been studied
        """
        assert repetition >= 0

        self.repetition = repetition
        self.interval = interval
        self.ef = ef
        self.recall = Recall(recall)

    def update(self, recall: Union[Recall, int]) -> None:
        """
        Recalculate the memory stats of a term

        Args:
            recall (Recall): the recall quality of the term
        """
        self.ef = get_easiness_factor(self.ef, recall)
        self.recall = recall

    def session_init(self) -> None:
        """
        Initialize the stats of a study term at the start of a study session
        """
        self.recall = None

    def session_update(self) -> None:
        """
        Update the stats of the object after it's been studied
        """
        if self.recall:
            self.repetition = get_repetition(self.repetition, self.recall)
            self.interval = get_repetition_interval(self.repetition, self.ef)

    def __str__(self) -> str:
        """
        Represent the [Stats] as JSON string 
        """
        return str(self.to_json())


class StatsDecoder(json.JSONDecoder):
    """ 
    Decodes a JSON object into a [Stats]
    """

    def decode(self, input_str):
        json_dict = json.loads(input_str)
        return Stats(**json_dict)
