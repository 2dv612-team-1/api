"""
Auth route
"""

from flask import Blueprint, request
from utils.response import response
from dal.auth import auth_and_return_user
import jwt

AUTH = Blueprint('auth', __name__)

# add bcrypt


@AUTH.route('/auth', methods=['POST'])
def auth_actions():
    """Authenticates any user"""

    try:

        found_user = auth_and_return_user(request)

        if found_user:
            payload = {'username': found_user['username'], 'role': found_user['role']}
            encoded = jwt.encode(payload, 'super-secret')

            return response('Successfully logged in as ' + found_user['role'],
                            200,
                            {'token': encoded.decode('utf-8')})
        else:
            raise AttributeError()
    except AttributeError:
        return response('Wrong credentials', 400)
