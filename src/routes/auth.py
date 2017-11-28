"""
Auth route
"""

from flask import Blueprint, request
from utils.response import response
from utils.dal import SuperDAL
import jwt

super_dal = SuperDAL()
AUTH = Blueprint('auth', __name__)

# add bcrypt


@AUTH.route('/auth', methods=['POST'])
def auth_actions():
    """Authenticates any user"""

    try:
        username = request.form['username']
        password = request.form['password']

        found_user = super_dal.auth_and_return_user(username, password)

        if found_user:
            payload = {'username': username, 'role': found_user['role']}
            encoded = jwt.encode(payload, 'super-secret')

            return response('Successfully logged in as ' + found_user['role'],
                            200,
                            {'token': encoded.decode('utf-8')})
        else:
            raise AttributeError()
    except AttributeError:
        return response('Wrong credentials', 400)
