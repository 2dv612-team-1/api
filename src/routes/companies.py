"""
Company routes
"""

from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from utils.response import defaultResponse
import jwt

companies = Blueprint('companies', __name__)
client = MongoClient('mongodb:27017')
db = client.api

# add bcrypt
@companies.route('/companies', methods=['GET', 'POST'])
def companyActions():
    if request.method == 'GET':

        try:
            data = []
            for company in db.companies.find():
                data.append({'username': company['username']})
            
            return defaultResponse('Successfully extracted all companies', 200, { 'companies': data })
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

                companyExists = db.companies.find_one({'username': username})

                if companyExists:
                    return defaultResponse('Company already exists', 409)
                else:
                    db.companies.insert(company)
                    return defaultResponse('Company was created', 201)
        except AttributeError:
            return defaultResponse('Wrong credentials', 400)


@companies.route('/companies/auth', methods=['POST'])
def companiesAuth():

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            foundCompany = db.companies.find_one(
                {'username': username, 'password': password})

            if foundCompany:
                payload = {'username': username, 'role': 'company'}
                encoded = jwt.encode(payload, 'super-secret')
                return defaultResponse('Successfully logged in as company', 200, { 'token': encoded.decode('utf-8') })
            else:
                raise AttributeError()
        except AttributeError:
            return defaultResponse('Wrong credentials', 400)
