# imports
from flask import Blueprint, current_app, request, jsonify
from flask_jwt import jwt_required, current_identity
import os, sys

from storage.language_datastore import LanguageDatastore
from scraping.annotation_utils import annotate_text
from storage.vocabulary_connector import VocabularyConnector

# constants


# Blueprint Setup
bp = Blueprint('annotate', __name__, url_prefix="/annotate")


# 
@bp.route("", methods=['POST'])
@jwt_required()
def annotate():
  request_data = request.get_json()

  try:
    # TODO something about this isn't getting the vocab annotations, not sure why
    id = current_identity.id
    text = request_data['text']
    language = request_data['language']
    
    language_datastore = LanguageDatastore(current_app.ds_client, language)
    
    annotated_text = annotate_text(text, language_datastore, user_id=id, discovery_mode=False)
    response = jsonify({'annotations': annotated_text})

    return response
  except AssertionError as e:
    return "bad request"