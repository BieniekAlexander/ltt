# imports
import os

from flask import Blueprint, request
from pymongo import MongoClient
from storage.lexicon_connector import LexiconConnector

# constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"

# objects
db_client = MongoClient(MONGODB_URI)
lexicon_connector = LexiconConnector(db_client, LANGUAGE)

# interface
bp = Blueprint('lexicon', __name__,url_prefix="/lexicon")


@bp.route("", methods=['GET'])
def lexicon():
    request_data = request.get_json()

    try:
        lexeme = lexicon_connector.get_lexeme_entry(**request_data)
        return lexeme
    except AssertionError as e:
        return "bad request"