from pymongo import MongoClient

client = MongoClient('mongodb:27017')
db_conn = client.api