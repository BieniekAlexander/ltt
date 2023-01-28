# reference: https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
# TODO I guess JWT stuff isn't very secure, probably change this in the future
import os

from flask import Blueprint, current_app, jsonify, make_response, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_restx import Namespace, Resource, fields

# constants
MONGODB_URI = os.environ['MONGODB_URI']

# Flask JWT Integration


def authenticate(username, password):
    """
    Helper function to authenticate the basic auth against the datastore
    """
    user = current_app.auth_datastore.get_user_by_username(username)
    if user.password.encode('utf-8') == password.encode('utf-8'):
        return user


def init_flask_jwt(app):
    """
    Helper function to initialize JWT
    """
    current_app.config['SECRET_KEY'] = 'super-secret'
    jwt = JWTManager(app)


# interface
bp = Blueprint('auth', __name__, url_prefix='/auth')
ns = Namespace('auth', "Resource for handling logins")

user_fields = ns.model('user', {
    'username': fields.String(description='The ID of the user for whom we want to manage a vocabulary term'),
    'password': fields.String(description='The password for the said user'),
})


@ns.route('/login')
class Login(Resource):
    @ns.doc(body=user_fields)
    def post(self):
        """
        Create a user
        """
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']

        user = authenticate(username, password)
        print(user)

        if not user:
            return "Bad username and password combination", 401
        else:
            user_data = user.to_json()
            token_data = {
                'user_id': str(user_data['_id']),
                'username': user_data['username']
            }
            access_token = create_access_token(token_data)
            return {"access_token": access_token}


@ns.route('/register')
class Register(Resource):
    @ns.doc(body=user_fields)
    def post(self):
        """
        Create a user session, and get the login token for the user session
        """
        request_data = request.get_json()
        username = request_data['username']
        password = request_data['password']

        if current_app.auth_datastore.get_user_by_username(username):
            return "username already exists", 500
        else:
            return current_app.auth_datastore.add_user(username, password)
