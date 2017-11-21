from unittest import TestCase
from main import APP
from pymongo import MongoClient
from db_helper import DBHelper


class BaseTest(TestCase):

    def setUp(self):
        client = MongoClient('mongodb:27017')
        self._db_helper = DBHelper(client.api.users)
        self._app = APP.test_client()
        self._app.testing = True

    def tearDown(self):
        self._db_helper.deleteTestDataInDB()