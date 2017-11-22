
import json
from basetest import BaseTest


class AuthTestCase(BaseTest):

    def test_authAsAdmin(self):
        username = 'admin'
        password = '1234'

        response_auth = self._app.post('/auth', data=dict({'username': username, 'password': password}))
        auth_data = json.loads(response_auth.data)

        self.assertEqual(response_auth.status_code, 200)
        self.assertEqual(auth_data['message'], 'Successfully logged in as ' + self._db_helper.getRoleForUser(username)['role'])
        self.assertTrue(auth_data['token'])