
import json
from basetest import BaseTest


class AuthTestCase(BaseTest):

    def test_authEveryUserInDB(self):
        for user in self._db_helper.getUsers():
            self.__authUser(user)

    def __authUser(self, user):
        username = user['username']
        password = user['password']

        response_auth = self._app.post('/auth', data=dict({'username': username, 'password': password}))
        auth_data = json.loads(response_auth.data)

        self.assertEqual(response_auth.status_code, 200)
        self.assertEqual(auth_data['message'], 'Successfully logged in as ' + self._db_helper.getRoleForUser(username)['role'])
        self.assertTrue(auth_data['token'])
