# imports
import pymongo, logging
from bson.objectid import ObjectId

from storage.storage_errors import StorageConnectionError

# constants


class DatastoreClient(object):
  """
  An interface that lets us connect to a document store 
  """
  def __init__(self, uri: str):
    """
    Establish an initial connection to the document store
    """
    self.client = pymongo.MongoClient(uri)
    self.db = self.client.admin

    if self.db.command("serverStatus"):
      logging.debug("Connected to mongodb and got server status")
    else:
      raise StorageConnectionError()