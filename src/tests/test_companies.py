import unittest
import jwt
import json
from basetest import BaseTest


class CompaniesTestCase(BaseTest):

    def test_getCompaniesOnEmptyCollection(self):
        self._db_helper.deleteAllTestDataInDB()
        response = self._app.get('/companies')
        self.assertEqual(response.status_code, 200)
        self._db_helper.addTestDataToDB()

    def test_getCompaniesOnPopulatedCollection(self):
        response = self._app.get('/companies')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) != 0)

    def test_creatingNewCompanyAccountAsAdmin(self):
        comp_username, comp_password = self._getRandomUserNameAndPasswordOflenEight()
        response_data = self.__getResponseDataFromPostRequest('admin', comp_username, comp_password)
        self.assertEqual(response_data['status'], 201)
        self.assertTrue(self._db_helper.deleteOneUserTestData(comp_username))

    def test_creatingAlreadyExisingCompanyAccountAsAdmin(self):
        user_comp = self._db_helper.getFirstUserNameAndPasswordFromRole('company')
        response_data = self.__getResponseDataFromPostRequest('admin', user_comp['username'], user_comp['password'])
        self.assertEqual(response_data['status'], 409)
        self.assertEqual(response_data['message'], 'Username already exists')

    def test_creatingNewCompanyAccountAsOtherRolesThenConsumer(self):
        roles_to_test = [role for role in self.roles if role != 'admin']
        for role in roles_to_test:
            comp_username, comp_password = self._getRandomUserNameAndPasswordOflenEight()
            response_data = self.__getResponseDataFromPostRequest(role, comp_username, comp_password)
            self.assertEqual(response_data['status'], 400)
            self.assertEqual(response_data['message'], 'You have to be an admin to create company')


    def __getResponseDataFromPostRequest(self, as_role, username, password):
        encoded_data = jwt.encode({'role': as_role}, 'super-secret')
        response_auth = self._app.post('/companies', data=dict({'username': username,
                                                       'password': password,
                                                       'jwt': encoded_data}))
        return json.loads(response_auth.data)

if __name__ == '__main__':
    unittest.main()

