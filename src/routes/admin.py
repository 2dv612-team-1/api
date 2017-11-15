"""
Admin routes
"""

from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import jwt

client = MongoClient('mongodb:27017')
admin = Blueprint('admin', __name__)
db = client.api

@admin.route('/admins', methods=['POST'])
def adminActions():
    """When requested create admin account"""
    if request.method == 'POST':
        default_admin = {
            'username': 'admin',
            'password': 'admin123'
        }

        db.admin.update({}, default_admin, upsert=True)

        return jsonify({
            'status': 201,
            'message': 'Admin account has been created'
        }), 201

@admin.route('/admins/auth', methods=['POST'])
def adminAuth():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            foundAdmin = db.admin.find_one({'username': username, 'password': password})

            if foundAdmin:
                payload = {'username': username, 'role': 'admin'}
                encoded = jwt.encode(payload, 'super-secret')
                return jsonify({
                    'token': encoded.decode('utf-8'),
                    'message': 'Successfully logged in as admin',
                    'status': 200
                }), 200
            else:
                raise AttributeError()
        except AttributeError:
            return jsonify({
                'message': 'Wrong credentials',
                'status': 400
            }), 400
