from mongo_client import db_conn


def get_categories(self):
    categories_data = []
    for category in db_conn.categories.find():
        categories_data.append({
            'category': category.get('category'),
            '_id': str(category.get('_id'))
        })

    return categories_data


def create_category(self, category):
    if db_conn.categories.find({'category': category}).count() != 0:
        return True
    else:
        self.db_conn.categories.insert({'category': category})
        return False
