"""
Company routes
"""

from flask import Blueprint, request
from utils.response import response
from utils.string import *
from utils.jwt_handler import *
from dal.users import get_users_with_role
from dal.companies import create_company, get_representatives_for_company, dal_create_representative, get_products_for_company, dal_read_thread
from exceptions.BadFormData import BadFormData


COMPANIES_ROUTER = Blueprint(COMPANIES, __name__)


@COMPANIES_ROUTER.route('/companies')
def company_actions():
    """Extracts companies"""
    try:
        users = get_users_with_role(COMPANY)
        return response('Successfully extracted all users', 200, {COMPANIES: users})
    except SystemError:
        return response('Something went wrong while retrieving the data', 500)


@COMPANIES_ROUTER.route('/companies', methods=['POST'])
def company_creation():
    """Creates company"""
    try:
        payload = extract(request)
        authorized_role(payload, ADMIN)
        company = create_company(request)
        return response('Company was created', 201, {DATA: {COMPANY: company}})

    except Exception as e:
        return response(str(e), 400)


@COMPANIES_ROUTER.route('/companies/<name>/representatives')
def get_representatives(name):
    """Gets list of representatives from specific company"""
    try:
        representatives = get_representatives_for_company(name)
        return response(name, 200, {REPRESENTATIVES: representatives})

    except AttributeError:
        return response('Invalid company', 400)


@COMPANIES_ROUTER.route('/companies/<name>/representatives', methods=['POST'])
def create_representative(name):
    """Creates representative"""
    try:
        payload = extract(request)
        authorized_role(payload, COMPANY)
        representative = dal_create_representative(request, name)
        return response('Representative was created', 201, {DATA: {REPRESENTATIVE: representative}})

    except Exception as e:
        return response(str(e), 400)


@COMPANIES_ROUTER.route('/companies/<name>/products')
def get_product(name):
    """Gets all products for the company"""
    try:

        products = get_products_for_company(name)
        return response(
            'Successfully retreived all the products for company ' + name,
            200,
            {DATA:
             {PRODUCTS: products}
             })
    except Exception as e:
        return response(str(e), 400)


@COMPANIES_ROUTER.route('/companies/<name>/threads/<thread_id>', methods=['PATCH'])
def remove_thread_read(name, thread_id):
    """Removes read thread from company"""

    try:
        payload = extract(request)
        authorized_role(payload, REPRESENTATIVE)

        if payload[DATA][OWNER] != name:
            raise BadFormData('Wrong company')

        dal_read_thread(thread_id, name)
        return response('', 204)
    except Exception as e:
        return response(str(e), 400)
