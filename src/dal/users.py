from mongo_client import db_conn
import jwt

"""
    db_conn.users   => client.api.users
"""

"""Auth user by comparing username and password in users collection"""

#returns role and encoded
def auth_and_return_user(form):
    username = form['username']
    password = form['password']

    found_user = db_conn.users.find_one({'username': username, 'password': password})

    if found_user:
        payload = {'username': found_user['username'], 'role': found_user['role']}
        encoded = jwt.encode(payload, 'super-secret')
        return encoded, found_user['role']

    else:
        return AttributeError()


"""Search for user by username"""

# add token and handle
def find_user_by_name(name):
    found_user = db_conn.users.find_one({'username': name})
    return found_user


"""Iterates users collection and returns dict of usernames with role"""


def get_users_with_role(form):
    users = []
    for user in db_conn.users.find({'role': form['role']}):
        users.append({'username': user['username']})

    return response('Successfully extracted all users', 200,{'users': users})