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

        representativeExists = db.representatives.find_one({ 'username': username })

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
          _representatives.append({'username': representative['username']})

        return jsonify({
          'status': 200,
          'message': 'Successfully extracted all representatives',
          'representatives': _representatives
        }), 200
      else:
        return defaultResponse('You need to be a company to get representatives', 409)
    except SystemError:
      return defaultResponse('Something went wrong while retreiving the data', 500)

@representatives.route('/representatives/auth', methods=['POST'])
def representativesAuth():

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            foundRepresentative = db.representatives.find_one({'username': username, 'password': password})

            if foundRepresentative:
                payload = {'username': username, 'role': 'representative'}
                encoded = jwt.encode(payload, 'super-secret')
                return jsonify({
                    'token': encoded.decode('utf-8'),
                    'message': 'Successfully logged in as representative',
                    'status': 200
                }), 200
            else:
                raise AttributeError()
        except AttributeError:
            return defaultResponse('Wrong credentials', 400)
