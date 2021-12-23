# imports
from flask import Flask, request

from storage.lexicon_connector import LexiconConnector
from storage.language_datastore import LanguageDatastore
from scraping.annotation_utils import annotate_text

from server import lexicon

# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "polish"

# objects

language_datastore = LanguageDatastore(MONGODB_URL, "polish")


# Flask
app = Flask(__name__)
app.register_blueprint(lexicon.bp)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


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