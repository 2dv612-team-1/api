from .mongo_client import db_conn
from exceptions.WrongCredentials import WrongCredentials
from exceptions.AlreadyExists import AlreadyExists
from exceptions.TamperedToken import TamperedToken
from utils.string import *
import jwt


def dal_get_categories():
    categories_data = []
    for category in db_conn.categories.find():
        categories_data.append({
            CATEGORY: category.get(CATEGORY),
            ID: str(category.get(ID)),
            SUB: category.get(SUB)
        })

    return categories_data


def dal_create_category(form):
    try:
        token = form[JWT]
        category = form[CATEGORY]

    except Exception:
        raise WrongCredentials()
    try:
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        raise AttributeError()

    if payload[ROLE] == ADMIN:
        category_exists = db_conn.categories.find_one({CATEGORY: category})

        if category_exists:
            raise AlreadyExists()

        is_subcategory = db_conn.categories.find_one({
            'sub.category': category
        })

        if is_subcategory:
            raise AlreadyExists('Category is a subcategory')

        db_conn.categories.insert({CATEGORY: category, SUB: []})


def dal_create_subcategory(form, category):
    try:
        token = form[JWT]
        subcategory = form[CATEGORY]
    except Exception:
        raise WrongCredentials('JWT or Category is missing')

    try:
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        raise TamperedToken('Changes has been made to JWT')

    if payload[ROLE] != ADMIN:
        raise AttributeError('Not an admin')

    subcategory_exists = db_conn.categories.find_one({
        '%s.%s' % (SUB, CATEGORY): subcategory
    })

    if subcategory_exists:
        raise AlreadyExists('Subcategory exists')

    is_category = db_conn.categories.find_one({
        CATEGORY: subcategory
    })

    if is_category:
        raise AlreadyExists('Category with that name exists')

    try:
        db_conn.categories.find_one_and_update(
            {CATEGORY: category},
            {'$push': {SUB: {CATEGORY: subcategory}}},
            upsert=True
        )
    except Exception as e:
        return str(e)
