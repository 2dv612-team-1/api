# Dbconnector


class DBHelper():
    def __init__(self, db_conn):
        self.__db_users = db_conn
        self.__test_data = []
        self.__createTestData()
        self.addTestDataToDB()

    def __createTestData(self):
        """" Consumer Data """
        consumer_data = {'PersonalInfo': {'name': 'Eggbert', 'age': 34},
                         'Manuals': ('manual_1', 'manual_2', 'manual_2')}
        self.__test_data.append({'username': 'consumer1', 'password': 'consumer1', 'role': 'consumer', 'data': consumer_data})

        """ Admin Data """
        admin_data = {'Dell': {'username': 'userDell', 'password': 'passDell'},
                      'Apple': {'username': 'userApple', 'password': 'passApple'},
                      'Samsung': {'username': 'userSams', 'password': 'passSams'}}
        self.__test_data.append({'username': 'admin', 'password': '1234', 'role': 'admin', 'data': admin_data})

        """ Company Data """
        company_data = {'Representatives': [{'username': 'rep1', 'password': 'rep1'},
                                            {'username': 'rep2', 'password': 'rep2'},
                                            {'username': 'rep3', 'password': 'rep3'}]}
        self.__test_data.append({'username': 'userDell', 'password': 'passDell', 'role': 'company', 'data': company_data})

        """ Representative Data """
        self.__test_data.append({'username': 'rep1', 'password': 'rep1', 'role': 'representative', 'data': {'company': 'Dell'}})
        self.__test_data.append({'username': 'rep2', 'password': 'rep2', 'role': 'representative', 'data': {'company': 'Apple'}})
        self.__test_data.append({'username': 'rep3', 'password': 'rep3', 'role': 'representative', 'data': {'company': 'Samsung'}})

    def addTestDataToDB(self):
        for user in self.__test_data:
            self.__db_users.insert(user)

    def getUsers(self):
        return self.__db_users.find()

    def deleteTestDataInDB(self):
        for user in self.__test_data:
            self.__db_users.remove(user)

    def companyExistInDB(self, in_username):
        if self.__db_users.find({'username': in_username}):
            return True
        else:
            return False
