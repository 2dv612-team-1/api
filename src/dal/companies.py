from .mongo_client import db_conn
from utils.string import *
from utils.form_handler import *
from config import *
from exceptions.AlreadyExists import AlreadyExists

"""Create company account, if company account with given username and password does not already exist"""


def create_company(request):

    try:
        username = extract_attribute(request, USERNAME)
        password = extract_attribute(request, PASSWORD)
    except Exception as e:
        raise e

    if db_conn.users.find({USERNAME: username}).count() != 0:
        raise AlreadyExists('Username is already in use')

    company = {
        USERNAME: username,
        PASSWORD: password,
        ROLE: COMPANY,
        UNREAD: list()
    }

    company_id = db_conn.users.insert(company)
    new_company = {NAME: username, ID: str(company_id)}
    return new_company


def get_representatives_for_company(company_name):
    if db_conn.users.find_one({USERNAME: company_name}):

        representatives = []

        for representative in db_conn.users.find({DATA: {OWNER: company_name}}):
            representatives.append({USERNAME: representative[USERNAME]})

        return representatives

    else:
        raise AttributeError()


def dal_create_representative(request, owner):

    try:
        username = extract_attribute(request, USERNAME)
        password = extract_attribute(request, PASSWORD)
    except Exception as e:
        raise e

    if db_conn.users.find({USERNAME: username}).count() != 0:
        raise AlreadyExists('Username is already in use')

    representative = {
        USERNAME: username,
        PASSWORD: password,
        ROLE: REPRESENTATIVE,
        DATA: {OWNER: owner}
    }

    rep_id = db_conn.users.insert(representative)
    new_rep = {USERNAME: username, ID: str(rep_id)}
    return new_rep


def dal_add_unread(form, thread_id):
    products = db_conn.products.find({CATEGORY: form[CATEGORY]})
    producers = list(map(lambda product: product[PRODUCER], products))
    for producer in producers:
        db_conn.users.find_one_and_update({USERNAME: producer}, {
            '$push': {UNREAD: thread_id}
        })


def get_products_for_company(name):

    try:
        products = db_conn.products.find({PRODUCER: name})
    except Exception:
        raise AttributeError('Cannot get company products')

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


def dal_read_thread(thread_id, company_name):
    """Checks thread as read"""

    try:
        db_conn.users.find_one_and_update(
            {USERNAME: company_name},
            {'$pull': {UNREAD: thread_id}}
        )
    except Exception:
        raise AttributeError('There is nothing to read')
