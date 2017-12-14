from .mongo_client import db_conn
from exceptions.WrongCredentials import WrongCredentials
from exceptions.AlreadyExists import AlreadyExists
from exceptions.TamperedToken import TamperedToken
from utils.string import *
from utils.jwt_handler import *
from config import *
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


def dal_create_category(category):

    category_exists = db_conn.categories.find_one({CATEGORY: category})

    if category_exists:
        raise AlreadyExists()

    is_subcategory = db_conn.categories.find_one({
        '%s.%s' % (SUB, CATEGORY): category
    })

    if is_subcategory:
        raise AlreadyExists('Category is a subcategory')

    db_conn.categories.insert({CATEGORY: category, SUB: []})


def dal_create_subcategory(category, subcategory):

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
