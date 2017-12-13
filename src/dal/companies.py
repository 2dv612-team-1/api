from .mongo_client import db_conn
from utils.string import *
from config import *
import jwt

"""Create company account, if company account with given username and password does not already exist"""


def create_company(form):
    token = form[JWT]
    payload = jwt.decode(token, SECRET)

    if payload[ROLE] == ADMIN:
        username = form[USERNAME]
        password = form[PASSWORD]
    else:
        raise AttributeError()

    if db_conn.users.find({USERNAME: username}).count() != 0:
        return True
    else:

        company = {
            USERNAME: username,
            PASSWORD: password,
            ROLE: COMPANY
        }

        db_conn.users.insert(company)
        return False


def get_representatives_for_company(company_name):
    if db_conn.users.find_one({USERNAME: company_name}):

        representatives = []

        for representative in db_conn.users.find({DATA:{OWNER: company_name}}):
            representatives.append({USERNAME: representative[USERNAME]})

        return representatives

    else:
        raise AttributeError()


def dal_create_representative(form, owner):

    token = form[JWT]
    payload = jwt.decode(token, SECRET)

    if payload[ROLE] == COMPANY:
        username = form[USERNAME]
        password = form[PASSWORD]
    else:
        raise AttributeError()

    if db_conn.users.find({USERNAME: username}).count() != 0:
        return True
    else:

        representative = {
            USERNAME: username,
            PASSWORD: password,
            ROLE: REPRESENTATIVE,
            DATA: {OWNER: owner}
        }

        db_conn.users.insert(representative)
        return False

def get_products_for_company(name):

    user = db_conn.users.find_one({USERNAME: name})
    owner = user[DATA][OWNER]

    products = []
    for product in db_conn.products.find({PRODUCER: owner}):
        products.append(str(product))

    return products
