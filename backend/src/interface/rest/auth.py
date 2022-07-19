# # https://pythonhosted.org/Flask-JWT/
from flask import Blueprint, request, current_app
from flask_jwt import jwt_required, current_identity


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