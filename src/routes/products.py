"""
Products route
"""

from flask import Blueprint, request
from utils.response import response

from dal.products import dal_get_products, dal_create_product_upload_files, dal_get_product_by_id, dal_upload_files, dal_rate_material
from exceptions.WrongCredentials import WrongCredentials
from exceptions.AlreadyExists import AlreadyExists
from exceptions.InvalidRole import InvalidRole
from exceptions.BadFormData import BadFormData
from exceptions.ErrorRequestingFiles import ErrorRequestingFiles
from exceptions.ErrorCreatingFiles import ErrorCreatingFiles
from exceptions.NotFound import NotFound

from utils.string import *
from config import *


PRODUCTS_ROUTER = Blueprint(PRODUCTS, __name__)


@PRODUCTS_ROUTER.route('/products')
def get_products():
    """Gets all available products"""

    products_data = dal_get_products()
    return response(
        'Successfully retreived all the products',
        200,
        {DATA: {PRODUCTS: products_data}}
    )


@PRODUCTS_ROUTER.route('/products', methods=['POST'])
def create_product():
    """Create a product"""
    try:
<<<<<<< HEAD

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
=======
        token = request.form[JWT]
    except Exception:
        return response('No JWT', 400)

    try:
        payload = jwt.decode(token, SECRET)
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
            PRODUCTNO: request.form[PRODUCTNO],
            CREATEDBY: payload[USERNAME],
            PRODUCER: company
        }
    except Exception:
        return response('Wrong information', 400)

    search_obj = {
        NAME: new_product[NAME],
        PRODUCER: company,
        PRODUCTNO: new_product[PRODUCTNO]
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

    return response('Product was created', 201, {DATA: {PRODUCTS: str(_id)}})
>>>>>>> origin/master


@PRODUCTS_ROUTER.route('/products/<_id>')
def get_product(_id):
    """Gets a single product"""
    try:
<<<<<<< HEAD

        product = dal_get_product_by_id(_id)
        return response('Found product', 200, {'data': {'product': product}})
=======
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
            PRODUCTNO: product[PRODUCTNO],
            PRODUCER: product[PRODUCER],
            DESCRIPTION: product[DESCRIPTION]
        }
    except Exception:
        return response('Cannot find product', 400)

    return response('Found product', 200, {DATA: {PRODUCTS: get_product}})
>>>>>>> origin/master

    except WrongCredentials:
        return response('Not a valid id', 400)
    except NotFound:
        return response('Cannot find product', 400)

@PRODUCTS_ROUTER.route('/products/<_id>/materials', methods=['POST'])
def upload_actions(_id):
    try:
<<<<<<< HEAD

        dal_upload_files(request.form, request.files, _id)
        return response(
            'Successfully uploaded material to the product',
            201,
            {'data': {'product': 'File uploaded'}}
        )
=======
        token = request.form[JWT]
    except Exception:
        return response('No JWT', 400)

    try:
        payload = jwt.decode(token, SECRET)
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
            PATH: '/' + MATERIALS + '/' + file_company + '/' + str(_id) + '/' + filename[FILE_TIME],
            NAME: filename[FILE_NAME],
            RATES: list(),
            VOTES: 0,
            COMMENTS: list(),
            AVERAGE: 0
        }, filenames))

    except Exception as e:
        return response(str(e), 409)
>>>>>>> origin/master

    except AttributeError:
        return response('Broken JWT', 400)
    except WrongCredentials:
        return response('Invalid credentials', 400)
    except NotFound:
        return response('Files missing from request', 400)
    except ErrorRequestingFiles:
        return response('Error requesting files', 409)
    except ErrorCreatingFiles:
        return response('Error creating files', 409)

<<<<<<< HEAD
=======
    return response(
        'Successfully uploaded material to the product',
        201,
        {DATA: {PRODUCTS: 'File uploaded'}}
    )
>>>>>>> origin/master


@PRODUCTS_ROUTER.route('/products/<product_id>/materials/<material_name>/rate', methods=['POST'])
def rate_material(product_id, material_name):
    """Used to rate material"""
    try:
<<<<<<< HEAD

        total_vote_value, vote_amount = dal_rate_material(request.form, product_id, material_name)
        return response(str({
            'average': total_vote_value,
            'amount': vote_amount
        }), 200)

    except WrongCredentials:
        return response('Expected jwt key', 400)
    except InvalidRole:
        return response('Have to be consumer to rate', 400)
    except BadFormData:
=======
        token = request.form[JWT]
        payload = jwt.decode(token, SECRET)
    except Exception:
        return response('Expected jwt key', 400)

    if payload[ROLE] != CONSUMER:
        return response('Have to be consumer to rate', 400)

    try:
        rate = request.form[RATE]
    except Exception:
>>>>>>> origin/master
        return response('Expected rate key', 400)
    except FloatingPointError:
        return response('Expected rate to be int', 400)
    except ValueError:
        return response('Expected star value to be between 1 and 5', 400)
<<<<<<< HEAD
    except NotFound:
        return response('There\'s nothing to rate', 200)
=======

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
>>>>>>> origin/master
