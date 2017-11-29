"""
Products route
"""

from flask import Blueprint, request, current_app
from pymongo import MongoClient
from utils.response import response
from utils.files import files
import jwt

PRODUCTS = Blueprint('products', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api

# add bcrypt

@PRODUCTS.route('/products/upload', methods=['POST'])
def upload_actions():

    # Get from JWT instead
    file_company = request.form['company']

    f = files(request.files)
    # Check user error
    try:
        f.check_request_files()
    except AttributeError as e:
        return response(str(e), 400)

    f.save(file_company)

    return response('Successfully uploaded material', 200)
