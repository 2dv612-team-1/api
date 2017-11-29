from mongo_client import db_conn


"""Auth user by comparing username and password in users collection"""


def auth_and_return_user(request):
    username = request.form['username']
    password = request.form['password']

    found_user = db_conn.users.find_one({'username': username, 'password': password})
    return found_user
