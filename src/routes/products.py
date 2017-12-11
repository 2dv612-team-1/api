"""
Products route
"""

from flask import Blueprint, request, current_app
from pymongo import MongoClient, ReturnDocument
from exceptions.TamperedToken import TamperedToken
from utils.response import response
from utils.files import check_request_files, create_file_path, save
from dal.products import dal_get_products, dal_create_product_upload_files, dal_get_product_by_id
from exceptions.WrongCredentials import WrongCredentials
from exceptions.AlreadyExists import AlreadyExists
from exceptions.InvalidRole import InvalidRole
from exceptions.BadFormData import BadFormData
from exceptions.ErrorRequestingFiles import ErrorRequestingFiles
from exceptions.NotFound import NotFound

import jwt

PRODUCTS = Blueprint('products', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api

# add bcrypt


@PRODUCTS.route('/products')
def get_products():
    """Gets all available products"""

    products_data = dal_get_products()

    return response(
        'Successfully retreived all the products',
        200,
        {'data': {'products': products_data}}
    )


@PRODUCTS.route('/products', methods=['POST'])
def create_product():
    """Create a product"""
    try:

        _id = dal_create_product_upload_files(request.form, request.files)
        return response('Product was created', 201, {'data': {'product': str(_id)}})

    except AttributeError:
        return response('Broken JWT', 400)
    except WrongCredentials:
        return response('Invalid credentials', 400)
    except AlreadyExists:
        return response('Category exists', 409)
    except InvalidRole:
        return response('You are not a representative', 400)
    except BadFormData:
        return response('Wrong information', 400)
    except ErrorRequestingFiles:
        return response('Error requesting files', 409)


@PRODUCTS.route('/products/<_id>')
def get_product(_id):
    """Gets a single product"""
    try:

        product = dal_get_product_by_id(_id)
        return response('Found product', 200, {'data': {'product': product}})

    except WrongCredentials:
        return response('Not a valid id', 400)
    except NotFound:
        return response('Cannot find product', 400)

@PRODUCTS.route('/products/<_id>/materials', methods=['POST'])
def upload_actions(_id):

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

    representative = DB.users.find_one({'username': payload['username']})
    file_company = representative['owner']

    try:
        if len(request.files) < 1:
            raise AttributeError('Files missing from request')
        check_request_files(request.files)
    except AttributeError as e:
        return response(str(e), 400)

    try:
        path = create_file_path(file_company, _id)
        filenames = save(path, request.files.getlist('files'))

        files = list(map(lambda filename: {
            'material_id': filename['file_time'],
            'owner': str(_id),
            'path': '/materials/' + file_company + '/' + str(_id) + '/' + filename['file_time'],
            'name': filename['file_name'],
            'stars': list(),
            'votes': 0,
            'comments': list(),
            'average': 0
        }, filenames))

    except Exception as e:
        return response(str(e), 409)

    if files:
        DB.files.insert(files)

    return response(
        'Successfully uploaded material to the product',
        201,
        {'data': {'product': 'File uploaded'}}
    )


@PRODUCTS.route('/products/<product_id>/materials/<material_name>/rate', methods=['POST'])
def rate_material(product_id, material_name):
    """Used to rate material"""

    try:
        token = request.form['jwt']
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        return response('Expected jwt key', 400)

    if payload['role'] != 'consumer':
        return response('Have to be consumer to rate', 400)

    try:
        rate = request.form['rate']
    except Exception:
        return response('Expected rate key', 400)

    try:
        rateInt = float(float(rate))
    except Exception:
        return response('Expected rate to be int', 400)

    if rateInt > 5 or rateInt < 1:
        return response('Expected star value to be between 1 and 5', 400)

    user_has_voted = DB.files.find_one({
        'owner': str(product_id),
        'material_id': material_name,
        'stars.username': payload['username']
    })

    if user_has_voted:
        updated = DB.files.find_one_and_update(
            {'owner': str(product_id), 'material_id': material_name,
             'stars.username': payload['username']},
            {'$set': {'stars.$.rate': rateInt}},
            return_document=ReturnDocument.AFTER
        )
    else:
        updated = DB.files.find_one_and_update(
            {'owner': str(product_id), 'material_id': material_name},
            {'$inc': {'votes': 1}, '$push': {
                'stars': {'username': payload['username'], 'rate': rateInt}}},
            return_document=ReturnDocument.AFTER
        )

    if not updated:
        return response('There\'s nothing to rate', 200)

    current_votes = updated['stars']
    vote_amount = len(current_votes)
    total = 0
    for value in current_votes:
        total += value['rate']
    total_vote_value = round(total / vote_amount, 1)

    DB.files.find_one_and_update(
        {'owner': str(product_id), 'material_id': material_name},
        {'$set': {'average': total_vote_value}}
    )

    return response(str({
        'average': total_vote_value,
        'amount': vote_amount
    }), 200)
