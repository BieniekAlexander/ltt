# imports
from flask import Blueprint, request
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.language_datastore import LanguageDatastore
from scraping.annotation_utils import annotate_text

# constants
MONGODB_URL = "mongodb://localhost:27017/"
LANGUAGE = "polish"

# objects
language_datastore = LanguageDatastore(MONGODB_URL, LANGUAGE)

# interface
bp = Blueprint('annotate', __name__,url_prefix="/annotate")


@bp.route("")
def annotate():
    request_data = request.get_json()

    try:
        text = request_data['text']
        annotated_text = annotate_text(text, language_datastore, vocabulary_connector=None, discovery_mode=False)
        return {'annotations': annotated_text}
    except AssertionError as e:
        return "bad request"