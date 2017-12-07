from .mongo_client import db_conn


def get_products(name):
    """Gets products from db

    Will either get all products or based on filter (eg: {'producer': <company-name>})

    Returns:
        list -- products found in db
    """

    user = db_conn.users.find_one({'username': name})
    owner = user['data']['owner']

    products = []
    for product in db_conn.products.find({'producer': owner}):
        products.append({
            'category': product.get('category'),
            'name': product.get('name'),
            'description': product.get('description'),
            '_id': str(product.get('_id')),
            'subcategory': product.get('subcategory'),
            'serialNo': product.get('serialNo'),
            'createdBy': product.get('createdBy'),
            'producer': product.get('producer')
        })

    return products
