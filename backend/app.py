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


# Flask
app = Flask(__name__)
app.register_blueprint(lexicon.bp)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"