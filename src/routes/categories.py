"""
Categories Route
"""

from flask import Blueprint, request
from dal.categories import dal_get_categories, dal_create_category, dal_create_subcategory
from utils.response import response
from utils.string import *
from utils.jwt_handler import *
from utils.form_handler import extract_attribute
from exceptions.WrongCredentials import WrongCredentials
from exceptions.AlreadyExists import AlreadyExists
from exceptions.NoJWT import NoJWT
from exceptions.TamperedToken import TamperedToken
from exceptions.NotAuthorized import NotAuthorized
from exceptions.BadFormData import BadFormData

CATEGORIES_ROUTER = Blueprint(CATEGORIES, __name__)


@CATEGORIES_ROUTER.route('/categories')
def get_categories():
    """Gets all available categories"""
    categories_data = dal_get_categories()
    return response(categories_data, 200)


@CATEGORIES_ROUTER.route('/categories', methods=['POST'])
def create_categories():
    """Creates a new category"""

    try:
        payload = extract(request)
        authorized_role(payload, ADMIN)
        dal_create_category(extract_attribute(request, CATEGORY))
        return response('Category created', 201)
    except AttributeError:
        return response('Broken JWT', 400)
    except WrongCredentials:
        return response('Invalid credentials', 400)
    except AlreadyExists:
        return response('Category exists', 409)
    except NoJWT:
        return response(str(e), 400)
    except TamperedToken:
        return response(str(e), 400)
    except NotAuthorized as e:
        return response(str(e), 403)
    except BadFormData as e:
        return response(str(e), 400)


@CATEGORIES_ROUTER.route('/categories/<category>/subcategories', methods=['POST'])
def create_sub(category):
    """Create a subcategory"""

    try:
        payload = extract(request)
        authorized_role(payload, ADMIN)
        dal_create_subcategory(category, extract_attribute(request, CATEGORY))
        return response('Subcategory created', 201)
    except Exception as e:
        return response(str(e), 400)
