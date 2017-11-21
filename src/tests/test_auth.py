import unittest

from main import APP
from pymongo import MongoClient

from db_helper import DBHelper
import json


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        client = MongoClient('mongodb:27017')
        self.__db_helper = DBHelper(client.api.users)
        self.__app = APP.test_client()
        self.__app.testing = True

    def tearDown(self):
        self.__db_helper.deleteTestDataInDB()

    def test_authAsAdmin(self):
        response_auth = self.__app.post('/auth',
                                        data=dict({'username': 'admin', 'password': '1234'}))
        auth_data = json.loads(response_auth.data)
        self.assertEqual(response_auth.status_code, 200)
        self.assertEqual(auth_data['message'], 'Successfully logged in as ' + self.__db_helper.getRoleForUser('admin')['role'])
        self.assertTrue(auth_data['token'])