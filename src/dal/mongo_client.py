from pymongo import MongoClient

""" Data Access Layer

    self.db_conn            => client.api
    self.db_conn.users      => users collection
    self.db_conn.admin      => admin collection
    self.db_conn.categories => categories collection

<<<<<<< HEAD
    self.db_conn.products   => products collection      {'  _id:autogen
                                                            filepath':uploads/filename,
                                                            'title/display name': random title
                                                            'owner':company name,
                                                            'category':category name} ?
=======
    self.db_conn.products   => products collection
>>>>>>> origin/master
"""

client = MongoClient('mongodb:27017')
db_conn = client.api