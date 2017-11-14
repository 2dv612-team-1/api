from flask import Blueprint, request, jsonify
from pymongo import MongoClient

users = Blueprint('users', __name__)

client = MongoClient('mongodb:27017')
db = client.usersdb

# add bcrypt
@users.route('/users', methods=['GET', 'POST'])
def createUser():
  if request.method == 'POST':
    user = {
      'username': request.form['username'],
      'password': request.form['password']
    }

    db.usersdb.update({}, user, upsert=True)
    userd = db.usersdb.find({'username': request.form['username']})
    for user in userd:
      print(user)
    
    _items = db.usersdb.find()
    items = [item for item in _items]
    print(items)
    return jsonify(items)

