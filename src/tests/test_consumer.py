from basetest import BaseTest
import jwt


# Todo
# test 500 and 400
# add more tests

class ConsumerTestCase(BaseTest):

    #Test @CONSUMERS.route('/consumers', methods=['GET', 'POST'])
    def test_createConsumerWithExistingConsumerCredentials(self):
        path = '/consumers'
        response_data = self._getResponseDataFromPostRequest(path, 'consumer', 'consumer1', 'consumer1')

        self.assertEqual(response_data['status'], 409)
        self.assertEqual(response_data['message'], 'User already exists')

    #Test @CONSUMERS.route('/consumers', methods=['GET', 'POST'])
    def test_createNewConsumer(self):
        path = '/consumers'
        response_data = self._getResponseDataFromPostRequest(path, 'consumer', 'new_consumer', 'new_consumer')

        self.assertEqual(response_data['status'], 201)
        self.assertEqual(response_data['message'], 'User was created')
        self.assertTrue(self._db_helper.deleteOneUserTestData('new_consumer'))

    #Test @CONSUMERS.route('/consumers', methods=['GET', 'POST'])
    def test_getConsumers(self):
        path = '/consumers'
        response = self._app.get(path)
        self.assertEqual(response.status_code, 200)

    #Test @CONSUMERS.route('/consumers/<token>', methods=['GET'])
    def test_getUser(self):
        user_name = 'pelle'
        encoded_data = jwt.encode({'username': user_name}, 'super-secret')
        headers = {'Content-Type': 'application/json', 'Token': encoded_data}
        response = self._app.get('/companies', headers = headers)

        if self._db_helper.userExistInDB(user_name):
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.status_code, 400)
