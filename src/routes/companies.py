"""
Company routes
"""

from flask import Blueprint, request
from pymongo import MongoClient
from utils.response import response
import jwt

COMPANIES = Blueprint('companies', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api

# add bcrypt


@COMPANIES.route('/companies')
def company_actions():
    """Extracts companies"""
    try:
        data = []
        for company in DB.users.find({'role': 'company'}):
            data.append({'username': company['username']})

        return response('Successfully extracted all companies', 200, {'companies': data})
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

            company = {
                'username': username,
                'password': password,
                'role': 'company'
            }

            company_exists = DB.users.find_one({'username': username})

            if company_exists:
                return response('Username already exists', 409)
            else:
                DB.users.insert(company)
                return response('Company was created', 201)
        else:
            return response('You have to be an admin to create company', 400)
    except AttributeError:
        return response('Wrong credentials', 400)


@COMPANIES.route('/companies/<name>/representatives')
def get_representatives(name):
    """Gets list of representatives from specific company"""
    company = DB.users.find_one({'username': name})
    if company:
        representatives = []
        for representative in DB.users.find({'owner': name}):
            representatives.append({'username': representative['username']})
        return response(name, 200, {'representatives': representatives})
    else:
        return response('Invalid company', 400)


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

            representative = {
                'username': username,
                'password': password,
                'owner': name,
                'role': 'representative'
            }

            representative_exists = DB.users.find_one({'username': username})

            if representative_exists:
                return response('Username already exists', 409)
            else:
                DB.users.insert(representative)
                return response('Representative was created', 201)
        else:
            return response('You are not a company', 400)
    except AttributeError:
        return response('Wrong credentials', 400)
