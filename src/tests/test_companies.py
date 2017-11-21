import unittest

from main import APP
from pymongo import MongoClient

from db_helper import DBHelper
import jwt
import json

"""Test for (sprint-1) companies routes"""


class CompaniesTestCase(unittest.TestCase):

    def setUp(self):
        client = MongoClient('mongodb:27017')
        self.__db_helper = DBHelper(client.api.users)
        self.__app = APP.test_client()
        self.__app.testing = True

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

    """ Removed from company route
    def test_authAsAdmin(self):
        response_auth = self.__app.post('/companies/auth',
                                        data=dict({'username': 'admin', 'password': '1234'}),
                                        content_type='application/x-www-form-urlencoded')

        result_auth = json.loads(response_auth.data.decode())
        self.assertEqual(response_auth.status_code, 200)
        self.assertEqual(result_auth['message'], 'Successfully logged in as company')
        self.assertTrue(result_auth['token'])
    """

    def test_addingCompanyAccountAsAdmin(self):
        username_comp = 'userDell'
        password_comp = 'passDell'

        encoded_data = jwt.encode({'role': 'admin'}, 'super-secret')
        response_auth = self.__app.post('/companies',
                                        data=dict({'username': username_comp, 'password': password_comp, 'jwt': encoded_data}))

        if self.__db_helper.companyExistInDB(username_comp):
            self.assertEqual(response_auth.status_code, 409)
        else:
            self.assertEqual(response_auth.status_code, 201)

if __name__ == '__main__':
    unittest.main()

