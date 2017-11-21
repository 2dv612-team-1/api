"""
Users
"""

from flask import Blueprint, request
from pymongo import MongoClient
from utils.response import response
import jwt

USERS = Blueprint('users', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api

# add bcrypt


@USERS.route('/users', methods=['GET', 'POST'])
def user_actions():
    """Creates user"""

    if request.method == 'POST':
        form = request.form

        try:
            username = form['username']
            password = form['password']

            user = {
                'username': username,
                'password': password
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
            for user in DB.users.find():
                _users.append({'username':user['username']})

            return response(
                'Successfully extracted all users', 200,
                {'users': _users}
            )
        except SystemError:
            return response('Something went wrong while retreiving the data', 500)


@USERS.route('/users/<token>', methods=['GET'])
def get_user(token):
    """Gets current user"""

    try:
        payload = jwt.decode(token, 'super-secret')
        username = payload['username']

        found_user = DB.users.find_one(
            {'username': username}
        )

        if found_user:
            return response(
                'Successfully gather user data', 200,
                {found_user}
            )
        else:
            raise AttributeError()
    except AttributeError:
        return response('Wrong credentials', 400)


@USERS.route('/users/auth', methods=['POST'])
def user_auth():
    """Authenticates user"""

    try:
        username = request.form['username']
        password = request.form['password']

        found_user = DB.users.find_one(
            {'username': username, 'password': password}
        )

        if found_user:
            payload = {'username': username, 'role': 'user'}
            encoded = jwt.encode(payload, 'super-secret')

            return response(
                'Successfully logged in as a user', 200,
                {'token': encoded.decode('utf-8')}
            )
        else:
            raise AttributeError()
    except AttributeError:
        return response('Wrong credentials', 400)
