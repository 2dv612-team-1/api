from .mongo_client import db_conn
from utils.string import *
import jwt

"""
    db_conn.admin   => client.api.admin
"""

"""Auth admin by comparing username and password in admin collection"""


def auth_and_return_admin(form):
    username = form[USERNAME]
    password = form[PASSWORD]

    found_admin = db_conn.admin.find_one({USERNAME: username, PASSWORD: password})

    if found_admin:
        payload = {USERNAME: found_admin[USERNAME], ROLE: ADMIN}
        encoded = jwt.encode(payload, 'super-secret')
        return encoded

    else:
        raise AttributeError()


"""Creates default admin account in admin collection"""


def create_default_admin():
    default_admin = {
        USERNAME: 'admin',
        PASSWORD: 'admin123',
        ROLE: ADMIN
    }

    db_conn.admin.update({}, default_admin, upsert=True)