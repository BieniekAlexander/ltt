"""
Functions of the Supermemory 2 algorithm

source: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
"""
from math import ceil

from training.sm2.recall import Recall


def get_easiness_factor(ef: float, recall: Recall) -> float:
    """
    Recalculate the easiness factor

    Args:
        ef (float): easiness previous factor
        recall (Recall): recall quality

    Returns:
      float: The new easiness factor
    """
    assert recall in Recall

    q = recall.value
    return max(ef - .8 + .28*q - .02*q**2, 1.3)


def get_repetition_interval(repetition: int, ef: float) -> int:
    """
    Get the number of sessions that the algorithm should wait until we need to review this term

    Args:
        repetition (int): the number repitition that this is
        ef (float): the easines factor

    Returns:
        int: the number of sessions until next review
    """
    assert repetition > 0
    interval = 0

    if repetition == 1:
        interval = 1
    elif repetition == 2:
        interval = 6
    else:
        interval = get_repetition_interval(repetition-1, ef) * ef

    return ceil(interval)


def get_repetition(repetition: int, recall: Recall) -> int:
    """
    Recalculate the repetition count we're on

    Specifically, if [Recall]>2, then repetition=repetition+1; otherwise, repetition=0

    Args:
        repetition (int): the number of repetitions done so far
        recall (Recall): the quality of the previous recall

    Returns:
        int: the repetition count
    """
    if recall.value > 2:
        return repetition+1
    else:
        return 1