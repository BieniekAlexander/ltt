# imports
from flask import Flask, request

from storage.lexicon_connector import LexiconConnector
from storage.language_datastore import LanguageDatastore
from scraping.annotation_utils import annotate_text


# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "polish"


# objects
lexicon_connector = LexiconConnector(MONGODB_URL, LANGUAGE)
language_datastore = LanguageDatastore(MONGODB_URL, "polish")


# Flask App
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/lexicon")
def lexicon():
    request_data = request.get_json()

    try:
        _, lexeme = lexicon_connector.get_lexeme_dictionary_mapping(**request_data)
        return lexeme
    except AssertionError as e:
        return "bad request"


@app.route("/vocabulary")
def vocabulary():
    request_data = request.get_json()

    try:
        _, lexeme = lexicon_connector.get_lexeme_dictionary_mapping(**request_data)
        return lexeme
    except AssertionError as e:
        return "bad request"


@app.route("/annotate")
def annotate():
    request_data = request.get_json()

    try:
        text = request_data['text']
        annotated_text = annotate_text(text, language_datastore, vocabulary_connector=None, discovery_mode=False)
        return {'annotations': annotated_text}
    except AssertionError as e:
        return "bad request"


annotate_text