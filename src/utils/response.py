"""
Response
"""

from flask import jsonify


def response(message, status, rest={}):
    """Takes a message and status and applies remaining dicts"""

    default = {
        'message': message,
        'status': status
    }
    default.update(rest)
    return jsonify(default), status
