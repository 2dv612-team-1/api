import unittest

from main import APP
from pymongo import MongoClient

from db_helper import DBHelper

import json

"""Test for (sprint-1) companies routes"""


class CompaniesTestCase(unittest.TestCase):

    def setUp(self):
        client = MongoClient('mongodb:27017')
        self.__db_helper = DBHelper(client.api.companies)#companies coll!
        self.__app = APP.test_client()
        self.__app.testing = True;

    def tearDown(self):
        self.__db_helper.deleteTestDataInDB()

    def test_getCompaniesOnEmptyCollection(self):
        self.__db_helper.deleteTestDataInDB()
        response = self.__app.get('/companies')
        self.assertEqual(response.status_code, 200)
        self.__db_helper.addTestDataToDB()

    def test_getCompaniesOnPopulatedCollection(self):
        response = self.__app.get('/companies')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) != 0)

    def test_getToken(self):
        response = self.__app.post('/companies/auth', data=dict({'username': 'admin', 'password': '1234'}), content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

