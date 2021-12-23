# imports
from flask import Blueprint, request
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.lexicon_connector import LexiconConnector

# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "polish"

# objects
lexicon_connector = LexiconConnector(MONGODB_URL, LANGUAGE)

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