from flask import Blueprint, request, jsonify
from pymongo import MongoClient
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
          'password': password
        }

        representativeExists = db.representatives.find_one({ 'username': username })

        if representativeExists:
          return jsonify({
            'status': 409,
            'message': 'Representative already exists'
          }), 409
        else:
          db.representatives.insert(representative)
          return jsonify({
            'status': 201,
            'message': 'Representative was created'
          }), 201
    except:
      return jsonify({
        'message': 'Wrong credentials',
        'status': 400
      }), 400
