"""
Consumers
"""

from flask import Blueprint, request
from utils.response import response
from utils.string import *
from dal.users import get_users_with_role, check_user_token
from dal.threads import dal_get_user_threads
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
        consumer = create_consumer(request)
        return response('User was created', 201, {DATA: {CONSUMER: consumer}})
    except Exception as e:
        return response(str(e), 400)


@CONSUMERS_ROUTER.route('/consumers/<token>', methods=['GET'])
def get_user(token):
    """Gets current user"""

    try:
        username = check_user_token(token)
        return response('Successfully retreived user data', 200, {DATA: username})

    except AttributeError:
        return response('Wrong credentials', 400)


@CONSUMERS_ROUTER.route('/consumers/<username>/threads')
def get_user_threads(username):
    """Gets users threads"""

    try:
        threads = dal_get_user_threads(username)
        return response(threads, 200)
    except Exception:
        return response('Everything broke', 500)
