from flask import Blueprint, jsonify
entry = Blueprint('entry', __name__)

@entry.route('/')
def getEntry():
  routes = {
    'companies': '/companies',
    'representatives': '/representatives(?token=jwt)',
    'admins': '/admins',
    'self': '/'
  }
  return jsonify(routes)
