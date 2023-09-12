# reference: https://flask-restx.readthedocs.io/en/latest/example.html
# imports
import os

from bson.objectid import ObjectId
import pandas as pd
from flask import Blueprint, current_app, request
from flask_restx import Namespace, Resource, fields
from training.ebisu.stats import Stats
from utils.json_utils import jsonify
from storage.language_datastores import LANGUAGE_DATASTORE_MAP

# TODO put these term lists elsewhere
POLISH_CORPUS_VOCAB_DF = pd.read_csv("gs://language-training-toolkit-dev-dataproc/polish/form_counts.csv")
CHINESE_CORPUS_VOCAB_DF = pd.read_csv("gs://language-training-toolkit-dev-dataproc/chinese/word_counts.csv")

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
    'language': fields.String(description='The language in which the term exists')
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

        language_datastore_class = LANGUAGE_DATASTORE_MAP[language.lower()]
        language_datastore = language_datastore_class(current_app.ds_client)
        return language_datastore.get_vocabulary_entries(lexeme_id, user_id)[0]

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
            language_datastore_class = LANGUAGE_DATASTORE_MAP[language.lower()]
            language_datastore = language_datastore_class(current_app.ds_client)
            vocab_entries = language_datastore.get_vocabulary_entries(
                lexeme_id=[ObjectId(lexeme_id)], user_id=ObjectId(user_id))

            if vocab_entries:
                vocab_entry = vocab_entries[0]
                return jsonify({
                    "vocabulary_id": vocab_entry['_id'],
                    'stats': vocab_entry['stats'],
                    'user_id': user_id,
                    'lexeme_id': lexeme_id,
                    'language': language
                })
            else:
                stats = {k: (Stats(**request_data['stats'][k])) for k in request_data['stats']}
                vocabulary_id = language_datastore.add_vocabulary_entries(
                    [dict(lexeme_id=ObjectId(lexeme_id), stats=stats, user_id=ObjectId(user_id))])[0]  # TODO check if the stats get loaded properly
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

        assert len(stats) > 0

        try:
            # TODO return to this implementation - it looks like it creates a new vocab entry, but a PUT shouldn't create new data
            language_datastore_class = LANGUAGE_DATASTORE_MAP[language.lower()]
            language_datastore = language_datastore_class(current_app.ds_client)
            lexeme_id = request_data['lexeme_id']
            user_id = request_data['user_id']
            stats = {key: Stats(**stats[key]) for key in stats}
            vocabulary_id = language_datastore.add_vocabulary_entry(
                ObjectId(lexeme_id), stats, ObjectId(user_id))  # TODO check if the stats get loaded properly
            response = jsonify({'vocabulary_id': str(vocabulary_id)})
            return response
        except AssertionError as e:
            return "bad request"

recommendation_fields_get = ns.model('recommendations_get', {
    'user_id': fields.String(description='The ID of the user for whom we want to pull vocabulary recommendations'),
    'language': fields.String(description='The language for which we want to recommend terms')
})

@ns.route('/recommendations')
class Recommendations(Resource):
    @ns.doc(body=recommendation_fields_get)
    def get(self) -> dict:
        """
        Get a set of study facts for recommendation
        """
        # TODO
        request_args = request.args
        language = request_args['language']
        user_id = ObjectId(request_args['user_id'])
        count = 10

        language_datastore_class = LANGUAGE_DATASTORE_MAP[language.lower()]
        language_datastore = language_datastore_class(current_app.ds_client)
        # TODO hardcoding this for now, should generalize the data pulling
        if language == "polish":
            corpus_lemmas = list(POLISH_CORPUS_VOCAB_DF[POLISH_CORPUS_VOCAB_DF['lemma'].notnull()]['lemma']) # this list is sorted in order of word_count
            lexemes = language_datastore.get_lexemes(lemma=corpus_lemmas)
            vocabulary_entries = language_datastore.get_vocabulary_entries(user_id=user_id)
            
            vocabulary_lemmas = list(map(lambda x: x['lexeme'].lemma, vocabulary_entries))
            lemma_map = {lexemes[key].lemma: {'lexeme_id': key, 'lexeme': lexemes[key]} for key in lexemes}
            reccs_tuples = []

            for lemma in corpus_lemmas:
                if lemma in lemma_map and lemma not in vocabulary_lemmas:
                    reccs_tuples.append((str(lemma_map[lemma]['lexeme_id']), lemma_map[lemma]['lexeme'].to_json()))

            return dict(reccs_tuples[:count])

        elif language == "chinese":
            corpus_lemmas = list(CHINESE_CORPUS_VOCAB_DF['word']) # this list is sorted in order of word_count
            lexemes = language_datastore.get_lexemes(lemma=corpus_lemmas)
            vocabulary_entries = language_datastore.get_vocabulary_entries(user_id=user_id)
            
            vocabulary_lemmas = list(map(lambda x: x['lexeme'].lemma, vocabulary_entries))
            lemma_map = {lexemes[key].lemma: {'lexeme_id': key, 'lexeme': lexemes[key]} for key in lexemes}
            reccs_tuples = []

            for lemma in corpus_lemmas:
                if lemma in lemma_map and lemma not in vocabulary_lemmas:
                    reccs_tuples.append((str(lemma_map[lemma]['lexeme_id']), lemma_map[lemma]['lexeme'].to_json()))

            return dict(reccs_tuples[:count])
        else:
            return f"language not supported: {language}"

        # TODO get the list of vocab terms for a user, get the queue of common terms for the language, diff the lists, sort, and return n
        # ...
        return []