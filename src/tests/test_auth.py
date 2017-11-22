import random, string
import json
from basetest import BaseTest


class AuthTestCase(BaseTest):

    def test_authEveryUserInDB(self):
        for user in self._db_helper.getUsers():
            self.__authWithValidUserCredentials(user['username'], user['password'])

    def test_authInvalidUsernameAndPassword(self):
        random_username, random_password = self.__getRandomUserNameAndPasswordOflenEight()
        auth_data = self.__getResponseDataFromPostRequest(random_username, random_password)

        self.assertEquals(auth_data['status'], 400)
        self.assertEqual(auth_data['message'],'Wrong credentials')
        self.assertRaises(KeyError, lambda: auth_data['token'])

    def __authWithValidUserCredentials(self, username, password):
        auth_data = self.__getResponseDataFromPostRequest(username, password)
        self.assertEqual(auth_data['status'], 200)
        self.assertEqual(auth_data['message'],
                             'Successfully logged in as ' + self._db_helper.getRoleForUser(username)['role'])
        self.assertTrue(auth_data['token'])

    def __getResponseDataFromPostRequest(self, username, password):
        response_auth = self._app.post('/auth', data=dict({'username': username, 'password': password}))
        return json.loads(response_auth.data)

    def __getRandomUserNameAndPasswordOflenEight(self):
        return self.__generateRandomWord(8), self.__generateRandomWord(8)

    def __generateRandomWord(self, len_for_word):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(len_for_word))