# # imports
# from flask import Blueprint, request, jsonify
# from flask_cors import cross_origin, CORS
# import os, sys

# from storage.language_datastore import LanguageDatastore
# from scraping.annotation_utils import annotate_text

# # constants
# MONGODB_URI = os.environ['MONGODB_URI']
# LANGUAGE = "polish"

# # objects
# language_datastore = LanguageDatastore(MONGODB_URI, LANGUAGE)

# # interface
# # bp = Blueprint('annotate', __name__, url_prefix="/annotate")
# # CORS(bp)

# # @bp.route("", methods=['POST'])
# # @cross_origin()
# # def annotate():
# #     print("hihihihi")
# #     request_data = request.get_json()

# #     try:
# #         text = request_data['text']
# #         language = request_data['language']
# #         annotated_text = annotate_text(text, language_datastore, vocabulary_connector=None, discovery_mode=False)
# #         response = jsonify({'annotations': annotated_text})

# #         # temp
# #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
# #         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
# #         response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
# #         response.headers.add('Access-Control-Allow-Credentials', 'true')

# #         return response
# #     except AssertionError as e:
# #         return "bad request"