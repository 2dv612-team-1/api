from pymongo import MongoClient

""" Super Data Access Layer

    self.db_conn            => client.api
    self.db_conn.users      => users collection
    self.db_conn.admin      => admin collection
    self.db_conn.categories => categories collection
    
    self.db_conn.products   => products collection      {'  _id:autogen
                                                            filepath':uploads/filename,
                                                            'title/display name': random title
                                                            'owner':company name,
                                                            'category':category name}
"""

class SuperDAL:
    def __init__(self):
        client = MongoClient('mongodb:27017')
        self.db_conn = client.api

    """Iterates users collection and returns list of usernames with role of representatives"""
    def get_representatives_for_company(self, company_username):
        representatives = []
        for representative in self.db_conn.users.find({'owner': company_username}):
            representatives.append({'username': representative['username']})
        return representatives

    # not used in route
    def get_categories(self):
        categories_data = []
        for category in self.db_conn.categories.find():
            categories_data.append({
                'category': category.get('category'),
                '_id': str(category.get('_id'))
            })

        return categories_data

    # not used in route
    def create_category(self, category):
        if self.db_conn.categories.find({'category': category}).count() != 0:
            return True
        else:
            self.db_conn.categories.insert({'category': category})
            return False

    # todo
    def get_products(self):
        pass

    # todo
    def create_product(self):
        pass

    """Create representative account, if representative account with given username and password does not already exist"""
    def create_representative(self, username, password, owner):
        if self.db_conn.users.find({'username': username}).count() != 0:
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

    """Create consumer account, if consumer account with given username and password does not already exist"""
    def create_consumer(self, username, password):

        if self.db_conn.users.find({'username': username}).count() != 0:
            return True
        else:

            user = {
                'username': username,
                'password': password,
                'role': 'consumer'
            }

            self.db_conn.users.insert(user)
            return False
