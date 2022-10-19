# imports
import os

from flask import Blueprint, current_app, request
from flask_restx import Namespace, Resource, fields
from interface.rest.vocabulary import entry_fields_put
from training.training_session import get_study_entries, put_studied_entries

# constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"

# interface
bp = Blueprint('training', __name__, url_prefix="/training")
ns = Namespace(
    'training', "A resource used for managing a user's training session")

training_fields_get = ns.model('terms_get', {
    'user_id': fields.String(description='The ID of the user for whom we want to pull a vocabulary term'),
    'language': fields.String(description='The language in which the term exists'),
    'count': fields.Integer(description="The number of terms to get for studying")
})

training_fields_put = ns.model('terms_put', {
    'user_id': fields.String(description="The user for whom we are updating terms"),
    'language': fields.String(description="The language being studied"),
    'entries': fields.List(
        fields.Nested(entry_fields_put, description="The study terms to update"),
                      description="boop")
})

@ns.route('')
class StudySet(Resource):
  """
  Manage training sessions
  """
  @ns.doc(body=training_fields_get)
  @ns.marshal_list_with(entry_fields_put)
  def get(self):
    """
    Get a set of vocabulary terms as a training session
    """
    request_data = request.get_json()
    user_id = request_data['user_id']
    language = request_data['language']
    count = request_data['count']

    get_study_entries(user_id, language, count=count)

  @ns.doc(body=training_fields_put)
  def put(self):
    """
    Update a set of vocabulary study term stats
    TODO this endpoint redundantly requiers language and user_id
    """
    request_data = request.get_json()
    user_id = request_data['user_id']
    language = request_data['language']
    entries = request_data['entries']

    put_studied_entries(user_id, language, current_app.ds_client, entries)
