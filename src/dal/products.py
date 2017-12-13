from .mongo_client import db_conn

from utils.files import check_request_files, create_file_path, save
from utils.string import *
from config import *
from pymongo import ReturnDocument
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

    products_data = list(map(lambda product: {
        NAME: product[NAME],
        CATEGORY: product[CATEGORY],
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


def dal_create_product_upload_files(form, files):

    #ref
    try:
        token = form[JWT]
    except Exception:
        raise WrongCredentials()

    try:
        payload = jwt.decode(token, SECRET)
    except Exception:
        raise AttributeError()

    if payload[ROLE] != REPRESENTATIVE:
        raise InvalidRole()

    try:
        check_request_files(files)
    except Exception:
        raise ErrorRequestingFiles()
    #ref

    try:
        representative = db_conn.users.find_one({USERNAME: payload[USERNAME]})
        company = representative[DATA][OWNER]
        new_product = {
            CATEGORY: form[CATEGORY],
            NAME: form[NAME],
            DESCRIPTION: form[DESCRIPTION],
            PRODUCTNO: form[PRODUCTNO],
            CREATEDBY: payload[USERNAME],
            PRODUCER: company
        }
    except Exception:
        raise BadFormData()

    search_obj = {
        NAME: new_product[NAME],
        PRODUCER: company,
        PRODUCTNO: new_product[PRODUCTNO]
    }

    if db_conn.products.find_one(search_obj):
        raise AlreadyExist()

    _id = db_conn.products.insert(new_product)

    try:
        path = create_file_path(company, str(_id))
        filenames = save(path, files.getlist(FILES))
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

    except Exception:
        raise ErrorCreatingFiles()

    if files:
        db_conn.files.insert(files)

    return _id


def dal_upload_files(form, files, _id):
    #ref
    try:
        token = form[JWT]
    except Exception:
        raise WrongCredentials()

    try:
        payload = jwt.decode(token, SECRET)
    except Exception:
        raise AttributeError()

    if payload[ROLE] != REPRESENTATIVE:
        raise InvalidRole()
    #ref

    representative = db_conn.users.find_one({USERNAME: payload[USERNAME]})
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
            MATERIAL_ID: filename[FILE_TIME],
            OWNER: str(_id),
            PATH: '/' + MATERIALS + '/' + file_company + '/' + str(_id) + '/' + filename[FILE_TIME],
            NAME: filename[FILE_NAME],
            RATES: list(),
            VOTES: 0,
            COMMENTS: list(),
            AVERAGE: 0
        }, filenames))

    except Exception:
        raise ErrorCreatingFiles()

    if files:
        db_conn.files.insert(files)


def dal_rate_material(form, product_id, material_name):
    #ref
    try:
        token = form[JWT]
        payload = jwt.decode(token, SECRET)

    except Exception:
        raise WrongCredentials()

    if payload[ROLE] != CONSUMER:
        raise InvalidRole()

    try:
        rate = form[RATE]
    except Exception:
        raise BadFormData()
    #ref

    try:
        rateInt = float(float(rate))
    except Exception:
        raise FloatingPointError()

    if rateInt > 5 or rateInt < 1:
        raise ValueError()

    user_has_voted = db_conn.files.find_one({
        OWNER: str(product_id),
        MATERIAL_ID: material_name,
        '%s.%s' % (RATES, USERNAME): payload[USERNAME]
    })

    if user_has_voted:
        updated = db_conn.files.find_one_and_update(
            {OWNER: str(product_id), MATERIAL_ID: material_name,
             '%s.%s' % (RATE, USERNAME): payload[USERNAME]},
            {'$set': {'%s.$.%s' % (RATES, RATE): rateInt}},
            return_document=ReturnDocument.AFTER
        )
    else:
        updated = db_conn.files.find_one_and_update(
            {OWNER: str(product_id), MATERIAL_ID: material_name},
            {'$inc': {VOTES: 1}, '$push': {
                RATES: {USERNAME: payload[USERNAME], RATE: rateInt}}},
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

    return total_vote_value, vote_amount

