import json
from dataclasses import dataclass
from typing import Union, Optional
from enforce_typing import enforce_types

from training.sm2_anki.recall import Recall, RECALL_EASINESS_FACTORS, RECALL_INTERVALS
from utils.json_utils import JSONSerializable

# number of days betwen study sessions when the card is in learning mode
STEP_INTERVALS = [0, 1, 3, 10]
MAX_INTERVAL = 365


@enforce_types
@dataclass
class Stats(JSONSerializable):
    """
    A struct that represents when a user will next review a term

    based on the Anki sm2 algorithm

    Args:
        interval (int): the number of days until the next time you have to study the term
        ef (float): easiness factor
        recall (Recall): your ability to recall the term (updated in the study session)
        step (int): the number of times you've studied the term towards graduation (-1 if graduated)
        suspended (bool): whether the card is, for whatever reason, currently suspended from studying
    """
    interval: int = 0
    ef: float = 2.5
    recall: Optional[Union[Recall, int]] = None
    step: int = 0
    suspended: bool = False

    def __post_init__(self):
        """
        Assert values after initialization
        """
        assert self.ef >= 1.3
        assert self.step >= -1

    def update(self, recall: Recall) -> None:
        """
        Recalculate the memory stats of a term

        Args:
            recall (Recall): the recall quality of the term
        """
        # TODO Anki's sm2 has a less direct manner of deciding what needs to be studied again in this session vs what gets saved for the next session
        # words are instead sort of studied either loosely later in the session (i.e. in 10 min?) or, depending on the step, sometime in another session
        # it's eventually graduated and the intervals are calculated differently
        self.recall = Recall(recall)

        
        if recall == Recall.FORGET:
            raise Exception("forgetting should not be handled here, it should be handled at the study entry level!")
        elif recall == Recall.SUSPEND:
            self.suspended = True
        if self.step == -1: # in review phase
            self.ef = max(self.ef*RECALL_EASINESS_FACTORS[recall], 1.3)

            if recall == 0:
                self.step = 0
            elif recall == 1:
                self.interval = int(self.interval*RECALL_INTERVALS[recall])
            else:
                self.interval = int(max(self.ef*self.interval, 1))
        else: # in learning phase
            if recall == 0:
                self.step = 0
            elif recall == 2:
                if self.step+1==len(STEP_INTERVALS):
                    self.step = -1
                    self.interval = 1
                else:
                    self.step += 1
            elif recall == 3:
                self.step = -1
                self.interval = 4

            if self.step != -1:
                self.interval = STEP_INTERVALS[self.step]

        self.interval = max(self.interval, MAX_INTERVAL)

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