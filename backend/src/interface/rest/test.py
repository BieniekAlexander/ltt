# imports
import os
import time

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

# constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"

# interface
bp = Blueprint('test', __name__, url_prefix="/test")
ns = Namespace('test', 'A namespace for testing REST interface functionality')


@ns.route("/sleep/<duration>")
class Sleep(Resource):
    @ns.doc(params={'duration': 'The duration to wait, in seconds'})
    def get(self, duration):
        """
        Sleep test endpoint - will wait for [duration] seconds
        """
        duration = int(duration)
        time.sleep(duration)
        return f"Slept for {duration} seconds"


@ns.route("/auth")
class Auth(Resource):
    @jwt_required(optional=(os.environ.get("JWT_AUTH_OPTIONAL").lower()=="true"))
    def get(self):
        """
        Auth test endpoint - reqiures JWT token authorization, will return dummy data
        """
        try:
            return "hehe dummy data"
        except Exception as e:
            return str(e)