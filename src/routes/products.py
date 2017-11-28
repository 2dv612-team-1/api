"""
Products route
"""

import os
from flask import Blueprint, request
from pymongo import MongoClient
from utils.response import response
from utils.extensionCheck import allowed_file
from werkzeug.utils import secure_filename
import jwt

UPLOAD_FOLDER = './uploads'
PRODUCTS = Blueprint('products', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api

@PRODUCTS.route('/products')
def get_products():
    """Gets all available products"""

    products_data = []
    for product in DB.products.find():
        products_data.append({
            'name': product.get('name'),
            'serialNo': product.get('serialNo'),
            'producer': product.get('producer'),
            'category': product.get('category'),
            'desc': product.get('desc'),
            'createdBy': product.get('createdBy') 
        })

    return response(products_data, 200)

@PRODUCTS.route('/products/upload', methods=['POST'])
def upload_actions():
    if 'file' not in request.files:
        return response('File param should be \'file\'', 400)
    file = request.files['file']
    file_category = request.form['category']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return response('No file present in request', 400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_folder = os.path.join(UPLOAD_FOLDER, file_category)
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)
        file_path = os.path.join(file_folder, filename)
        file.save(file_path)
        return response('Successfully uploaded the file', 200)
