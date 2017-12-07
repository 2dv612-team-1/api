from .mongo_client import db_conn


def get_products(name):
    """Gets products from db

    Will either get all products or based on filter (eg: {'producer': <company-name>})

    Returns:
        list -- products found in db
    """

    products = []
    for product in db_conn.products.find({'producer': name}):
        products.append(str(product))

    return products
