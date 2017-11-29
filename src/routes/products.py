"""
Products route
"""

import os
from flask import Blueprint, request
from pymongo import MongoClient
from exceptions.TamperedToken import TamperedToken
from utils.response import response
from utils.extensionCheck import allowed_file
from bson.objectid import ObjectId
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
            'title': product.get('title'),
            'category': product.get('category'),
            'description': product.get('description'),
            'createdBy': product.get('createdBy'),
            '_id': str(product.get('_id'))
        })

    return response(products_data, 200)


@PRODUCTS.route('/products', methods=['POST'])
def create_product():
    """Create a product"""

    try:
        token = request.form['jwt']
    except Exception:
        return response('No JWT', 400)

    try:
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        return response('Tampered token', 400)

    if payload['role'] == 'representative':
        try:
            file = request.files['file']
        except Exception:
            return response('No key \'file\' is present', 400)

        try:
            filename = secure_filename(file.filename)
        except Exception:
            return response(str(request.files), 200)
            return response('No file present in request', 400)

        return response('Successfully uploaded the file', 200)

        try:
            new_product = {
                'category': request.form['category'],
                'title': request.form['title'],
                'description': request.form['description'],
                'createdBy': payload['username']
            }
        except Exception:
            return response('Wrong information', 400)

        try:
            file_folder = os.path.join(UPLOAD_FOLDER, new_product['category'])
        except Exception:
            return response('Could not create directory', 409)

        try:
            if not os.path.exists(file_folder):
                os.makedirs(file_folder)
            file_path = os.path.join(file_folder, filename)
            file.save(file_path)
            new_product.update({'file': file_path})
        except Exception:
            return response('Could not create file', 409)

        if DB.products.find_one(new_product):
            return response('Product already exists', 409)

        DB.products.insert(new_product)
        return response('Product was created', 201)
    else:
        return response('You are not a representative', 400)


@PRODUCTS.route('/products/<_id>')
def get_product(_id):
    """Gets a single product"""

    try:
        product = DB.products.find_one({'_id': ObjectId(_id)})
    except Exception:
        return response('Not a valid id', 400)

    try:
        get_product = {
            'category': product['category'],
            'title': product['title'],
            'description': product['description'],
            'createdBy': product['createdBy']
        }
    except Exception:
        return response('Cannot find product', 400)

    if product:
        return response(get_product, 200)
    else:
        return response('No product with that id', 200)


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
