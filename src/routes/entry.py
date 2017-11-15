from flask import Blueprint, jsonify
entry = Blueprint('entry', __name__)

@entry.route('/')
def getEntry():
  routes = {
    'auth': '/auth',
    'representatives': '/representatives',
    'self': '/'
  }
  return jsonify(routes)
