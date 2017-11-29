from mongo_client import db_conn
import jwt

"""Create company account, if company account with given username and password does not already exist"""


def create_company(form):
    token = form['jwt']
    payload = jwt.decode(token, 'super-secret')

    if payload['role'] == 'admin':
        username = form['username']
        password = form['password']
    else:
        return AttributeError()

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
