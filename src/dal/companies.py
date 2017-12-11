from .mongo_client import db_conn
import jwt

"""Create company account, if company account with given username and password does not already exist"""


def create_company(form):
    token = form['jwt']
    payload = jwt.decode(token, 'super-secret')

    if payload['role'] == 'admin':
        username = form['username']
        password = form['password']
    else:
        raise AttributeError()

    if db_conn.users.find({'username': username}).count() != 0:
        return True
    else:

        company = {
            'username': username,
            'password': password,
            'role': 'company'
        }

        db_conn.users.insert(company)
        return False


def get_representatives_for_company(company_name):
    if db_conn.users.find_one({'username': company_name}):

        representatives = []

        for representative in db_conn.users.find({'data':{'owner': company_name}}):
            representatives.append({'username': representative['username']})

        return representatives

    else:
        raise AttributeError()


def dal_create_representative(form, owner):

    token = form['jwt']
    payload = jwt.decode(token, 'super-secret')

    if payload['role'] == 'company':
        username = form['username']
        password = form['password']
    else:
        raise AttributeError() #Need custom return to trigger 'You are not a company' response in route

    if db_conn.users.find({'username': username}).count() != 0:
        return True
    else:

        representative = {
            'username': username,
            'password': password,
            'role': 'representative',
            'data': {'owner': owner}
        }

        db_conn.users.insert(representative)
        return False

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
        products.append(str(product))

    return products