"""
Products route
"""

from flask import Blueprint, request, current_app
from pymongo import MongoClient, ReturnDocument
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
            'name': product['name'],
            'category': product['category'],
            'description': product['description'],
            'createdBy': product['createdBy'],
            '_id': str(product['_id']),
            'files': product['files'],
            'producer': product['producer']
        })

    return response(
        'Successfully retreived all the products',
        200,
        {'data': {'products': products_data}}
    )


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
            'producer': company,
            'files': list()
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
        filenames = save(path, request.files.getlist('files'))
        files = list(map(lambda filename: {
            'material_id': filename['file_time'],
            'path': '/materials/' + company + '/' + str(_id) + '/' + filename['file_time'],
            'name': filename['file_name'],
            'stars': list(),
            'votes': 0,
            'comments': list(),
            'average': 0
        }, filenames))

        file_id = list(map(lambda file: {
            'material_id': file['file_time']
        }, filenames))

    except Exception as e:
        return response(str(e), 409)

    new_product = DB.products.find_one_and_update(
        {'_id': ObjectId(_id)},
        {'$set': {'files': file_id}},
        return_document=ReturnDocument.AFTER
    )

    DB.files.insert(files)

    return response('Product was created', 201, {'data': {'product': str(new_product)}})


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
            'createdBy': product['createdBy'],
            'files': product['files'],
            'serialNo': product['serialNo'],
            'producer': product['producer']
        }
    except Exception:
        return response('Cannot find product', 400)

    return response('Found product', 200, {'data': {'product': get_product}})


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
        product = DB.products.find_one(
            {'_id': ObjectId(_id), 'producer': file_company})
    except Exception as e:
        return response(str(e), 400)

    try:
        path = create_file_path(file_company, _id)
        filenames = save(path, request.files.getlist('files'))
        files = list(map(lambda filename: {
            'material': filename['file_time'],
            'path': '/materials/' + file_company + '/' + str(_id) + '/' + filename['file_time'],
            'name': filename['file_name'],
            'stars': list(),
            'votes': 0,
            'comments': list(),
            'average': 0
        }, filenames))

    except Exception as e:
        return response(str(e), 409)

    updated_product = DB.products.find_one_and_update(
        {'_id': ObjectId(_id)},
        {'$push': {'files': {'$each': files}}},
        return_document=ReturnDocument.AFTER
    )
    updated_product.update({
        '_id': str(updated_product['_id'])
    })
    return response(
        'Successfully uploaded material to the product',
        201,
        {'data': {'product': updated_product}}
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
        rateInt = int(rate)
    except Exception:
        return response('Expected rate to be int', 400)

    if rateInt > 5 or rateInt < 1:
        return response('Expected star value to be between 1 and 5', 400)

    user_has_voted = DB.products.find_one({
        '_id': ObjectId(product_id),
        'files.material': material_name,
        'files.stars.username': payload['username']
    })
    return response(str(user_has_voted), 200)

    # if user_has_voted:
    #     for file in user_has_voted['files']:
    #         if file['material'] == material_name:
    #             for rate in file['stars']:
    #                 if rate['username'] ==  payload['username']:
    #                     rate['rate'] == rateInt


    #     updated = DB.products.find_one_and_update({
    #         '_id': ObjectId(product_id),
    #         'files.material': material_name,
    #         'files.stars.username': payload['username']},
    #         {'$set': {'files.0.stars.$.rate': rateInt}},
    #         return_document=ReturnDocument.AFTER
    #     )
    #     return response(str(updated), 200)
    # else:
    updated = DB.products.find_one_and_update(
        {'_id': ObjectId(product_id), 'files.material': material_name},
        {'$inc': {'files.votes': 1}, '$push': {
            'files.$.stars': {'username': payload['username'], 'rate': rateInt}}}
    )

    current_votes = updated['files'][0]['stars']
    vote_amount = len(current_votes)
    total = 0
    for value in current_votes:
        total += value['rate']
    total_vote_value = total / vote_amount

    works = DB.products.find_one_and_update(
        { '_id': ObjectId(product_id), 'files.material': material_name},
        {'$set': {'files.$.average': total_vote_value}}
    )

    return response(str({
        'average': total_vote_value,
        'amount': vote_amount
    }), 200)
