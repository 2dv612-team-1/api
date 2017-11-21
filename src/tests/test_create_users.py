from main import APP
from pymongo import MongoClient
from db_helper import DBHelper
import unittest

"""Very simple tests writing and reading """


class UsersTest(unittest.TestCase):

    def setUp(self):
        client = MongoClient('mongodb:27017')
        self.__db_helper = DBHelper(client.api.users)#users coll!
        self.__app = APP.test_client()
        self.__app.testing = True

    def tearDown(self):
        self.__db_helper.deleteTestDataInDB()
    
    def test_runTestDepOnRole(self):
        for user in self.__db_helper.getUsers():
            if user['role'] == 'admin':
                self.__testInsertedAdminData(user)
            elif user['role'] == 'consumer':
                self.__testInsertedConsumerData(user)
            elif user['role'] == 'company':
                self.__testInsertedCompanyData(user)
            elif user['role'] == 'representative':
                self.__testInsertedRepresentativeData(user)
                self.__findCompanyForRepresentative(user)
            else:
                pass
    
    def __findCompanyForRepresentative(self, user):
        if user['username'] == 'rep1':
            self.assertEqual(user['data']['company'], 'Dell')

    def __testInsertedRepresentativeData(self, user):
        self.assertEqual(user['password'], user['username'])

    def __testInsertedConsumerData(self, user):
        self.assertEqual(user['password'], 'consumer1')
        self.assertEqual(len(user['data']['Manuals']), 3)

    def __testInsertedAdminData(self, user):
        self.assertEqual(user['password'], '1234')
        self.assertEqual(user['data']['Dell']['username'], 'userDell')
    
    def __testInsertedCompanyData(self, user):
        self.assertEqual(user['password'], 'passDell')
        self.assertEqual(len(user['data']['Representatives']), 3)


if __name__ == '__main__':
    unittest.main()