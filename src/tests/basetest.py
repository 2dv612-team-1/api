from unittest import TestCase
from main import APP
from pymongo import MongoClient
from db_helper import DBHelper
import random, string, jwt, json


class BaseTest(TestCase):

    def setUp(self):
        client = MongoClient('mongodb:27017')
        self._db_helper = DBHelper(client.api.users)
        self._app = APP.test_client()
        self._app.testing = True

    def tearDown(self):
        self._db_helper.deleteAllTestDataInDB()

    # Todo add code to return unique pass & name
    def _getRandomUserNameAndPasswordOflenEight(self):
        return self.__generateRandomWord(8), self.__generateRandomWord(8)

    def __generateRandomWord(self, len_for_word):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(len_for_word))

    # private helper/util
    def _getResponseDataFromPostRequest(self, path='',  role='', username='', password='', encoded_data = None):
        if encoded_data is None:
            encoded_data = jwt.encode({'role': role}, 'super-secret')

        response_auth = self._app.post(path, data = dict({'username': username,
                                                       'password': password,
                                                       'jwt': encoded_data}))
        return json.loads(response_auth.data)