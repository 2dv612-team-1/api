from pymongo import MongoClient
from config import *

""" Data Access Layer

    self.db_conn            => client.api
    self.db_conn.users      => users collection
    self.db_conn.admin      => admin collection
    self.db_conn.categories => categories collection

    self.db_conn.products   => products collection
"""

client = MongoClient(MONGO)
db_conn = client.api