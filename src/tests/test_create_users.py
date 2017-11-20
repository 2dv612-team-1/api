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
    
    def test_checkForRole(self):
        for user in self.__db_users.find():
            if user['role'] == 'admin':
                self.__testinsertedAdminData(user)
            elif user['role'] == 'consumer':
                self.__testinsertedConsumerData(user)
            else:
                pass

    def __testinsertedConsumerData(self, user):
        self.assertEqual(user['password'], 'consumer1')
        self.assertEqual(len(user['data']['Manuals']), 3)

    def __testinsertedAdminData(self, user):
        self.assertEqual(user['password'], '1234')
        self.assertEqual(user['data']['Dell']['username'], 'userDell')

    def __createTestData(self):
        """" Consumer Data """
        consumer_data = {'PersonalInfo':{'name' : 'Eggbert', 'age' : 34},
                        'Manuals': ('manual_1', 'manual_2', 'manual_2')}


        self.__test_data.append({'username' : 'consumer1', 'password' : 'consumer1', 'role' : 'consumer', 'data' : consumer_data})

        """ Admin Data """
        admin_data = {'Dell' :{ 'username' : 'userDell', 'password' : 'passDell'},
                        'Apple':{'username' : 'userApple', 'password': 'passApple'}}

        self.__test_data.append({'username' : 'admin', 'password' : '1234', 'role' : 'admin', 'data' : admin_data})

    def __saveTestDataToDB(self):
        for user in self.__test_data:
            self.__db_users.insert(user)

    def __deleteTestDataInDB(self):
        for user in self.__test_data:
            self.__db_users.remove(user)

if __name__ == '__main__':
    unittest.main()