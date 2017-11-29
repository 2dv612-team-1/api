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
