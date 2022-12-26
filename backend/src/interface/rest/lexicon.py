# imports
import os

from flask import Blueprint, request
from pymongo import MongoClient
from storage.language_datastores.polish_datastore import PolishDatastore

# constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"

# objects
db_client = MongoClient(MONGODB_URI)
polish_datastore = PolishDatastore(db_client, LANGUAGE)

# interface
bp = Blueprint('lexicon', __name__, url_prefix="/lexicon")


@bp.route("", methods=['GET'])
def lexicon():
    """
    TODO this seems not implemented
    """
    request_data = request.get_json()

    try:
        lexeme = polish_datastore.get_lexemes_from_form(**request_data)
        return lexeme
    except AssertionError as e:
        return "bad request"
