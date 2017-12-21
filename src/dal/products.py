from .mongo_client import db_conn

from utils.files import check_request_files, create_file_path, save
from utils.string import *
from utils.form_handler import *
from config import *
from pymongo import ReturnDocument
from exceptions.WrongCredentials import WrongCredentials
from exceptions.InvalidRole import InvalidRole
from exceptions.BadFormData import BadFormData
from exceptions.AlreadyExists import AlreadyExists
from exceptions.ErrorCreatingFiles import ErrorCreatingFiles
from exceptions.ErrorRequestingFiles import ErrorRequestingFiles
from exceptions.NotFound import NotFound
import jwt

from bson.objectid import ObjectId


def dal_get_products():

    products_data = list(map(lambda product: {
        NAME: product[NAME],
        CATEGORY: product[CATEGORY],
        SUBCATEGORY: product[SUBCATEGORY],
        DESCRIPTION: product[DESCRIPTION],
        CREATEDBY: product[CREATEDBY],
        ID: str(product[ID]),
        PRODUCER: product[PRODUCER]
    }, db_conn.products.find()))

    return products_data

def dal_get_product_by_id(_id):
    try:

        product = db_conn.products.find_one({'_id': ObjectId(_id)})
        files = db_conn.files.find({'owner': _id}, {'_id': False})

    except Exception:
        raise WrongCredentials()

    try:

        get_product = {
            CATEGORY: product[CATEGORY],
            SUBCATEGORY: product[SUBCATEGORY],
            NAME: product[NAME],
            CREATEDBY: product[CREATEDBY],
            FILES: [files for files in files],
            PRODUCTNO: product[PRODUCTNO],
            PRODUCER: product[PRODUCER],
            DESCRIPTION: product[DESCRIPTION]
        }

    except Exception:
        raise NotFound()

    return get_product


def dal_create_product_upload_files(request, username):

    try:
        check_request_files(request.files)
    except Exception:
        raise ErrorRequestingFiles()

    try:
        representative = db_conn.users.find_one({USERNAME: username})
        company = representative[DATA][OWNER]
        new_product = {
            CATEGORY: extract_attribute(request, CATEGORY),
            SUBCATEGORY: extract_attribute(request, SUBCATEGORY),
            NAME: extract_attribute(request, NAME),
            DESCRIPTION: extract_attribute(request, DESCRIPTION),
            PRODUCTNO: extract_attribute(request, PRODUCTNO),
            CREATEDBY: username,
            PRODUCER: company
        }
    except BadFormData as e:
        raise BadFormData(str(e))

    search_obj = {
        NAME: new_product[NAME],
        PRODUCER: company,
        PRODUCTNO: new_product[PRODUCTNO]
    }

    if db_conn.products.find_one(search_obj):
        raise AlreadyExists('Product already exists')

    _id = db_conn.products.insert(new_product)

    try:
        path = create_file_path(company, str(_id))
        filenames = save(path, request.files.getlist(FILES))
        files = list(map(lambda filename: {
            MATERIAL_ID: filename[MATERIAL_ID],
            FILENAME: filename[FILENAME],
            ORIGINAL_FILENAME: filename[ORIGINAL_FILENAME],
            OWNER: str(_id),
            PATH: '/' + MATERIALS + '/' + company + '/' + str(_id) + '/' + filename[FILENAME],
            RATES: list(),
            VOTES: 0,
            COMMENTS: list(),
            AVERAGE: 0
        }, filenames))

    except Exception as e:
        raise ErrorCreatingFiles(str(e))

    if files:
        db_conn.files.insert(files)

    new_product[ID] = str(_id)
    return new_product


def dal_upload_files(files, username, _id):
    representative = db_conn.users.find_one({USERNAME: username})
    file_company = representative[DATA][OWNER]

    try:

        if len(files) < 1:
            raise NotFound()

        check_request_files(files)

    except Exception:
        raise ErrorRequestingFiles()

    try:
        path = create_file_path(file_company, _id)
        filenames = save(path, files.getlist(FILES))

        files = list(map(lambda filename: {
            MATERIAL_ID: filename[MATERIAL_ID],
            FILENAME: filename[FILENAME],
            ORIGINAL_FILENAME: filename[ORIGINAL_FILENAME],
            OWNER: str(_id),
            PATH: '/' + MATERIALS + '/' + file_company + '/' + str(_id) + '/' + filename[FILENAME],
            RATES: list(),
            VOTES: 0,
            COMMENTS: list(),
            AVERAGE: 0
        }, filenames))

    except Exception:
        raise ErrorCreatingFiles()

    if files:
        db_conn.files.insert(files)


def dal_rate_material(rate, username, product_id, material_name):
    try:
        rateInt = float(rate)
    except Exception:
        raise FloatingPointError()

    if rateInt > 5 or rateInt < 1:
        raise ValueError()

    user_has_voted = db_conn.files.find_one({
        OWNER: str(product_id),
        MATERIAL_ID: material_name,
        '%s.%s' % (RATES, USERNAME): username
    })

    if user_has_voted:
        updated = db_conn.files.find_one_and_update(
            {OWNER: product_id, MATERIAL_ID: material_name,
             '%s.%s' % (RATES, USERNAME): username},
            {'$set': {'%s.$.%s' % (RATES, RATE): rateInt}},
            return_document=ReturnDocument.AFTER
        )
    else:
        updated = db_conn.files.find_one_and_update(
            {OWNER: product_id, MATERIAL_ID: material_name},
            {'$inc': {VOTES: 1}, '$push': {
                RATES: {USERNAME: username, RATE: rateInt}}},
            return_document=ReturnDocument.AFTER
        )

    if not updated:
        raise NotFound()

    current_votes = updated[RATES]
    vote_amount = len(current_votes)
    total = 0
    for value in current_votes:
        total += value[RATE]
    total_vote_value = round(total / vote_amount, 1)

    db_conn.files.find_one_and_update(
        {OWNER: str(product_id), MATERIAL_ID: material_name},
        {'$set': {AVERAGE: total_vote_value}}
    )

    return {
        AVERAGE: total_vote_value,
        AMOUNT: vote_amount
    }

