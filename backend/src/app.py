# imports
import os
from flask import Flask, request, jsonify, current_app
from flask_jwt import JWT, jwt_required
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

from storage.language_datastore import LanguageDatastore
from storage.auth_datastore import AuthDatastore
from scraping.annotation_utils import annotate_text
from training.sm2.stats import Stats
from server import lexicon, auth, annotate
from server.auth import authenticate, identity

# Constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"
USER_ID = "a"*24


# Flask Setup 
app = Flask(__name__)

with app.app_context():
    # Datastore Connectivity
    current_app.ds_client = MongoClient(MONGODB_URI)
    current_app.auth_datastore = AuthDatastore(current_app.ds_client)

    # JWT Authorization
    current_app.config['SECRET_KEY'] = 'super-secret'
    jwt = JWT(current_app, authenticate, identity)

CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(lexicon.bp) # TODO Flask blueprints aren't working with CORS
app.register_blueprint(auth.bp)
app.register_blueprint(annotate.bp)


# Additional Endpoints
@app.route("/", methods=['GET'])
@jwt_required()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/vocabulary/addTerm", methods=['POST'])
@jwt_required()
def addTerm():
    request_data = request.get_json()
    print(request_data)

    try:
        # TODO which language does this request relate to?
        # TODO I literally only deal with Polish right now, but I can't instantiate on a constant language if I'm gonna support more languages
        language_datastore = LanguageDatastore(current_app.ds_client, LANGUAGE)
        lexeme_id = request_data['lexeme_id']
        user_id = request_data['user_id']
        stats = Stats()
        vocabulary_id = current_app.add_vocabulary_entry(lexeme_id, stats, user_id) # TODO check if the stats get loaded properly
        response = jsonify({'vocabulary_id': str(vocabulary_id)})

        return response
    except AssertionError as e:
        return "bad request"

print(app.url_map)