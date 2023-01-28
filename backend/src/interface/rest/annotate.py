# imports
import os

from bson.objectid import ObjectId
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from scraping.annotation_utils import annotate_text
from storage.language_datastores.polish_datastore import PolishDatastore

# constants
MONGODB_URI = os.environ['MONGODB_URI']

# interface
bp = Blueprint('annotate', __name__, url_prefix='/annotate')
ns = Namespace('annotate', "Resource for annotating text")

annotation_fields = ns.model('annotation_request', {
    'text': fields.String(description='The text to be annotated'),
    'language': fields.String(description='The password for the said user'),
    'user_id': fields.String(description='The ID of the user for whom we want to manage a vocabulary term'),
})


@ns.route('')
class Annotate(Resource):
    @ns.doc(body=annotation_fields)
    def post(self):
        """
        Create annotations for [text]
        """
        try:
            request_data = request.get_json()
            text = request_data['text']
            language = request_data['language']
            user_id = request_data.get('user_id', None)
            if user_id is not None: user_id = ObjectId(user_id)

            # TODO something about this isn't getting the vocab annotations, not sure why
            # id = current_identity.id
            language_datastore = PolishDatastore(current_app.ds_client, language)
            annotated_text = annotate_text(text, language_datastore, user_id=user_id, discovery_mode=True) # TODO how should we decide if in discovery mode
            response = jsonify({'annotations': annotated_text})
            return response
        except AssertionError as e:
            return "bad request"