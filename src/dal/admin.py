from mongo_client import db_conn

"""Auth admin by comparing username and password in admin collection"""


def auth_and_return_admin(request):
    username = request.form['username']
    password = request.form['password']

    found_admin = db_conn.admin.find_one({'username': username, 'password': password})
    return found_admin