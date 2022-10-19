# custom implementation of priority queues, because I think python's implementation uses keys instead of function pointers


from typing import Any


class PriorityQueue():
    def __init__(self, comparison_function):
        """
        Initialize the priority queue
        """
        self.lizt = []
        self.comparison_function = comparison_function

    def is_empty(self) -> bool:
        """
        Return True if the priority queue is empty

        Returns:
            bool: True if the priority queue is empty
        """
        return len(self.lizt) == 0

    def pop(self) -> Any:
        """
        Pop (remove and return) the element in the priority queue with the highest priority

        Returns:
            Any: the element in the priority queue with the highest priority
        """
        return self.lizt.pop(0)

    def push(self) -> None:
        pass

    def __sizeof__(self) -> int:
        """
        Return the size of the priority queue

        Returns:
            int: The size of the priority queue
        """
        return len(self.lizt)
