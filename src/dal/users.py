from .mongo_client import db_conn
from utils.string import *
from config import *
import jwt

"""
    db_conn.users   => client.api.users
"""

"""Auth user by comparing username and password in users collection"""


def auth_and_return_user(form):
    username = form[USERNAME]
    password = form[PASSWORD]

    found_user = db_conn.users.find_one(
        {USERNAME: username, PASSWORD: password})

    try:
        data = found_user[DATA]
    except Exception as e:
        data = {}

    if found_user:
        payload = {USERNAME: found_user[USERNAME],
                   ROLE: found_user[ROLE], DATA: data}
        encoded = jwt.encode(payload, SECRET)
        return encoded, found_user[ROLE]

    else:
        raise AttributeError()


"""Search for user by username"""


def check_user_token(token):
    payload = jwt.decode(token, SECRET)
    username = payload.get(USERNAME)

    found_user = db_conn.users.find_one({USERNAME: username})
    if found_user:
        return username
    else:
        return AttributeError()


"""Iterates users collection and returns dict of usernames with role"""


def get_users_with_role(role):
    users = []
    for user in db_conn.users.find({ROLE: role}):
        users.append({USERNAME: user[USERNAME]})

    return users
  
def get_user(username):
    #TODO: Filter out password and any other private data
    return db_conn.users.find_one({'username': username})
