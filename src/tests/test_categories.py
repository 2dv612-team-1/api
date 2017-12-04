from basetest import BaseTest
import jwt

#ToDO


class CategoriesTestCase(BaseTest):

    # Test @CATEGORIES.route('/categories')
    def test_GetCategories(self):
        path = '/categories'
        response = self._app.get(path)
        self.assertEqual(response.status_code, 200)

    # Test @CATEGORIES.route('/categories', methods=['POST'])
    def test_createNewCategorie(self):
        path = '/categories'
        new_category = 'new_category'

        encoded_data = jwt.encode({'role': 'admin'}, 'super-secret')
        response = self._app.post(path, data = dict({'jwt': encoded_data, 'category': new_category}))

        self.assertEqual(response.status_code, 201)
        self.assertTrue(self._db_helper.deleteCategory(new_category))

    # Test @CATEGORIES.route('/categories', methods=['POST'])
    def test_createAlreadyExistingCategory(self):
        path = '/categories'
        new_category = 'Freezer'

        encoded_data = jwt.encode({'role': 'admin'}, 'super-secret')
        response = self._app.post(path, data = dict({'jwt': encoded_data, 'category': new_category}))

        self.assertEqual(response.status_code, 409)

    # Test @CATEGORIES.route('/categories', methods=['POST'])
    def test_createNewCategoryBrokenJwt(self):
        path = '/categories'
        new_category = 'new_category'

        encoded_data = jwt.encode({'role': 'admin'}, 'super-secret')
        response = self._app.post(path, data = dict({'broken-jwt': encoded_data, 'category': new_category}))

        self.assertEqual(response.status_code, 400)
        self.assertTrue(self._db_helper.deleteCategory(new_category))

    # Test @CATEGORIES.route('/categories', methods=['POST'])
    def test_createNewCategoryWrongSecret(self):
        path = '/categories'
        new_category = 'new_category'

        encoded_data = jwt.encode({'role': 'admin'}, 'wrong-secret')
        response = self._app.post(path, data = dict({'broken-jwt': encoded_data, 'category': new_category}))

        self.assertEqual(response.status_code, 400)
        self.assertTrue(self._db_helper.deleteCategory(new_category))
