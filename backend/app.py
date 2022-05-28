# imports
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from storage.datastore_client import DatastoreClient
from storage.language_datastore import LanguageDatastore
from scraping.annotation_utils import annotate_text
from server import lexicon

# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "polish"
USER_ID = "a"*24

# objects 
ds_client = DatastoreClient(MONGODB_URL)
language_datastore = LanguageDatastore(ds_client, LANGUAGE)

# Flask
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.register_blueprint(lexicon.bp) # TODO Flask blueprints aren't working with CORS


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

# @cross_origin TODO this isn't doing anything?
@app.route("/annotate", methods=['POST'])
def annotate():
    request_data = request.get_json()

    try:
        text = request_data['text']
        language = request_data['language']
        annotated_text = annotate_text(text, language_datastore, user_id=USER_ID, discovery_mode=False)
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
        rating = 1.0
        vocabulary_id = language_datastore.add_vocabulary_entry(lexeme_id, rating, user_id)
        response = jsonify({'vocabulary_id': str(vocabulary_id)})

        return response
    except AssertionError as e:
        return "bad request"
