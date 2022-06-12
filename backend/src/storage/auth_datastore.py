from bson import ObjectId
from pymongo import MongoClient
from storage.collection_connector import CollectionConnector


class User(object):
  def __init__(self, _id: ObjectId, username: str, password: str):
      self.id = str(_id)
      self.username = username
      self.password = password


class AuthDatastore(object):
  """
  A datastore interafce for dealing with auth
  """
  def __init__(self, datastore_client: MongoClient):
    """ A connector that handles interaction with a language, as it exists in the datastore

    Args:
        datastore_client (MongoClient): the MongoDB client used to interact with the datastore
        language (str): the language that we're dealing with
    """
    self.users_collection = CollectionConnector(datastore_client, "auth", "users")

  def get_user_by_username(self, username: str) -> User:
    """
    Get the [User] with the given username from the datastore

    Args:
        username (str): the username of the user

    Returns:
        User: The user data, if the user exists
    """
    user_document = self.users_collection.get_document({'username': username})
    
    if user_document:
      return User(**user_document)

  def get_user_by_id(self, id: str) -> User:
    """
    Get the [User] with the given id from the datastore

    Args:
        id (str): the id of the user

    Returns:
        User: The user data, if the user exists
    """
    user_document = self.users_collection.get_document({'_id': ObjectId(id)})
    
    if user_document:
      return User(**user_document)

  def add_user(self, username: str, password: str) -> str:
    """
    Create a new user and get the ID of the new user.

    Args:
        username (str)
        password (str)

    Returns:
        str: the ID of the new user
    """
    return str (self.users_collection.push_document(
      {'username': username, 'password': password}))