# imports
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from storage.lexicon_connector import LexiconConnector
from storage.language_datastore import LanguageDatastore
from scraping.annotation_utils import annotate_text
from storage.vocabulary_connector import VocabularyConnector
from server import lexicon

# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "polish"
USER_ID = "a"*24

# objects 
language_datastore = LanguageDatastore(MONGODB_URL, LANGUAGE)
vocabulary_connector = VocabularyConnector(MONGODB_URL, LANGUAGE, USER_ID)

# Flask
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
# app.register_blueprint(lexicon.bp) TODO Flask blueprints aren't working with CORS


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/annotate", methods=['POST'])
@cross_origin()
def annotate():
    request_data = request.get_json()

    try:
        text = request_data['text']
        language = request_data['language']
        annotated_text = annotate_text(text, language_datastore, vocabulary_connector=vocabulary_connector, discovery_mode=False)
        response = jsonify({'annotations': annotated_text})

        return response
    except AssertionError as e:
        return "bad request"

@app.route("/vocabulary/addTerm", methods=['POST'])
@cross_origin()
def addTerm():
    request_data = request.get_json()
    print(request_data)

    try:
        lexeme_id = request_data['lexeme_id']
        user_id = request_data['user_id']
        rating = 1.0
        vocabulary_id = vocabulary_connector.push_vocabulary_entry(lexeme_id, rating, user_id)
        response = jsonify({'vocabulary_id': str(vocabulary_id)})

        return response
    except AssertionError as e:
        return "bad request"