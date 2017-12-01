"""
Consumers
"""

from flask import Blueprint, request
from utils.response import response

from dal.users import get_users_with_role, check_user_token
from dal.consumer import create_consumer

CONSUMERS = Blueprint('consumers', __name__)


# add bcrypt


@CONSUMERS.route('/consumers', methods=['GET', 'POST'])
def user_actions():
    """Creates user"""

    if request.method == 'POST':
        try:
            consumer_exist = create_consumer(request.form)

            if consumer_exist:
                return response('User already exists', 409)
            else:
                return response('User was created', 201)

        except AttributeError:
            return response('Wrong credentials', 400)

    if request.method == 'GET':
        try:

            users = get_users_with_role('consumer')
            return response('Successfully extracted all users', 200, {'users': users})

        except SystemError:
            return response('Something went wrong while retreiving the data', 500)


@CONSUMERS.route('/consumers/<token>', methods=['GET'])
def get_user(token):
    """Gets current user"""

    try:

        username = check_user_token(token)
        return response('Successfully gather user data', 200, {'data': username})

    except AttributeError:
        return response('Wrong credentials', 400)
