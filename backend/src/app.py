# imports
import os
from flask import Flask, request, jsonify, current_app
from flask_jwt import JWT
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

from storage.language_datastore import LanguageDatastore
from storage.auth_datastore import AuthDatastore
from scraping.annotation_utils import annotate_text
from training.sm2.stats import Stats
from server import lexicon, auth
from server.auth import authenticate, identity

# constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"
USER_ID = "a"*24

# Flask
app = Flask(__name__)
with app.app_context():
    # Datastore Connectivity
    ds_client = MongoClient(MONGODB_URI)
    current_app.auth_datastore = AuthDatastore(ds_client)
    current_app.language_datastore = LanguageDatastore(ds_client, LANGUAGE)
    # TODO I literally only deal with Polish right now, but I can't instantiate on a constant language if I'm gonna support more languages
    
    # JWT Authorization
    current_app.config['SECRET_KEY'] = 'super-secret'
    jwt = JWT(current_app, authenticate, identity)


CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(lexicon.bp) # TODO Flask blueprints aren't working with CORS
app.register_blueprint(auth.bp)

# @cross_origin TODO this isn't doing anything?
@app.route("/annotate", methods=['POST'])
def annotate():
    request_data = request.get_json()

    try:
        text = request_data['text']
        language = request_data['language']
        annotated_text = annotate_text(text, current_app.language_datastore, user_id=USER_ID, discovery_mode=False)
        response = jsonify({'annotations': annotated_text})

        return response
    except AssertionError as e:
        return "bad request"


@app.route("/vocabulary/addTerm", methods=['POST'])
def addTerm():
    request_data = request.get_json()
    print(request_data)

    try:
        lexeme_id = request_data['lexeme_id']
        user_id = request_data['user_id']
        stats = Stats()
        vocabulary_id = current_app.language_datastore.add_vocabulary_entry(lexeme_id, stats, user_id) # TODO check if the stats get loaded properly
        response = jsonify({'vocabulary_id': str(vocabulary_id)})

        return response
    except AssertionError as e:
        return "bad request"
