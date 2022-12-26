# reference: https://flask-restx.readthedocs.io/en/latest/example.html
# imports
import os

from bson.objectid import ObjectId
from flask import Blueprint, current_app, request
from flask_restx import Namespace, Resource, fields
from pymongo import MongoClient
from storage.language_datastores.polish_datastore import PolishDatastore
from training.sm2_anki.stats import Stats
from utils.json_utils import jsonify

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
    'ste': fields.Integer(description="The step towards graduation of the term to review mode"),
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
    'stats': fields.Nested(fields.Nested(stats_fields, description="data for studying the term"), description="A map of study stat entries, for each aspect of studying the term")
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

        language_datastore = PolishDatastore(current_app.ds_client, language)
        return language_datastore.get_vocabulary_entry(lexeme_id, user_id)

    @ns.doc(body=entry_fields_put)
    def post(self):
        """
        Post a new vocabulary entry for a given user, term, and language (or return the existing one if it already exists)
        """
        request_data = request.get_json()
        language = request_data['language']
        user_id = request_data['user_id']
        lexeme_id = request_data['lexeme_id']

        try:
            language_datastore = PolishDatastore(
                current_app.ds_client, language)
            vocab_entry = language_datastore.get_vocabulary_entry(
                lexeme_id, ObjectId(user_id))

            if vocab_entry:
                return jsonify({
                    "vocabulary_id": vocab_entry['_id'],
                    'stats': vocab_entry['stats'],
                    'user_id': user_id,
                    'lexeme_id': lexeme_id,
                    'language': language
                })
            else:
                stats = {k: (Stats(**request_data['stats'][k])) for k in request_data['stats']} if 'stats' in request_data else {'definition': Stats()}
                vocabulary_id = language_datastore.add_vocabulary_entry(
                    ObjectId(lexeme_id), stats, ObjectId(user_id))  # TODO check if the stats get loaded properly
                ret = jsonify({
                    'vocabulary_id': str(vocabulary_id),
                    'stats': jsonify(stats),
                    'user_id': user_id,
                    'lexeme_id': lexeme_id,
                    'language': language
                })

                return ret
        except Exception as e:
            print(f"error - {str(e)}")
            return "", 500

    @ns.doc(body=entry_fields_put)
    def put(self, user_id: str, lexeme_id: str, language: str, stats: list):
        """
        Update the given term with new stats
        """
        request_data = request.get_json()
        language = request_data['language']
        user_id = request_data['user_id']
        lexeme_id = request_data['lexeme_id']
        stats = request_data['stats']

        try:
            language_datastore = PolishDatastore(
                current_app.ds_client, language)
            lexeme_id = request_data['lexeme_id']
            user_id = request_data['user_id']
            stats = {key: Stats(**stats[key]) for key in stats}
            vocabulary_id = language_datastore.add_vocabulary_entry(
                ObjectId(lexeme_id), stats, ObjectId(user_id))  # TODO check if the stats get loaded properly
            response = jsonify({'vocabulary_id': str(vocabulary_id)})
            return response
        except AssertionError as e:
            return "bad request"
