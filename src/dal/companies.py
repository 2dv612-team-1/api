from .mongo_client import db_conn
from utils.string import *
from utils.form_handler import *
from config import *
from exceptions.AlreadyExists import AlreadyExists
# import jwt

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
        ROLE: COMPANY
    }

    company_id = db_conn.users.insert(company)
    new_company = {NAME: username, ID: str(company_id)}
    return new_company


def get_representatives_for_company(company_name):
    if db_conn.users.find_one({USERNAME: company_name}):

        representatives = []

        for representative in db_conn.users.find({DATA:{OWNER: company_name}}):
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
