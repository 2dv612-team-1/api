# Creates test data used in unittests


class DBHelper():
    def __init__(self, db_conn):
        self.__db_users = db_conn.users
        self.__db_admin = db_conn.admin
        self.__user_test_data = []

        self.__createUsersTestData()
        self.__createAdminTestData()

    def __createAdminTestData(self):

        default_admin = {
            'username': 'admin',
            'password': 'admin123',
            'role': 'admin'
        }

        self.__db_admin.update({}, default_admin, upsert=True)

    def __createUsersTestData(self):

        user1 = {
            'username': 'user1',
            'password': 'user1',
            'role': 'consumer'
        }

        user2 = {
            'username': 'user2',
            'password': 'user2',
            'role': 'consumer'
        }

        user3 = {
            'username': 'user3',
            'password': 'user3',
            'owner': 'userdell',
            'role': 'representative'
        }

        user4 = {
            'username': 'user4',
            'password': 'user4',
            'owner': 'user_apple',
            'role': 'representative'
        }

        user5 = {
            'username': 'userapple',
            'password': 'userapple',
            'role': 'company'
        }

        user6 = {
            'username': 'userdell',
            'password': 'userdell',
            'role': 'company'
        }

        self.__user_test_data.append(user1)
        self.__user_test_data.append(user2)
        self.__user_test_data.append(user3)
        self.__user_test_data.append(user4)
        self.__user_test_data.append(user5)
        self.__user_test_data.append(user6)

        self.addTestDataToDB()

    def addTestDataToDB(self):
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
        self.__db_admin.drop()

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