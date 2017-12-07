from .mongo_client import db_conn
from exceptions.WrongCredentials import WrongCredentials
from exceptions.AlreadyExists import AlreadyExists
from exceptions.TamperedToken import TamperedToken
import jwt


def dal_get_categories():
    categories_data = []
    for category in db_conn.categories.find():
        categories_data.append({
            'category': category.get('category'),
            '_id': str(category.get('_id')),
            'sub': category.get('sub')
        })

    return categories_data


def dal_create_category(form):
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

        db_conn.categories.insert({'category': category, 'sub': []})


def dal_create_subcategory(form, category):
    try:
        token = form['jwt']
        subcategory = form['category']
    except Exception:
        raise WrongCredentials()

    try:
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        raise TamperedToken()

    if payload['role'] != 'admin':
        raise AttributeError('Not an admin')

    subcategory_exists = db_conn.categories.find_one({
        'category.sub.category': subcategory
    })

    if subcategory_exists:
        raise AlreadyExists('Subcategory exists')

    is_category = db_conn.categories.find_one({
        'category': subcategory
    })

    if is_category:
        raise AlreadyExists('Category with that name exists')

    try:
        db_conn.categories.find_one_and_update(
            {'category': category},
            {'$push': {'sub': {'category': subcategory}}},
            upsert=True
        )
    except Exception as e:
        return str(e)
