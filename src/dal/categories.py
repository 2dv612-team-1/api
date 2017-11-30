from .mongo_client import db_conn
from exceptions.WrongCredentials import WrongCredentials
from exceptions.AlreadyExists import AlreadyExists
import jwt


def get_categories():
    categories_data = []
    for category in db_conn.categories.find():
        categories_data.append({
            'category': category.get('category'),
            '_id': str(category.get('_id'))
        })

    return categories_data


def create_category(form):
    try:
        token = form['jwt']
        category = form['category']

    except Exception:
        raise WrongCredentials()
    try:
        payload = jwt.decode(token, 'super-secret')

    except Exception:
        raise AttributeError()

    if payload['role'] == 'admin':
        category_exists = db_conn.categories.find_one({'category': category})

        if category_exists:
            raise AlreadyExists()

        db_conn.categories.insert({'category': category})
