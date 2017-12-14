"""
Response
"""

from flask import jsonify
from utils.string import *

def response(message, status, rest={}):
    """Takes a message and status and applies remaining dicts"""

    default = {
        MESSAGE: message,
        STATUS: status
    }
    default.update(rest)
    return jsonify(default), status
