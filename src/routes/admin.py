"""
Admin routes
"""

from flask import Blueprint, request
from utils.response import response
import jwt
from dal.admin import auth_and_return_admin, create_default_admin

ADMIN = Blueprint('admin', __name__)



@ADMIN.route('/admins', methods=['POST'])
def admin_actions():
    """When requested create admin account"""

    if request.method == 'POST':
        return create_default_admin()


@ADMIN.route('/admins/auth', methods=['POST'])
def admin_auth():
    """Authenticates an admin"""

    if request.method == 'POST':
        try:

            found_admin = auth_and_return_admin(request.form)

            if found_admin:
                payload = {'username': found_admin['username'], 'role': 'admin'}
                encoded = jwt.encode(payload, 'super-secret')
                return response('Successfully logged in as admin',
                                       200,
                                       {'token': encoded.decode('utf-8')})
            else:
                raise AttributeError()
        except AttributeError:
            return response('Wrong credentials', 400)
