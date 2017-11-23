import json
from basetest import BaseTest

#Done
#"""Authenticates any user"""

#Todo fix database corr, add test for limiter

class AuthTestCase(BaseTest):

    #Test @AUTH.route('/auth', methods=['POST'])
    def test_authEveryUserInDB(self):
        for user in self._db_helper.getUsers():
            self.__authWithValidUserCredentials(user['username'], user['password'])

    #Test @AUTH.route('/auth', methods=['POST'])
    def test_authWithInvalidUsernameAndPassword(self):
        random_username, random_password = self._getRandomUserNameAndPasswordOflenEight()
        auth_data = self.__getResponseDataFromPostRequest(random_username, random_password)

        #Need simple check with db before asserts
        self.assertEquals(auth_data['status'], 400)
        self.assertEqual(auth_data['message'],'Wrong credentials')
        self.assertRaises(KeyError, lambda: auth_data['token'])

    def __authWithValidUserCredentials(self, username, password):
        auth_data = self.__getResponseDataFromPostRequest(username, password)

        self.assertEqual(auth_data['status'], 200)
        self.assertEqual(auth_data['message'], 'Successfully logged in as ' + self._db_helper.getRoleForUser(username)['role'])
        self.assertTrue(auth_data['token'])

    def __getResponseDataFromPostRequest(self, username, password):
        response_auth = self._app.post('/auth', data=dict({'username': username, 'password': password}))
        return json.loads(response_auth.data)