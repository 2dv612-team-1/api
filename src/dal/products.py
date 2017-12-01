from .mongo_client import db_conn
#ToDO

def dal_get_products(self, filter={}):
    """Gets products from db

    Will either get all products or based on filter (eg: {'producer': <company-name>})

    Returns:
        list -- products found in db
    """

    products = []
    for product in self.db_conn.products.find(filter):
        product.update({'_id': str(product['_id'])})
        products.append(product)

    return products