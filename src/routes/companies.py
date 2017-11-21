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

    """Extracts companies"""
    if request.method == 'GET':

        try:
            data = []
            for company in DB.companies.find():
                data.append({'username': company['username']})

            return response('Successfully extracted all companies', 200, {'companies': data})
        except SystemError:
            return response('Something went wrong while retreiving the data', 500)

    """Creates company"""
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
                    'password': password,
                    'role': 'company'
                }

                company_exists = DB.users.find_one({'username': username})

                if company_exists:
                    return response('Company already exists', 409)
                else:
                    DB.users.insert(company)
                    return response('Company was created', 201)
        except AttributeError:
            return response('Wrong credentials', 400)


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

                return response('Successfully logged in as company',
                                       200,
                                       {'token': encoded.decode('utf-8')})
            else:
                raise AttributeError()
        except AttributeError:
            return response('Wrong credentials', 400)
