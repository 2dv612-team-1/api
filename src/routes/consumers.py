"""
Consumers
"""

from flask import Blueprint, request
from utils.response import response
from utils.string import *
from dal.users import get_users_with_role, check_user_token
from dal.consumer import create_consumer

CONSUMERS_ROUTER = Blueprint(CONSUMERS, __name__)


# add bcrypt


@CONSUMERS_ROUTER.route('/consumers')
def get_consumers():
    try:

        users = get_users_with_role(CONSUMER)
        return response('Successfully extracted all users', 200, {USERS: users})

    except SystemError:
        return response('Something went wrong while retreiving the data', 500)


@CONSUMERS_ROUTER.route('/consumers', methods=['POST'])
def consumer_creation():
    """Creates consumer"""

    try:
        consumer_exist = create_consumer(request.form)

        if consumer_exist:
            return response('User already exists', 409)
        else:
            return response('User was created', 201)

    except AttributeError:
        return response('Wrong credentials', 400)


@CONSUMERS_ROUTER.route('/consumers/<token>', methods=['GET'])
def get_user(token):
    """Gets current user"""

    try:
        username = check_user_token(token)
        return response('Successfully gather user data', 200, {DATA: username})

    except AttributeError:
        return response('Wrong credentials', 400)
