"""
Representatives
"""

from flask import Blueprint, request
from pymongo import MongoClient
from utils.response import defaultResponse
import jwt

REPRESENTATIVES = Blueprint('users', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api

# add bcrypt


@REPRESENTATIVES.route('/representatives', methods=['GET', 'POST'])
def representative_actions():
    """Creates representative"""

    if request.method == 'POST':
        form = request.form

        try:
            token = form['jwt']
            payload = jwt.decode(token, 'super-secret')

            if payload['role'] == 'company':
                username = form['username']
                password = form['password']

                representative = {
                    'username': username,
                    'password': password,
                    'owner': payload['username']
                }

                representative_exists = DB.representatives.find_one(
                    {'username': username})

                if representative_exists:
                    return defaultResponse('Representative already exists', 409)
                else:
                    DB.representatives.insert(representative)
                    return defaultResponse('Representative was created', 201)
        except AttributeError:
            return defaultResponse('Wrong credentials', 400)

    if request.method == 'GET':
        try:
            token = request.args.get('token')
            payload = jwt.decode(token, 'super-secret')

            if payload['role'] == 'company':
                _representatives = []
                for representative in DB.representatives.find({'owner': payload['username']}):
                    _representatives.append(
                        {'username': representative['username']})

                return defaultResponse(
                    'Successfully extracted all representatives', 200,
                    {'representatives': _representatives}
                )
            else:
                return defaultResponse('You need to be a company to get representatives', 409)
        except SystemError:
            return defaultResponse('Something went wrong while retreiving the data', 500)


@REPRESENTATIVES.route('/representatives/auth', methods=['POST'])
def representatives_auth():
    """Authenticates representative"""

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            found_representative = DB.representatives.find_one(
                {'username': username, 'password': password}
            )

            if found_representative:
                payload = {'username': username, 'role': 'representative'}
                encoded = jwt.encode(payload, 'super-secret')

                return defaultResponse(
                    'Successfully logged in as a representative', 200,
                    {'token': encoded.decode('utf-8')}
                )
            else:
                raise AttributeError()
        except AttributeError:
            return defaultResponse('Wrong credentials', 400)
