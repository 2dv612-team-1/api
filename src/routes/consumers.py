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
            return create_consumer(request.form)
        except AttributeError:
            return response('Wrong credentials', 400)

    if request.method == 'GET':
        try:
            return get_users_with_role('consumer')
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
