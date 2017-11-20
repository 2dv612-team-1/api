from main import app
from pymongo import MongoClient
import unittest
import json

class UsersTest(unittest.TestCase):

    def setUp(self):
        client = MongoClient('mongodb:27017')
        self.__db_users = client.api.users
        self.__app = app.test_client()
        self.__app.testing = True;
        self.__test_data = []
        self.__createTestData()
        self.__saveTestDataToDB()

    def tearDown(self):
        self.__deleteTestDataInDB()
    
    def test_insertedData(self):
        user = self.__db_users.find_one({'username': 'admin'})
        self.assertEqual(user['password'], '1234')

    def __createTestData(self):
        company_dict = {'Dell' :{ 'username' : 'userDell', 'password' : 'passDell'},
                        'Apple':{'username' : 'userApple', 'password': 'passApple'}}

        self.__test_data.append({'username' : 'admin', 'password' : '1234', 'role' : 'admin', 'data' : company_dict})
    
    def __saveTestDataToDB(self):
        for user in self.__test_data:
            self.__db_users.insert(user)

    def __deleteTestDataInDB(self):
        for user in self.__test_data:
            self.__db_users.remove(user)

if __name__ == '__main__':
    unittest.main()