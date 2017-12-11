"""
Auth route
"""

from flask import Blueprint, request
from utils.response import response
from utils.string import *
from dal.users import auth_and_return_user

AUTH = Blueprint('auth', __name__)

# add bcrypt


@AUTH.route('/auth', methods=['POST'])
def auth_actions():
    """Authenticates any user"""

    try:
        encoded_data, role = auth_and_return_user(request.form)
        return response('Successfully logged in as ' + role, 200, {TOKEN: encoded_data.decode('utf-8')})

    except AttributeError:
        return response('Wrong credentials', 400)
