from pymongo import MongoClient

""" Super Data Access Layer

    self.db_conn        => client.api
    self.db_conn.users  => users collection
    self.db_conn.admin  => admin collection
"""

class SuperDAL:
    def __init__(self):
        client = MongoClient('mongodb:27017')
        self.db_conn = client.api

    """Auth user by comparing username and password"""
    def auth_and_return_user(self, username, password):
        found_user = self.db_conn.users.find_one({'username': username, 'password': password})
        return found_user

    """Search for user by username"""
    def find_user_by_name(self, username):
        found_user = self.db_conn.users.find_one({'username': username})
        return found_user

    """Iterates users collection and returns dict of usernames with assigned role"""
    def get_users_with_role(self, role):
        users = []
        for user in self.db_conn.users.find({'role': role}):
            users.append({'username': user['username']})
        return users

    """Iterates users collection and returns list of usernames with role of representatives"""
    def get_representatives(self, company_username):
        representatives = []
        for representative in self.db_conn.users.find({'owner': company_username}):
            representatives.append({'username': representative['username']})
        return representatives

    """Create representative account, if representative account with given username and password does not already exist"""
    def create_representative(self, username, password, owner):
        if self.db_conn.users.find_one({'username': username}):
            return True
        else:

            representative = {
                'username': username,
                'password': password,
                'owner': owner,
                'role': 'representative'
            }

            self.db_conn.users.insert(representative)

        return False

    """Create company account, if company account with given username and password does not already exist"""
    def create_company(self, username, password):

        if self.db_conn.users.find_one({'username': username}):
            return True
        else:

            company = {
                'username': username,
                'password': password,
                'role': 'company'
            }

            self.db_conn.users.insert(company)

        return False

    """Create consumer account, if consumer account with given username and password does not already exist"""
    def create_consumer(self, username, password):

        if self.db_conn.users.find_one(username):
            return True
        else:

            user = {
                'username': username,
                'password': password,
                'role': 'consumer'
            }

            self.db_conn.users.insert(user)

        return False