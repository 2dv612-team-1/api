from pymongo import MongoClient

"""Super Data Access Layer"""

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

    """Iterates users collection and returns list of usernames with role => company"""
    def get_companies(self):
        companies = []
        for company in self.db_conn.users.find({'role': 'company'}):
            companies.append({'username': company['username']})
        return companies

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