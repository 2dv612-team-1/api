"""
Data Access Layer/Object
"""

from pymongo import MongoClient

# CLIENT = MongoClient('mongodb:27017')
# DB = CLIENT.api

class DAO:

  def __init__(self):
    self.CLIENT = MongoClient('mongodb:27017')
    self.DB = self.CLIENT.api

  def get(self, collection_name):
    result = []
    collection = self.DB[collection_name]
    items = collection.find()
    for item in items:
      result.append({'username': item['username']})
    return result
