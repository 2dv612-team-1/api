from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from utils.response import defaultResponse
import jwt

representatives = Blueprint('users', __name__)
client = MongoClient('mongodb:27017')
db = client.api

# add bcrypt


@representatives.route('/representatives', methods=['GET', 'POST'])
def representativeActions():
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

                representativeExists = db.representatives.find_one(
                    {'username': username})

                if representativeExists:
                    return defaultResponse('Representative already exists', 409)
                else:
                    db.representatives.insert(representative)
                    return defaultResponse('Representative was created', 201)
        except:
            return defaultResponse('Wrong credentials', 400)

    if request.method == 'GET':
        try:
            token = request.args.get('token')
            payload = jwt.decode(token, 'super-secret')

            if payload['role'] == 'company':
                _representatives = []
                for representative in db.representatives.find({'owner': payload['username']}):
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


@representatives.route('/representatives/auth', methods=['POST'])
def representatives_auth():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            found_representative = db.representatives.find_one(
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
