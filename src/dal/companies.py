from mongo_client import db_conn

"""Create company account, if company account with given username and password does not already exist"""


def create_company(self, username, password):
    if self.db_conn.users.find({'username': username}).count() != 0:
        return True
    else:

        company = {
            'username': username,
            'password': password,
            'role': 'company'
        }

        self.db_conn.users.insert(company)
        return False
