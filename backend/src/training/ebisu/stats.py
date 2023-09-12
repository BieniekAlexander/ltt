import json
from dataclasses import dataclass, field
from enforce_typing import enforce_types
from typing import Union
from datetime import datetime

from utils.json_utils import JSONSerializable

FLOAT_ERROR = .001

def now_in_seconds() -> float:
    """
    Get the current time in seconds
    """
    return datetime.now().timestamp()


@enforce_types
@dataclass
class Stats(JSONSerializable):
    """
    A struct that represents a model for Ebisu memory decay

    Args:
        last_study_time (float): the unix timestamp of the last study time
        alpha (float): the alpha parameter of the Ebisu beta distribution
        beta (float): the beta parameter of the Ebisu beta distribution
        half_life (float): the half-life of the memory decay (in seconds)
        suspended (bool): Whether we want to suspend this card from showing up in our study set
    """
    last_study_time: Union[float, int] = field(default_factory=now_in_seconds)
    alpha: Union[float, int] = 2.0
    beta: Union[float, int] = 2.0
    half_life: Union[float, int] = 60*60*24.0
    suspended: bool = False

    def __post_init__(self):
        """
        Assert values after initialization
        """
        self.alpha = float(self.alpha)
        self.beta = float(self.beta)

        assert self.half_life > (1.0-FLOAT_ERROR)
        assert self.alpha > (2.0-FLOAT_ERROR)
        assert self.beta > (2.0-FLOAT_ERROR)

    def __str__(self) -> str:
        """
        Represent the [Stats] as JSON string 
        """
        return str(self.to_json())

    def get_prior(self) -> tuple:
        """
        Get the current Ebisu model for the fact's recallability
        """
        return (self.alpha, self.beta, self.half_life)


class StatsDecoder(json.JSONDecoder):
    """ 
    Decodes a JSON object into a [Stats]
    """

    def decode(self, input_str):
        json_dict = json.loads(input_str)
        return Stats(**json_dict)