class StorageError(Exception):
    """
    Base class for exceptions related to Datastore interface

    Attributes:
      message: the message held by the exception
    """


class StorageConnectionError(StorageError):
    """
    Exception raised when we hit connection issues with our Datastore

    Attributes:
        message: the message held by the exception
    """

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = f"Failed to connect to Datastore"

        super().__init__(self.message)
