"""
Company routes
"""

from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import jwt

companies = Blueprint('companies', __name__)
client = MongoClient('mongodb:27017')
db = client.api

# add bcrypt
# GET not implemented yet
@companies.route('/companies', methods=['GET', 'POST'])
def companyActions():
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

        companyExists = db.companies.find_one({ 'username': username })

        if companyExists:
          return jsonify({
            'status': 409,
            'message': 'Company already exists'
          }), 409
        else:
          db.companies.insert(company)
          return jsonify({
            'status': 201,
            'message': 'Company was created'
          }), 201
    except:
      return jsonify({
        'message': 'Wrong credentials',
        'status': 400
      }), 400

@companies.route('/companies/auth', methods=['POST'])
def companiesAuth():

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            foundCompany = db.companies.find_one({'username': username, 'password': password})

            if foundCompany:
                payload = {'username': username, 'role': 'company'}
                encoded = jwt.encode(payload, 'super-secret')
                return jsonify({
                    'token': encoded.decode('utf-8'),
                    'message': 'Successfully logged in as company',
                    'status': 200
                }), 200
            else:
                raise AttributeError()
        except AttributeError:
            return jsonify({
                'message': 'Wrong credentials',
                'status': 400
            }), 400