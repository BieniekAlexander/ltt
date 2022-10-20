# imports
import os
import time

from flask import Blueprint, request
from flask_restx import Namespace, Resource

# constants
MONGODB_URI = os.environ['MONGODB_URI']
LANGUAGE = "polish"

# interface
bp = Blueprint('test', __name__, url_prefix="/test")
ns = Namespace('test', 'A namespace for testing REST interface functionality')


@ns.route("/wait/<duration>")
class Wait(Resource):
    @ns.doc(params={'duration': 'The duration to wait, in seconds'})
    def get(self, duration):
        """
        Test endpoint - will wait for [duration] seconds
        """
        duration = int(duration)
        time.sleep(duration)
        return f"waited for {duration} seconds"
