from unittest import TestCase
from main import APP
from pymongo import MongoClient
from db_helper import DBHelper
import random, string

class BaseTest(TestCase):

    def setUp(self):
        self.roles = ['consumer', 'company', 'representative', 'admin'];
        client = MongoClient('mongodb:27017')
        self._db_helper = DBHelper(client.api.users)
        self._app = APP.test_client()
        self._app.testing = True

    def tearDown(self):
        self._db_helper.deleteAllTestDataInDB()

    #Add code to return unique pass & name
    def _getRandomUserNameAndPasswordOflenEight(self):
        return self.__generateRandomWord(8), self.__generateRandomWord(8)

    def __generateRandomWord(self, len_for_word):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(len_for_word))