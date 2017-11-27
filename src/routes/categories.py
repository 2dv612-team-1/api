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
        categories_data.append(category)

    return response(categories_data, 200)
