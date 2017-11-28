# Creates test data used in unittests


class DBHelper():
    def __init__(self, db_conn):
        self.__db_users = db_conn.users
        self.__db_admin = db_conn.admin
        self.__user_test_data = []
        self.__createUsersTestData()
        self.addUserTestDataToDB()

    def __createAdminTestData(self):
        pass

    def __createUsersTestData(self):

        """" Consumer Data """
        consumer_data = {'PersonalInfo': {'name': 'Eggbert', 'age': 34},
                         'Manuals': ('manual_1', 'manual_2', 'manual_2')}
        self.__user_test_data.append({'username': 'consumer1', 'password': 'consumer1', 'role': 'consumer', 'data': consumer_data})

        """ Admin Data 
        admin_data = {'Dell': {'username': 'userDell', 'password': 'passDell'},
                      'Apple': {'username': 'userApple', 'password': 'passApple'},
                      'Samsung': {'username': 'userSams', 'password': 'passSams'}}

        self.__test_data.append({'username': 'admin', 'password': '1234', 'role': 'admin', 'data': admin_data})
        """

        """ Company Data """
        company_data = {'Representatives': [{'username': 'rep1', 'password': 'rep1'},
                                            {'username': 'rep2', 'password': 'rep2'},
                                            {'username': 'rep3', 'password': 'rep3'}]}
        self.__user_test_data.append({'username': 'userDell', 'password': 'passDell', 'role': 'company', 'data': company_data})

        """ Representative Data """
        self.__user_test_data.append({'username': 'rep1', 'password': 'rep1', 'role': 'representative', 'data': {'company': 'Dell'}})
        self.__user_test_data.append({'username': 'rep2', 'password': 'rep2', 'role': 'representative', 'data': {'company': 'Apple'}})
        self.__user_test_data.append({'username': 'rep3', 'password': 'rep3', 'role': 'representative', 'data': {'company': 'Samsung'}})

    def addUserTestDataToDB(self):
        for user in self.__user_test_data:
            self.__db_users.insert(user)

    def getRoles(self):
        return ['consumer', 'company', 'representative', 'admin']

    def getUsers(self):
        return self.__db_users.find()

    def getRoleForUser(self, user_name):
        return self.__db_users.find_one({'username': user_name}, {'role': 1})

    def getFirstUserNameAndPasswordFromRole(self, user_role):
        return self.__db_users.find_one({'role': user_role}, {'username': 1, 'password': 1})

    def deleteAllTestDataInDB(self):
        self.__db_users.drop()

    def deleteOneUserTestData(self, username):
        return self.__db_users.remove({'username': username})

    def userExistInDB(self, user_name):
        if self.__db_users.find({'username': user_name}):
            return True
        else:
            return False

""" Consumer
            user = {
                'username': username,
                'password': password,
                'role': 'consumer'
            }
"""

""" Representative
            representative = {
                'username': username,
                'password': password,
                'owner': owner,
                'role': 'representative'
            }

"""

""" Company
            company = {
                'username': username,
                'password': password,
                'role': 'company'
            }

"""

""" Products collection
[

    {

        "name": "Kyl", //Product name

        "serialNo": "131hh-3", //Awesome serial number of product

        "producer": "Bosch", //Set by representative company association

        "category": {

			"name": "refrigerator",

			"id": "categoryID"

		}, //Set from Categories collection

        "desc": "A super smart fridge that not only keeps you food cold, but can also order more food from the interwebs when you are running low. It is so fantastic that it can even turn water into wine. Basically it's Jesus!", //Description added by rep,

        "createdBy": "Eggbert" //The representative that added the product

    }

]

"""

""" Categories collection
[

    {

        "name": "dishwasher", //Added by admin

		"id": "categoryId" //Auto increment from highest id in collection

    },

    {

        "name": "refrigerator",

        "id": "categoryId"

	}

]

"""