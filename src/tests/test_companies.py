import unittest
import jwt
from basetest import BaseTest

class CompaniesTestCase(BaseTest):

    def test_getCompaniesOnEmptyCollection(self):
        self._db_helper.deleteTestDataInDB()
        response = self._app.get('/companies')
        self.assertEqual(response.status_code, 200)
        self._db_helper.addTestDataToDB()

    def test_getCompaniesOnPopulatedCollection(self):
        response = self._app.get('/companies')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) != 0)

    def test_addingCompanyAccountAsAdmin(self):
        username_comp = 'userDell'
        password_comp = 'passDell'

        encoded_data = jwt.encode({'role': 'admin'}, 'super-secret')
        response_auth = self._app.post('/companies',
                                        data=dict({'username': username_comp, 'password': password_comp, 'jwt': encoded_data}))

        if self._db_helper.userExistInDB(username_comp):
            self.assertEqual(response_auth.status_code, 409)
        else:
            self.assertEqual(response_auth.status_code, 201)

if __name__ == '__main__':
    unittest.main()

