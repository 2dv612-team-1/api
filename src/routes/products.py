"""
Products route
"""

from flask import Blueprint, request
from utils.response import response
from utils.string import *
from utils.form_handler import *
from utils.jwt_handler import *
from config import *

from dal.products import dal_get_products, dal_create_product_upload_files, dal_get_product_by_id, dal_upload_files, dal_rate_material
from exceptions.WrongCredentials import WrongCredentials
from exceptions.NotFound import NotFound
from exceptions.AlreadyExists import AlreadyExists
from exceptions.InvalidRole import InvalidRole
from exceptions.BadFormData import BadFormData
from exceptions.ErrorRequestingFiles import ErrorRequestingFiles
from exceptions.ErrorCreatingFiles import ErrorCreatingFiles
from exceptions.NotFound import NotFound
from exceptions.NotAuthorized import NotAuthorized


PRODUCTS_ROUTER = Blueprint(PRODUCTS, __name__)


@PRODUCTS_ROUTER.route('/products')
def get_products():
    """Gets all available products"""

    products_data = dal_get_products()

    return response(
        'Successfully retreived all the products',
        200,
        {DATA: {PRODUCTS: products_data}}
    )


@PRODUCTS_ROUTER.route('/products', methods=['POST'])
def create_product():
    """Create a product"""
    try:
        payload = extract(request)
        authorized_role(payload, REPRESENTATIVE)
        product = dal_create_product_upload_files(request, payload[USERNAME])
        return response('Product was created', 201, {DATA: {PRODUCT: product}})

    except AttributeError:
        return response('Tampered token', 400)
    except WrongCredentials:
        return response('Invalid credentials', 400)
    except AlreadyExists as e:
        return response(str(e), 409)
    except InvalidRole:
        return response('You are not a representative', 400)
    except BadFormData as e:
        return response(str(e), 400)
    except ErrorRequestingFiles:
        return response('Error requesting files', 409)
    except NotAuthorized:
        return response('Beppe is a Teapot', 418)
    except ErrorCreatingFiles as e:
        return response(str(e), 409)


@PRODUCTS_ROUTER.route('/products/<_id>')
def get_product(_id):
    """Gets a single product"""
    try:

        product = dal_get_product_by_id(_id)
        return response('Found product', 200, {DATA: {PRODUCT: product}})

    except WrongCredentials:
        return response('Not a valid id', 400)
    except NotFound:
        return response('Cannot find product', 400)


@PRODUCTS_ROUTER.route('/products/<_id>/materials', methods=['POST'])
def upload_actions(_id):
    try:
        payload = extract(request)
        authorized_role(payload, REPRESENTATIVE)
        username = payload[USERNAME]
        dal_upload_files(request.files, username, _id)
        return response(
            'Successfully uploaded material to the product',
            201,
            {DATA: {PRODUCT: {ID: _id}}})

    except AttributeError:
        return response('Tampered token', 400)
    except WrongCredentials:
        return response('Invalid credentials', 400)
    except AlreadyExists as e:
        return response(str(e), 409)
    except InvalidRole:
        return response('You are not a representative', 400)
    except BadFormData as e:
        return response(str(e), 400)
    except ErrorRequestingFiles:
        return response('Error requesting files', 409)
    except NotAuthorized:
        return response('Beppe is a Teapot', 418)
    except ErrorCreatingFiles as e:
        return response(str(e), 409)


@PRODUCTS_ROUTER.route('/products/<product_id>/materials/<material_name>/rate', methods=['POST'])
def rate_material(product_id, material_name):
    """Used to rate material"""

    try:
        payload = extract(request)
        authorized_role(payload, CONSUMER)
        username = payload[USERNAME]
        rating = extract_attribute(request, RATE)

        updated_rating = dal_rate_material(
            rating, username, product_id, material_name)

        return response(updated_rating, 200)

    except WrongCredentials:
        return response('Expected jwt key', 400)
    except NotFound:
        return response('Not found', 400)
    except InvalidRole:
        return response('Have to be consumer to rate', 400)
    except BadFormData:
        return response('Expected rate key', 400)
    except FloatingPointError:
        return response('Expected rate to be int', 400)
    except ValueError:
        return response('Expected star value to be between 1 and 5', 400)
    except NotAuthorized:
        return response('Beppe is a Teapot', 418)
    except Exception:
        return response('Everything broke', 500)
