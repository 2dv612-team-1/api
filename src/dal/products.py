from .mongo_client import db_conn
from utils.files import check_request_files, create_file_path, save
from exceptions.WrongCredentials import WrongCredentials
from exceptions.InvalidRole import InvalidRole
from exceptions.BadFormData import BadFormData
from exceptions.AlreadyExist import AlreadyExist
from exceptions.ErrorCreatingFiles import ErrorCreatingFiles
from exceptions.ErrorRequestingFiles import ErrorRequestingFiles
from exceptions.NotFound import NotFound
import jwt

from bson.objectid import ObjectId


def dal_get_products():
    products_data = []
    for product in db_conn.products.find():
        products_data.append({
            'name': product['name'],
            'category': product['category'],
            'description': product['description'],
            'createdBy': product['createdBy'],
            '_id': str(product['_id']),
            'producer': product['producer']
        })
    return products_data


def dal_get_product_by_id(_id):
    try:

        product = db_conn.products.find_one({'_id': ObjectId(_id)})
        files = db_conn.files.find({'owner': _id}, {'_id': False})

    except Exception:
        raise WrongCredentials

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


def dal_upload_files():
    pass


def dal_get_product():
    pass
