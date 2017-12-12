"""
Admin routes
"""

from flask import Blueprint, request
from utils.response import response
from utils.string import *
from dal.admin import auth_and_return_admin, create_default_admin

ADMIN_ROUTER = Blueprint(ADMIN, __name__)



@ADMIN_ROUTE.route('/admins', methods=['POST'])
def admin_actions():
    """When requested create admin account"""

    create_default_admin()
    return response('Admin account has been created', 201)


@ADMIN_ROUTER.route('/admins/auth', methods=['POST'])
def admin_auth():
    """Authenticates an admin"""

    try:
        encoded_data = auth_and_return_admin(request.form)
        return response('Successfully logged in as admin', 200, {TOKEN: encoded_data.decode('utf-8')})

    except AttributeError:
        return response('Wrong credentials', 400)
