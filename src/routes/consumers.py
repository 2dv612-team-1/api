"""
Consumers
"""

from flask import Blueprint, request
from utils.response import response
from dal.users import get_users_with_role, find_user_by_name
from dal.consumer import create_consumer
import jwt

CONSUMERS = Blueprint('consumers', __name__)


# add bcrypt


@CONSUMERS.route('/consumers', methods=['GET', 'POST'])
def user_actions():
    """Creates user"""

    if request.method == 'POST':
        form = request.form

        try:
            username = form['username']
            password = form['password']

            user_exists = create_consumer(username, password)

            if user_exists:
                return response('User already exists', 409)
            else:
                return response('User was created', 201)
        except AttributeError:
            return response('Wrong credentials', 400)

    if request.method == 'GET':
        try:

            _users = get_users_with_role('consumer')

            return response(
                'Successfully extracted all users', 200,
                {'users': _users}
            )
        except SystemError:
            return response('Something went wrong while retreiving the data', 500)


@CONSUMERS.route('/consumers/<token>', methods=['GET'])
def get_user(token):
    """Gets current user"""

    try:
        payload = jwt.decode(token, 'super-secret')
        username = payload.get('username')

        found_user = find_user_by_name(username)

        if found_user:
            return response(
                'Successfully gather user data', 200,
                {'data': found_user['username']}
            )
        else:
            raise AttributeError()
    except AttributeError:
        return response('Wrong credentials', 400)
