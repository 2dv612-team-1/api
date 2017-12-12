from .mongo_client import db_conn
from utils.string import *


def get_products(name):
    """Gets products from db

    Will either get all products or based on filter (eg: {'producer': <company-name>})

    Returns:
        list -- products found in db
    """

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
