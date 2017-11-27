import unittest
import jwt
from basetest import BaseTest

#Done
"""Creates company"""
"""Extracts companies"""
"""Gets list of representatives from specific company"""
"""Creates representative"""

# Todo
# Pick test values from db!
# Server crash when sending wrong secret: jwt.exceptions.DecodeError: Signature verification failed

class CompaniesTestCase(BaseTest):

    #Test @COMPANIES.route('/companies')
    def test_getCompaniesOnEmptyCollection(self):
        self._db_helper.deleteAllTestDataInDB()
        response = self._app.get('/companies')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self._db_helper.getUsers().count() == 0)
        self._db_helper.addTestDataToDB()

    #Test @COMPANIES.route('/companies')
    def test_getCompaniesOnPopulatedCollection(self):
        response = self._app.get('/companies')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self._db_helper.getUsers().count() != 0)

    #Test @COMPANIES.route('/companies', methods=['POST'])
    def test_creatingNewCompanyAccountAsAdmin(self):
        comp_username, comp_password = self._getRandomUserNameAndPasswordOflenEight()
        response_data = self._getResponseDataFromPostRequest('/companies', 'admin', comp_username, comp_password)

        self.assertEqual(response_data['status'], 201)
        self.assertTrue(self._db_helper.deleteOneUserTestData(comp_username))

    #Test @COMPANIES.route('/companies', methods=['POST'])
    def test_creatingAlreadyExisingCompanyAccountAsAdmin(self):
        user_comp = self._db_helper.getFirstUserNameAndPasswordFromRole('company')
        response_data = self._getResponseDataFromPostRequest('/companies', 'admin', user_comp['username'], user_comp['password'])

        self.assertEqual(response_data['status'], 409)
        self.assertEqual(response_data['message'], 'Username already exists')

    #Test @COMPANIES.route('/companies', methods=['POST'])
    def test_creatingNewCompanyAccountAsOtherRolesThenAdmin(self):
        roles_to_test = [role for role in self._db_helper.getRoles() if role != 'admin']
        for role in roles_to_test:
            comp_username, comp_password = self._getRandomUserNameAndPasswordOflenEight()
            response_data = self._getResponseDataFromPostRequest('/companies', role, comp_username, comp_password)

            self.assertEqual(response_data['status'], 400)
            self.assertEqual(response_data['message'], 'You have to be an admin to create company')

    #Test @COMPANIES.route('/companies/<name>/representatives')
    def test_getListOfRepresentativesFromInvalidCompanyUsername(self):
        response = self._app.get('/companies/' + 'invalid_username' + '/representatives')

        self.assertEqual(response.status_code, 400)

    #Test @COMPANIES.route('/companies/<name>/representatives')
    def test_getListOfRepresentativesFromValidCompanyName(self):
        response = self._app.get('/companies/' + 'userDell' + '/representatives')

        self.assertEqual(response.status_code, 200)

    #Test @COMPANIES.route('/companies/<name>/representatives', methods=['POST'])
    def test_createRepresentativeAsValidCompanyRepresentativeExist(self):
        path = '/companies/' + 'userDell' + '/representatives'
        response_data = self._getResponseDataFromPostRequest(path, 'company', 'rep1', 'rep1')

        self.assertEqual(response_data['status'], 409)
        self.assertEqual(response_data['message'], 'Username already exists')

    #Test @COMPANIES.route('/companies/<name>/representatives', methods=['POST'])
    def test_createRepresentativeAsValidCompanyRepresentativeDoesNotExist(self):
        path = '/companies/' + 'userDell' + '/representatives'
        response_data = self._getResponseDataFromPostRequest(path, 'company', 'new_username', 'new_username')

        self.assertEqual(response_data['status'], 201)
        self.assertEqual(response_data['message'], 'Representative was created')
        self.assertTrue(self._db_helper.deleteOneUserTestData('new_username'))

    #Test @COMPANIES.route('/companies/<name>/representatives', methods=['POST'])
    def test_createRepresentativeAsInvalidCompanyRepresentativetExist(self):
        path = '/companies/' + 'invalid_company' + '/representatives'
        response_data = self._getResponseDataFromPostRequest(path, 'consumer', 'rep1', 'rep1')

        self.assertEqual(response_data['status'], 400)
        self.assertEqual(response_data['message'], 'You are not a company')

    #Test @COMPANIES.route('/companies/<name>/representatives', methods=['POST'])
    def test_createRepresentativeAsInvalidCompanyRepresentativeDoesNotExist(self):
        path = '/companies/' + 'invalid_company' + '/representatives'
        response_data = self._getResponseDataFromPostRequest(path, 'consumer', 'new_username', 'new_username')

        self.assertEqual(response_data['status'], 400)
        self.assertEqual(response_data['message'], 'You are not a company')

    """ jwt.exceptions.DecodeError: Signature verification failed
        Cant get response: "return response('Wrong credentials', 400)" from route
    """
    #Test @COMPANIES.route('/companies/<name>/representatives', methods=['POST'])
    def test_createRepresentativeAsInvalidCompanyRepresentativeDoesNotExistWrongCredentials(self):
        path = '/companies/' + 'invalid_company' + '/representatives'

        encoded_data = jwt.encode({'role': 'consumer'}, 'wrong-secret')
        # response_data = self.__getResponseDataFromPostRequest(path, 'consumer', 'new_username', 'new_username', encoded_data)

        #self.assertEqual(response_data['status'], 400)
        #self.assertEqual(response_data['message'], 'You are not a company')

if __name__ == '__main__':
    unittest.main()

