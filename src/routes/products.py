"""
Products route
"""

from flask import Blueprint, request, current_app
from pymongo import MongoClient, ReturnDocument
from exceptions.TamperedToken import TamperedToken
from utils.response import response
from utils.string import *
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

    products_data = list(map(lambda product: {
        NAME: product[NAME],
        CATEGORY: product[CATEGORY],
        DESCRIPTION: product[DESCRIPTION],
        CREATEDBY: product[CREATEDBY],
        ID: str(product[ID]),
        PRODUCER: product[PRODUCER]
    }, DB.products.find()))

    return response(
        'Successfully retreived all the products',
        200,
        {DATA: {PRODUCTSs: products_data}}
    )


@PRODUCTS.route('/products', methods=['POST'])
def create_product():
    """Create a product"""

    try:
        token = request.form[JWT]
    except Exception:
        return response('No JWT', 400)

    try:
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        return response('Tampered token', 400)

    if payload[ROLE] != REPRESENTATIVE:
        return response('You are not a representative', 400)

    try:
        check_request_files(request.files)
    except AttributeError as e:
        return response(str(e), 400)

    try:
        representative = DB.users.find_one({USERNAME: payload[USERNAME]})
        company = representative[DATA][OWNER]
        new_product = {
            CATEGORY: request.form[CATEGORY],
            NAME: request.form[NAME],
            DESCRIPTION: request.form[DESCRIPTION],
            SERIALNO: request.form[SERIALNO],
            CREATEDBY: payload[USERNAME],
            PRODUCER: company
        }
    except Exception:
        return response('Wrong information', 400)

    search_obj = {
        NAME: new_product[NAME],
        PRODUCER: company,
        SERIALNO: new_product[SERIALNO]
    }

    if DB.products.find_one(search_obj):
        return response('Product already exists', 409)

    _id = DB.products.insert(new_product)

    try:
        path = create_file_path(company, str(_id))
        filenames = save(path, request.files.getlist(FILES))
        files = list(map(lambda filename: {
            MATERIAL_ID: filename[FILE_TIME],
            OWNER: str(_id),
            PATH: '/' + MATERIALS + '/' + company + '/' + str(_id) + '/' + filename[FILE_TIME],
            NAME: filename[FILE_NAME],
            RATES: list(),
            VOTES: 0,
            COMMENTS: list(),
            AVERAGE: 0
        }, filenames))

    except Exception as e:
        return response(str(e), 409)

    if files:
        DB.files.insert(files)

    return response('Product was created', 201, {DATA: {PRODUCTSs: str(_id)}})


@PRODUCTS.route('/products/<_id>')
def get_product(_id):
    """Gets a single product"""

    try:
        product = DB.products.find_one({ID: ObjectId(_id)})
        files = DB.files.find({OWNER: _id}, {ID: False})
    except Exception:
        return response('Not a valid id', 400)

    try:
        get_product = {
            CATEGORY: product[CATEGORY],
            NAME: product[NAME],
            CREATEDBY: product[CREATEDBY],
            FILES: [files for files in files],
            SERIALNO: product[SERIALNO],
            PRODUCER: product[PRODUCER],
            DESCRIPTION: product[DESCRIPTION]
        }
    except Exception:
        return response('Cannot find product', 400)

    return response('Found product', 200, {DATA: {PRODUCTSs: get_product}})


@PRODUCTS.route('/products/<_id>/materials', methods=['POST'])
def upload_actions(_id):

    try:
        token = request.form[JWT]
    except Exception:
        return response('No JWT', 400)

    try:
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        return response('Tampered token', 400)

    if payload[ROLE] != REPRESENTATIVE:
        return response('You are not a representative', 400)

    representative = DB.users.find_one({USERNAME: payload[USERNAME]})
    file_company = representative[DATA][OWNER]

    try:
        if len(request.files) < 1:
            raise AttributeError('Files missing from request')
        check_request_files(request.files)
    except AttributeError as e:
        return response(str(e), 400)

    try:
        path = create_file_path(file_company, _id)
        filenames = save(path, request.files.getlist(FILES))

        files = list(map(lambda filename: {
            MATERIAL_ID: filename[FILE_TIME],
            OWNER: str(_id),
            PATH: '/' + MATERIALS + '/' + file_company + '/' + str(_id) + '/' + filename['file_time'],
            NAME: filename[FILE_NAME],
            RATES: list(),
            VOTES: 0,
            COMMENTS: list(),
            AVERAGE: 0
        }, filenames))

    except Exception as e:
        return response(str(e), 409)

    if files:
        DB.files.insert(files)

    return response(
        'Successfully uploaded material to the product',
        201,
        {DATA: {PRODUCTSs: 'File uploaded'}}
    )


@PRODUCTS.route('/products/<product_id>/materials/<material_name>/rate', methods=['POST'])
def rate_material(product_id, material_name):
    """Used to rate material"""

    try:
        token = request.form[JWT]
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        return response('Expected jwt key', 400)

    if payload[ROLE] != CONSUMER:
        return response('Have to be consumer to rate', 400)

    try:
        rate = request.form[ROLE]
    except Exception:
        return response('Expected rate key', 400)

    try:
        rateInt = float(float(rate))
    except Exception:
        return response('Expected rate to be int', 400)

    if rateInt > 5 or rateInt < 1:
        return response('Expected star value to be between 1 and 5', 400)

    user_has_voted = DB.files.find_one({
        OWNER: str(product_id),
        MATERIAL_ID: material_name,
        '%s.%s' % (RATES, USERNAME): payload[USERNAME]
    })

    if user_has_voted:
        updated = DB.files.find_one_and_update(
            {OWNER: str(product_id), MATERIAL_ID: material_name,
             '%s.%s' % (RATE, USERNAME): payload[USERNAME]},
            {'$set': {'%s.$.%s' % (RATES, RATE): rateInt}},
            return_document=ReturnDocument.AFTER
        )
    else:
        updated = DB.files.find_one_and_update(
            {OWNER: str(product_id), MATERIAL_ID: material_name},
            {'$inc': {VOTES: 1}, '$push': {
                RATES: {USERNAME: payload[USERNAME], RATE: rateInt}}},
            return_document=ReturnDocument.AFTER
        )

    if not updated:
        return response('There\'s nothing to rate', 200)

    current_votes = updated[RATES]
    vote_amount = len(current_votes)
    total = 0
    for value in current_votes:
        total += value[RATE]
    total_vote_value = round(total / vote_amount, 1)

    DB.files.find_one_and_update(
        {OWNER: str(product_id), MATERIAL_ID: material_name},
        {'$set': {AVERAGE: total_vote_value}}
    )

    return response(str({
        AVERAGE: total_vote_value,
        AMOUNT: vote_amount
    }), 200)
