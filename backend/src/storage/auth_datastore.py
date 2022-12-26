from bson import ObjectId
from pymongo import MongoClient
from dataclasses import dataclass
from enforce_typing import enforce_types

from storage.datastore_utils import generate_query
from storage.collection_connector import CollectionConnector
from utils.json_utils import JSONSerializable

@enforce_types
@dataclass
class User(JSONSerializable):
    _id: ObjectId
    username: str
    password: str

    def to_json(self) -> dict:
        return {
            'username': self.username,
            'password': self.password,
            '_id': self._id
        }

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
        user_document = self.users_collection.get_document(generate_query(username=username))

        if user_document:
            return User(**user_document)

    def get_user_by_id(self, _id: ObjectId) -> User:
        """
        Get the [User] with the given _id from the datastore

        Args:
            _id (ObjectId): the _id of the user

        Returns:
            User: The user data, if the user exists
        """
        user_document = self.users_collection.get_document(generate_query(_id=_id))

        if user_document:
            return User(**user_document)

    def add_user(self, username: str, password: str) -> ObjectId:
        """
        Create a new user and get the ID of the new user.

        Args:
            username (str)
            password (str)

        Returns:
            ObjectId: the ID of the new user
        """
        return self.users_collection.push_document(
            {'username': username, 'password': password})
