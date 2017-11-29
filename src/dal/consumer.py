from .mongo_client import db_conn
from utils.response import response

"""Create consumer account, if consumer account with given username and password does not already exist"""


def create_consumer(form):
    username = form['username']
    password = form['password']

    if db_conn.users.find({'username': username}).count() != 0:
        return True
    else:

        user = {
            'username': username,
            'password': password,
            'role': 'consumer'
        }

        db_conn.users.insert(user)
        return False

