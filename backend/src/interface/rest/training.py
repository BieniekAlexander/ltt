# imports
import os

from bson.objectid import ObjectId
from flask import Blueprint, current_app, request
from flask_restx import Namespace, Resource, fields
from interface.rest.vocabulary import entry_fields_put
from training.sm2_anki.training_session import get_study_entries, put_studied_entries
from utils.json_utils import jsonify
from training.sm2_anki.recall import Recall
from training.sm2_anki.stats import Stats

# constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"

# interface
bp = Blueprint('training', __name__, url_prefix="/training")
ns = Namespace(
    'training', "A resource used for managing a user's training session")

training_fields_get_parser = (
    ns.parser()
    .add_argument('user_id', type=str, help='The ID of the user for whom we want to pull a vocabulary term')
    .add_argument('language', type=str, help='The language in which the term exists')
    .add_argument('count', type=int, help='The number of terms to get for studying')
    .add_argument('fact', type=int, help="The fact that we're studying")
)

training_fields_put = ns.model('terms_put', {
    'user_id': fields.String(description="The user for whom we are updating terms"),
    'language': fields.String(description="The language being studied"),
    'entries': fields.List(
        fields.Raw(description="a study term"),
        description="The study terms to update")
})


@ns.route('/study_set')
class StudySet(Resource):
    """
    Manage training sessions
    """
    @ns.expect(training_fields_get_parser)
    @ns.marshal_list_with(training_fields_put)
    def get(self):
        """
        Get a set of vocabulary terms as a training session
        """
        request_data = request.args.to_dict()
        user_id = ObjectId(request_data['user_id'])
        language = request_data['language']
        fact = request_data['fact']
        count = int(request_data['count'])

        study_entries = get_study_entries(
            user_id=user_id,
            language=language,
            count=count,
            fact=fact,
            datastore_client=current_app.ds_client)

        return {
            'user_id': user_id,
            'language': language,
            'entries': list(map(jsonify, study_entries))
        }

    @ns.doc(body=training_fields_put)
    def put(self):
        """
        Update a set of vocabulary study term stats
        TODO this endpoint redundantly requires language and user_id
        """
        request_data = request.get_json()
        user_id = request_data['user_id']
        language = request_data['language']
        fact = request_data['fact']
        entries = request_data['entries']

        try:
            for entry in entries:
                entry['stats'] = {item: Stats(**entry['stats'][item]) for item in entry['stats']}

            put_studied_entries(user_id, language, current_app.ds_client, fact, entries)
        except Exception as e:
            print(str(e))
