from .mongo_client import db_conn
from utils.string import *

"""Create consumer account, if consumer account with given username and password does not already exist"""


def create_consumer(form):
    username = form[USERNAME]
    password = form[PASSWORD]

    if db_conn.users.find({USERNAME: username}).count() != 0:
        return True
    else:

        user = {
            USERNAME: username,
            PASSWORD: password,
            ROLE: CONSUMER
        }

        db_conn.users.insert(user)
        return False
