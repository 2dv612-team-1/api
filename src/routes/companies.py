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
        name = form['name']
        password = form['password']

        company = {
          'name': name,
          'password': password
        }

        companyExists = db.companies.find_one({ 'name': name })

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