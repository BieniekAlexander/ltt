# imports
import os

from flask import Blueprint, request
from pymongo import MongoClient
from flask_restx import Namespace, Resource, fields
from storage.language_datastores import LANGUAGE_DATASTORE_MAP

# constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"
DS_CLIENT = MongoClient(MONGODB_URI)

# interface
bp = Blueprint('lexicon', __name__, url_prefix="/lexicon")
ns = Namespace(
    'lexicon', "A resource used for collecting language data")

lexeme_fields_get_parser = (
    ns.parser()
    .add_argument('language', type=str, help='The language in which the term exists')
    .add_argument('form', type=str, help='A form of the lexeme to find')
)


@ns.route('/lexeme')
class Lexeme(Resource):
    """
    Get a lexeme
    """
    @ns.expect(lexeme_fields_get_parser)
    def get(self):
        """
        Get a lexeme, given a form
        """
        
        language = request.args['language']
        form = request.args['form']

        language_datastore = LANGUAGE_DATASTORE_MAP[language](DS_CLIENT)
        lexemes = language_datastore.get_lexemes_from_form(form)

        return {
            'lexeme': lexemes[0].to_json()
        }