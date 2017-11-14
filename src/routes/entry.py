from flask import Blueprint, jsonify
entry = Blueprint('entry', __name__)

@entry.route('/')
def getEntry():
  routes = {
    'auth': '/auth',
    'self': '/'
  }
  return jsonify(routes)
