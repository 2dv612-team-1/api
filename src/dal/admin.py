from .mongo_client import db_conn
from utils.string import *
from utils.jwt_handler import *
from config import *

"""
    db_conn.admin   => client.api.admin
"""

def auth_and_return_admin(form):
    """Auth admin by comparing username and password in admin collection"""
    username = form[USERNAME]
    password = form[PASSWORD]

    found_admin = db_conn.admin.find_one({USERNAME: username, PASSWORD: password})

    if found_admin:
        payload = {USERNAME: found_admin[USERNAME], ROLE: ADMIN}
        encoded = encode(payload)
        return encoded

    else:
        raise AttributeError()




def create_default_admin():
    """Creates default admin account in admin collection"""
    default_admin = {
        USERNAME: 'admin',
        PASSWORD: 'admin123',
        ROLE: ADMIN
    }

    db_conn.admin.update({}, default_admin, upsert=True)
