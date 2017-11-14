from flask import Blueprint, request, jsonify
from pymongo import MongoClient

users = Blueprint('users', __name__)

client = MongoClient('mongodb:27017')
db = client.userdb

# add bcrypt
@users.route('/users', methods=['GET', 'POST'])
def createUser():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password'] 

    user = {
      'username': username,
      'password': password
    }

    # value = db.usersdb.update({}, user, upsert=True)
    userExists = db.userdb.find_one({ 'username': username })
    if userExists:
      return jsonify({
        'status': 409,
        'message': 'User already exists'
      })
    else:
      db.userdb.insert(user)
      return jsonify({
        'status': 201,
        'message': 'User was created'
      })
