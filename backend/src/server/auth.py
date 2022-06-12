# # https://pythonhosted.org/Flask-JWT/
import os
from flask import Blueprint, Flask, request, current_app
from flask_jwt import JWT, jwt_required, current_identity
from mongomock import ObjectId
from pymongo import MongoClient


# JWT Functions
def authenticate(username, password):
  user = current_app.auth_datastore.get_user_by_username(username)
  if user.password.encode('utf-8') == password.encode('utf-8'):
    return user

def identity(payload):
  id = payload['identity']
  return current_app.auth_datastore.get_user_by_id(id)


# Auth Blueprint
bp = Blueprint('auth', __name__)

@bp.route('/auth/register', methods=['POST'])
def register():
  request_data = request.get_json()

  username = request_data['username']
  password = request_data['password']

  if current_app.auth_datastore.get_user_by_username(username):
    return "username already exists", 500
  else:
    return current_app.auth_datastore.add_user(username, password)

@bp.route('/vocab/size', methods=['GET'])
@jwt_required()
def vocab_size():
  id = current_identity.id
  return id