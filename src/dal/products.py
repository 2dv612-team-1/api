from .mongo_client import db_conn

from utils.files import check_request_files, create_file_path, save
from pymongo import ReturnDocument
from exceptions.WrongCredentials import WrongCredentials
from exceptions.InvalidRole import InvalidRole
from exceptions.BadFormData import BadFormData
from exceptions.AlreadyExist import AlreadyExist
from exceptions.ErrorCreatingFiles import ErrorCreatingFiles
from exceptions.ErrorRequestingFiles import ErrorRequestingFiles
from exceptions.NotFound import NotFound
import jwt
from utils.string import *
from config import *

from bson.objectid import ObjectId


def dal_get_products():
    products_data = list(map(lambda product: {
        NAME: product[NAME],
        CATEGORY: product[CATEGORY],
        DESCRIPTION: product[DESCRIPTION],
        CREATEDBY: product[CREATEDBY],
        ID: str(product[ID]),
        PRODUCER: product[PRODUCER]
    }, db_conn.products.products.find()))

    return products_data

def dal_get_product_by_id(_id):
    try:

        product = db_conn.products.find_one({'_id': ObjectId(_id)})
        files = db_conn.files.find({'owner': _id}, {'_id': False})

    except Exception:
        raise WrongCredentials()

    try:

        pretty_product = {
            'category': product['category'],
            'name': product['name'],
            'createdBy': product['createdBy'],
            'files': [files for files in files],
            'serialNo': product['serialNo'],
            'producer': product['producer'],
            'description': product['description']
        }

    except Exception:
        raise NotFound()

    return pretty_product


def dal_create_product_upload_files(form, files):

    #ref
    try:
        token = form['jwt']
    except Exception:
        raise WrongCredentials()

    try:
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        raise AttributeError()

    if payload['role'] != 'representative':
        raise InvalidRole()
    #ref

    try:
        check_request_files(files)
    except Exception:
        raise ErrorRequestingFiles()

    try:
        representative = db_conn.users.find_one({'username': payload['username']})
        company = representative['data']['owner']
        new_product = {
            'category': form['category'],
            'name': form['name'],
            'description': form['description'],
            'serialNo': form['serialNo'],
            'createdBy': payload['username'],
            'producer': company
        }
    except Exception:
        raise BadFormData()

    search_obj = {
        'producer': company,
        'serialNo': new_product['serialNo']
    }

    if db_conn.products.find_one(search_obj):
        raise AlreadyExist()

    _id = db_conn.products.insert(new_product)

    try:
        path = create_file_path(company, str(_id))
        filenames = save(path, files.getlist('files'))
        files = list(map(lambda filename: {
            'material_id': filename['file_time'],
            'owner': str(_id),
            'path': '/materials/' + company + '/' + str(_id) + '/' + filename['file_time'],
            'name': filename['file_name'],
            'stars': list(),
            'votes': 0,
            'comments': list(),
            'average': 0
        }, filenames))

    except Exception:
        raise ErrorCreatingFiles()

    if files:
        db_conn.files.insert(files)

    return _id


def dal_upload_files(form, files, _id):
    #ref
    try:
        token = form['jwt']
    except Exception:
        raise WrongCredentials()

    try:
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        raise AttributeError()

    if payload['role'] != 'representative':
        raise InvalidRole()
    #ref

    representative = db_conn.users.find_one({'username': payload['username']})
    file_company = representative['owner']

    try:

        if len(files) < 1:
            raise NotFound()

        check_request_files(files)

    except Exception:
        raise ErrorRequestingFiles()

    try:
        path = create_file_path(file_company, _id)
        filenames = save(path, files.getlist('files'))

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

    except Exception:
        raise ErrorCreatingFiles()

    if files:
        db_conn.files.insert(files)


def dal_rate_material(form, product_id, material_name):

    try:
        token = form['jwt']
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        raise WrongCredentials()

    if payload['role'] != 'consumer':
        raise InvalidRole()

    try:
        rate = form['rate']
    except Exception:
        raise BadFormData()

    try:
        rateInt = float(float(rate))
    except Exception:
        raise FloatingPointError()

    if rateInt > 5 or rateInt < 1:
        raise ValueError()

    user_has_voted = db_conn.files.find_one({
        'owner': str(product_id),
        'material_id': material_name,
        'stars.username': payload['username']
    })

    if user_has_voted:
        updated = db_conn.files.find_one_and_update(
            {'owner': str(product_id), 'material_id': material_name,
             'stars.username': payload['username']},
            {'$set': {'stars.$.rate': rateInt}},
            return_document=ReturnDocument.AFTER
        )
    else:
        updated = db_conn.files.find_one_and_update(
            {'owner': str(product_id), 'material_id': material_name},
            {'$inc': {'votes': 1}, '$push': {
                'stars': {'username': payload['username'], 'rate': rateInt}}},
            return_document=ReturnDocument.AFTER
        )

    if not updated:
        raise NotFound()

    current_votes = updated['stars']
    vote_amount = len(current_votes)
    total = 0
    for value in current_votes:
        total += value['rate']
    total_vote_value = round(total / vote_amount, 1)

    db_conn.files.find_one_and_update(
        {'owner': str(product_id), 'material_id': material_name},
        {'$set': {'average': total_vote_value}}
    )

    return total_vote_value, vote_amount
=======
    try:
        user = db_conn.users.find_one({USERNAME: name})
        owner = user[DATA][OWNER]
    except Exception:
        return 'No user information found'

    try:
        products = db_conn.products.find({PRODUCER: owner})
    except Exception:
        return 'Cannot get company products'

    return list(map(lambda product: {
        CATEGORY: product.get(CATEGORY),
        NAME: product.get(NAME),
        DESCRIPTION: product.get(DESCRIPTION),
        ID: str(product.get(ID)),
        SUB: product.get(SUB),
        PRODUCTNO: product.get(PRODUCTNO),
        CREATEDBY: product.get(CREATEDBY),
        PRODUCER: product.get(PRODUCER)
    }, products))
>>>>>>> origin/master
