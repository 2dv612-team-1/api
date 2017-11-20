
from routes.companies import db
from main import app
import unittest

class CompaniesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True;

    def tearDown(self):
        pass

    def test_getCompanies(self):
        companiesExistInDB = self.__checkIfCompaniesHasContent()
        response = self.app.get('/companies')

        if companiesExistInDB:
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 200)
    
    def __checkIfCompaniesCollectionHasContent(self):
        if (db.companies.find().count() != 0):
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
