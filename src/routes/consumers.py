"""
Consumers
"""

from flask import Blueprint, request
from pymongo import MongoClient
from utils.response import response
import jwt

CONSUMERS = Blueprint('consumers', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api

# add bcrypt


@CONSUMERS.route('/consumers', methods=['GET', 'POST'])
def user_actions():
    """Creates user"""

    if request.method == 'POST':
        form = request.form

        try:
            username = form['username']
            password = form['password']

            user = {
                'username': username,
                'password': password,
                'role': 'consumer'
            }

            user_exists = DB.users.find_one(
                {'username': username})

            if user_exists:
                return response('User already exists', 409)
            else:
                DB.users.insert(user)
                return response('User was created', 201)
        except AttributeError:
            return response('Wrong credentials', 400)

    if request.method == 'GET':
        try:
            _users = []
            for user in DB.users.find({'role': 'consumer'}):
                _users.append({'username': user['username']})

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

        found_user = DB.users.find_one(
            {'username': username}
        )

        if found_user:
            return response(
                'Successfully gather user data', 200,
                {'data': found_user['username']}
            )
        else:
            raise AttributeError()
    except AttributeError:
        return response('Wrong credentials', 400)
