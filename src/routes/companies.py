"""
Company routes
"""

from flask import Blueprint, request
from utils.response import response
from dal.users import get_users_with_role, find_user_by_name
import jwt

super_dal = SuperDAL()
COMPANIES = Blueprint('companies', __name__)

# add bcrypt


@COMPANIES.route('/companies')
def company_actions():
    """Extracts companies"""
    try:
        return get_users_with_role('company')
    except SystemError:
        return response('Something went wrong while retreiving the data', 500)


@COMPANIES.route('/companies', methods=['POST'])
def company_creation():
    """Creates company"""
    try:
        form = request.form
        token = form['jwt']
        payload = jwt.decode(token, 'super-secret')

        if payload['role'] == 'admin':
            username = form['username']
            password = form['password']

            company_exists = super_dal.create_company(username, password)

            if company_exists:
                return response('Username already exists', 409)
            else:
                return response('Company was created', 201)
        else:
            return response('You have to be an admin to create company', 400)
    except AttributeError:
        return response('Wrong credentials', 400)


@COMPANIES.route('/companies/<name>/representatives')
def get_representatives(name):
    """Gets list of representatives from specific company"""
    company = find_user_by_name(name)
    if company:
        representatives = super_dal.get_representatives_for_company(name)
        return response(name, 200, {'representatives': representatives})
    else:
        return response('Invalid company', 400)

# name => owner
@COMPANIES.route('/companies/<name>/representatives', methods=['POST'])
def create_representative(name):
    """Creates representative"""
    try:
        form = request.form
        token = form['jwt']
        payload = jwt.decode(token, 'super-secret')

        if payload['role'] == 'company':
            username = form['username']
            password = form['password']

            representative_exists = super_dal.create_representative(username, password, name)

            if representative_exists:
                return response('Username already exists', 409)
            else:
                return response('Representative was created', 201)
        else:
            return response('You are not a company', 400)
    except AttributeError:
        return response('Wrong credentials', 400)
