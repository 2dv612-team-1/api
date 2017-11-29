from mongo_client import db_conn


"""Auth user by comparing username and password in users collection"""


def auth_and_return_user(form):

    found_user = db_conn.users.find_one({'username': form['username'], 'password': form['password']})
    return found_user


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
    return users