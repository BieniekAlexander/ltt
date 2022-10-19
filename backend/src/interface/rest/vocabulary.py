# reference: https://flask-restx.readthedocs.io/en/latest/example.html
# imports
import os

from flask import Blueprint, current_app, jsonify, request
from flask_restx import Namespace, Resource, fields
from pymongo import MongoClient
from storage.language_datastore import LanguageDatastore
from training.sm2.stats import Stats

# constants
MONGODB_URI = os.environ['MONGODB_URI']

# interface
bp = Blueprint('vocabulary', __name__, url_prefix='/vocabulary')
ns = Namespace(
    'vocabulary', "Resource for a user's persisted vocabulary terms")

stats_fields = ns.model('stats', {
    'repetition': fields.Integer(description='The number of times that the user has studied the term'),
    'ef': fields.Float(description='The easiness factor for the user'),
    'interval': fields.Integer(description='The number of sessions until which a user should study the term again'),
    # 'recall': fields.Integer(description="the user's ability to recall the entry during a study session") # TODO this is handled only in study sessions, not relevant here
})

entry_fields_get = ns.model('vocabulary_get', {
    'user_id': fields.String(description='The ID of the user for whom we want to pull a vocabulary term'),
    'lexeme_id': fields.String(description='The ID of the term to manage'),
    'language': fields.String(description='The language in which the term exists'),

})

entry_fields_put = ns.model('vocabulary_put', {
    'user_id': fields.String(description='The ID of the user for whom we want to pull a vocabulary term'),
    'lexeme_id': fields.String(description='The ID of the term to manage'),
    'language': fields.String(description='The language in which the term exists'),
    'stats': fields.Nested(stats_fields, description="The study stats of the term")
})


@ns.route('')
class Entries(Resource):
    """
    Get, put, post, and delete vocabulary entries
    """
#   @ns.expect(get_parser, validate=False)
#   def get(self) -> list:
#     """
#     Get a list of vocabulary entries, given some criteria
#     TODO not implemented
#     """
#     return []
    @ns.doc(body=entry_fields_get)
    def get(self) -> dict:
        """
        Get a vocabulary entry, given its unique identifiers
        """
        request_data = request.get_json()
        language = request_data['language']
        user_id = request_data['user_id']
        lexeme_id = request_data['lexeme_id']

        language_datastore = LanguageDatastore(current_app.ds_client, language)
        return language_datastore.get_vocabulary_entry(lexeme_id, user_id)

    @ns.doc(body=entry_fields_put)
    def post(self):
        """
        Post a new vocabulary entry for a given user, term, and language
        """
        request_data = request.get_json()
        language = request_data['language']
        user_id = request_data['user_id']
        lexeme_id = request_data['lexeme_id']

        try:
            language_datastore = LanguageDatastore(
                current_app.ds_client, language)
            vocab_entry = language_datastore.get_vocabulary_entry(
                lexeme_id, user_id)
            print(vocab_entry)
            return
            lexeme_id = request_data['lexeme_id']
            user_id = request_data['user_id']
            stats = Stats(request_data['stats'])
            vocabulary_id = language_datastore.add_vocabulary_entry(
                lexeme_id, stats, user_id)  # TODO check if the stats get loaded properly
            response = jsonify({'vocabulary_id': str(vocabulary_id)})
            return response
        except AssertionError as e:
            return "bad request"

    @ns.doc(body=entry_fields_put)
    def put(self, user_id, lexeme_id, language, stats):
        """
        Update the given term with new stats
        """
        request_data = request.get_json()
        language = request_data['language']
        user_id = request_data['user_id']
        lexeme_id = request_data['lexeme_id']
        stats = request_data['stats']

        try:
            language_datastore = LanguageDatastore(
                current_app.ds_client, language)
            lexeme_id = request_data['lexeme_id']
            user_id = request_data['user_id']
            stats = Stats(request_data['stats'])
            vocabulary_id = language_datastore.add_vocabulary_entry(
                lexeme_id, stats, user_id)  # TODO check if the stats get loaded properly
            response = jsonify({'vocabulary_id': str(vocabulary_id)})
            return response
        except AssertionError as e:
            return "bad request"
