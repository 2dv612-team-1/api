"""
Data Access Layer/Object
"""

from pymongo import MongoClient


class DAO:

    def __init__(self):
        self.CLIENT = MongoClient('mongodb:27017')
        self.DB = self.CLIENT.api

    def get(self, collection_name):
        """Get all"""

        result = []
        collection = self.DB[collection_name]
        items = collection.find()

        for item in items:
            result.append({'username': item['username']})
        return result

    def create(self, collection_name, item):
        """Creates"""

    def get_by_id(self, collection_name, item):
        """Get one"""

    def update(self, collection_name, item, item_id):
        """Updates"""

    def delete(self, collection_name, item_id):
        """Deletes"""
