"""
Categories Route
"""

from flask import Blueprint, request
from pymongo import MongoClient
from utils.response import response
from exceptions.WrongCredentials import WrongCredentials
from exceptions.AlreadyExists import AlreadyExists
import jwt

CLIENT = MongoClient('mongodb:27017')
CATEGORIES = Blueprint('CATEGORIES', __name__)
DB = CLIENT.api


@CATEGORIES.route('/categories')
def get_categories():
    """Gets all available categories"""

    categories_data = []
    for category in DB.categories.find():
        categories_data.append({
            'category': category.get('category'),
            '_id': str(category.get('_id'))
        })

    return response(categories_data, 200)


@CATEGORIES.route('/categories', methods=['POST'])
def create_categories():
    """Creates a new category"""

    try:
        try:
            token = request.form['jwt']
            category = request.form['category']
        except Exception:
            raise WrongCredentials()

        try:
            payload = jwt.decode(token, 'super-secret')
        except Exception:
            raise AttributeError()

        if payload['role'] == 'admin':
            category_exists = DB.categories.find_one({'category': category})
            if category_exists:
                raise AlreadyExists()

            DB.categories.insert({
                'category': category
            })

            return response('Category created', 201)

    except AttributeError:
        return response('Broken JWT', 400)
    except WrongCredentials:
        return response('Invalid credentials', 400)
    except AlreadyExists:
        return response('Category exists', 409)
