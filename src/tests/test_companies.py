from main import APP
from pymongo import MongoClient
import unittest
import json

class CompaniesTestCase(unittest.TestCase):

    def setUp(self):
        client = MongoClient('mongodb:27017')
        self.__db_users = client.api.users
        self.app = APP.test_client()
        self.app.testing = True;

    def tearDown(self):
        pass

    def test_getCompanies(self):
        companiesExistInDB = self.__checkIfCompaniesCollectionHasContent()
        response = self.app.get('/companies')

        if companiesExistInDB:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 200)
    
    def __checkIfCompaniesCollectionHasContent(self):
        if (self.__db_users.find().count() != 0):
            companiesExist = True;
        else:
            companiesExist = False;
        return companiesExist

    def __addCompany(self):
        pass

    def __removeCompany(self):
        pass

    def __addCompanies(self):
        pass
    
    def __removeCompanies(self):
        pass

if __name__ == '__main__':
    unittest.main()
