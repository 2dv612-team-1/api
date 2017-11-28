"""
Admin routes
"""

from flask import Blueprint, request
from utils.response import response
from utils.dal import SuperDAL
import jwt

super_dal = SuperDAL()
ADMIN = Blueprint('admin', __name__)



@ADMIN.route('/admins', methods=['POST'])
def admin_actions():
    """When requested create admin account"""

    if request.method == 'POST':
        super_dal.create_default_admin()
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
