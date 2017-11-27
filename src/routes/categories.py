"""
Categories Route
"""

from flask import Blueprint, request
from pymongo import MongoClient
from utils.response import response
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
            'category_id': category.get('category_id')
        })

    return response(categories_data, 200)


@CATEGORIES.route('/categories', methods=['POST'])
def create_categories():
    """Creates a new category"""

    try:
        token = request.form.get('jwt')
        category = request.form['category']
        payload = jwt.decode(token, 'super-secret')

        if payload['role'] == 'admin':
            category_exists = DB.categories.find_one({ 'category': category })
            if category_exists:
                raise AttributeError()

            existing_categories = DB.categories.find()

            # category_id = existing_categories.len()
            DB.categories.insert({
                'category': category,
                'category_id': 0
            })
            return response('Category created', 201)

    except AttributeError:
        return response('Wrong credentials', 400)
