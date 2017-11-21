"""
Auth route
"""

from flask import Blueprint, request
from pymongo import MongoClient
from utils.response import response
import jwt

AUTH = Blueprint('auth', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api

# add bcrypt


@AUTH.route('/auth', methods=['POST'])
def auth_actions():
    """Authenticates any user"""

    try:
        username = request.form['username']
        password = request.form['password']

        found_user = DB.users.find_one(
            {'username': username, 'password': password})

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
