"""
Products route
"""

from flask import Blueprint, request, current_app
from pymongo import MongoClient
from exceptions.TamperedToken import TamperedToken
from utils.response import response
from utils.files import check_request_files, create_file_path, save
from bson.objectid import ObjectId
import jwt

PRODUCTS = Blueprint('products', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api

# add bcrypt

@PRODUCTS.route('/products')
def get_products():
    """Gets all available products"""

    products_data = []
    for product in DB.products.find():
        products_data.append({
            'name': product.get('name'),
            'category': product.get('category'),
            'description': product.get('description'),
            'createdBy': product.get('createdBy'),
            '_id': str(product.get('_id')),
            'paths': product.get('paths')
        })

    return response('Successfully retreived all the products', 200, { 'data': { 'products': products_data } })


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

    if payload['role'] != 'representative':
        return response('You are not a representative', 400)

    try:
        check_request_files(request.files)
    except AttributeError as e:
        return response(str(e), 400)

    try:
        representative = DB.users.find_one({'username': payload['username']})
        company = representative['owner']
        new_product = {
            'category': request.form['category'],
            'name': request.form['name'],
            'description': request.form['description'],
            'serialNo': request.form['serialNo'],
            'createdBy': payload['username'],
            'producer': company
        }
    except Exception:
        return response('Wrong information', 400)

    search_obj = {
        'name': new_product['name'],
        'producer': company,
        'serialNo': new_product['serialNo']
    }

    if DB.products.find_one(search_obj):
        return response('Product already exists', 409)

    _id = DB.products.insert(new_product)

    try:
        path = create_file_path(company, str(_id))
        filenames = save(path, request.files.getlist('file'), new_product)
        paths = list()
        for filename in filenames:
            paths.append({'path': '/materials/' + company + '/' + str(_id) + '/' + filename})

    except Exception as e:
        return response(str(e), 409)

    DB.products.find_one_and_update(
        {'_id': ObjectId(_id)},
        {'$set': {'paths': paths}}
    )
    new_product.update({
        '_id': str(_id),
        'paths': paths
    })
    return response('Product was created', 201, { 'data': {'product': new_product}})


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
            'name': product['name'],
            'description': product['description'],
            'createdBy': product['createdBy'],
            'paths': product['paths'],
            'serialNo': product['serialNo'],
            'producer': product['producer']
        }
    except Exception:
        return response('Cannot find product', 400)

    return response('Found product', 200, { 'data': { 'product': get_product } })

@PRODUCTS.route('/products/upload', methods=['POST'])
def upload_actions():

    # Get from JWT instead
    file_company = request.form['company']
    # Get from URL id
    product = 'a'

    try:
        check_request_files(request.files)
    except AttributeError as e:
        return response(str(e), 400)

    path = create_file_path(file_company, product)
    save(path, request.files.getlist('file'))

    return response('Successfully uploaded material', 200)
