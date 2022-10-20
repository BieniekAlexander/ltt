# imports
import os

from flask import Flask, current_app, jsonify, request
from flask_cors import CORS, cross_origin
from flask_restx import Api
from interface.rest import annotate, auth, lexicon, test, training, vocabulary
from interface.rest.auth import init_flask_jwt
from pymongo import MongoClient
from scraping.annotation_utils import annotate_text
from storage.auth_datastore import AuthDatastore
from storage.language_datastore import LanguageDatastore
from training.sm2.stats import Stats

# Constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"
USER_ID = "a"*24


# Flask Setup
api = Api(title="Language Training Toolkit API")
app = Flask(__name__)
api.init_app(app)

# Add namespaces
api.add_namespace(test.ns)
api.add_namespace(auth.ns)
api.add_namespace(vocabulary.ns)
api.add_namespace(training.ns)
api.add_namespace(annotate.ns)
# api.add_namespace(lexicon.ns)

with app.app_context():
    # Datastore Connectivity
    current_app.ds_client = MongoClient(MONGODB_URI)
    current_app.auth_datastore = AuthDatastore(current_app.ds_client)

    # JWT Authorization
    init_flask_jwt(current_app)

CORS(app, resources={r'/*': {'origins': '*'}})


# Additional Endpoints
# @jwt_required()
