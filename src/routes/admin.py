"""
Admin routes
"""

from flask import Blueprint, request
from pymongo import MongoClient
from utils.response import response
import jwt

CLIENT = MongoClient('mongodb:27017')
ADMIN = Blueprint('admin', __name__)
DB = CLIENT.api


@ADMIN.route('/admins', methods=['POST'])
def admin_actions():
    """When requested create admin account"""

    if request.method == 'POST':
        default_admin = {
            'username': 'admin',
            'password': 'admin123',
            'role': 'admin'
        }
        DB.users.update({}, default_admin, upsert=True)
        return response('Admin account has been created', 201)


@ADMIN.route('/admins/auth', methods=['POST'])
def admin_auth():
    """Authenticates an admin"""

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            found_admin = DB.admin.find_one(
                {'username': username, 'password': password})

            if found_admin:
                payload = {'username': username, 'role': 'admin'}
                encoded = jwt.encode(payload, 'super-secret')
                return response('Successfully logged in as admin',
                                       200,
                                       {'token': encoded.decode('utf-8')})
            else:
                raise AttributeError()
        except AttributeError:
            return response('Wrong credentials', 400)
