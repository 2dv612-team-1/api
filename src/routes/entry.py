from flask import Blueprint, jsonify
entry = Blueprint('entry', __name__)

@entry.route('/')
def getEntry():
  routes = {
    'representatives': '/representatives',
    'companies': '/companies',
    'admins': '/admins',
    'self': '/'
  }
  return jsonify(routes)
