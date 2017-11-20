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


@COMPANIES.route('/companies', methods=['GET', 'POST'])
def company_actions():
    """Creates company"""

    if request.method == 'GET':

        try:
            data = []
            for company in DB.companies.find():
                data.append({'username': company['username']})

            return defaultResponse('Successfully extracted all companies', 200, {'companies': data})
        except SystemError:
            return defaultResponse('Something went wrong while retreiving the data', 500)

    if request.method == 'POST':
        form = request.form

        try:
            token = form['jwt']
            payload = jwt.decode(token, 'super-secret')

            if payload['role'] == 'admin':
                username = form['username']
                password = form['password']

                company = {
                    'username': username,
                    'password': password
                }

                company_exists = DB.companies.find_one({'username': username})

                if company_exists:
                    return defaultResponse('Company already exists', 409)
                else:
                    DB.companies.insert(company)
                    return defaultResponse('Company was created', 201)
        except AttributeError:
            return defaultResponse('Wrong credentials', 400)


@COMPANIES.route('/companies/auth', methods=['POST'])
def companies_auth():
    """Authenticates company"""

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            found_company = DB.companies.find_one(
                {'username': username, 'password': password})

            if found_company:
                payload = {'username': username, 'role': 'company'}
                encoded = jwt.encode(payload, 'super-secret')

                return defaultResponse('Successfully logged in as company',
                                       200,
                                       {'token': encoded.decode('utf-8')})
            else:
                raise AttributeError()
        except AttributeError:
            return defaultResponse('Wrong credentials', 400)
