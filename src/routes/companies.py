"""
Company routes
"""

from flask import Blueprint, request
from utils.response import response
from utils.string import *
from dal.users import get_users_with_role
from dal.companies import create_company, get_representatives_for_company, dal_create_representative
from dal.products import get_products


COMPANIES = Blueprint('companies', __name__)


@COMPANIES.route('/companies')
def company_actions():
    """Extracts companies"""
    try:
        users = get_users_with_role(COMPANY)
        return response('Successfully extracted all users', 200, {'companies': users})
    except SystemError:
        return response('Something went wrong while retrieving the data', 500)


@COMPANIES.route('/companies', methods=['POST'])
def company_creation():
    """Creates company"""
    try:

        company_exists = create_company(request.form)

        if company_exists:
            return response('Username already exists', 409)
        else:
            return response('Company was created', 201)

    except AttributeError:
        return response('Wrong credentials', 400)


@COMPANIES.route('/companies/<name>/representatives')
def get_representatives(name):
    """Gets list of representatives from specific company"""
    try:
        representatives = get_representatives_for_company(name)
        return response(name, 200, {REPRESENTATIVE: representatives})

    except AttributeError:
        return response('Invalid company', 400)

# name => owner
@COMPANIES.route('/companies/<name>/representatives', methods=['POST'])
def create_representative(name):
    """Creates representative"""
    try:

        representative_exists = dal_create_representative(request.form, name)

        if representative_exists:
            return response('Username already exists', 409)
        else:
            return response('Representative was created', 201)

    except AttributeError:
        return response('Wrong credentials', 400)


@COMPANIES.route('/companies/<name>/products')
def get_product(name):
    """Gets all products for the company"""

    products = get_products(name)

    return response(
        'Successfully retreived all the products for company ' + name,
        200,
        { DATA:
            { PRODUCTS: products }
        }
    )
