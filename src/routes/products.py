"""
Products route
"""

from flask import Blueprint, request
from utils.response import response
from dal.products import dal_get_products, dal_create_product_upload_files, dal_get_product_by_id, dal_upload_files, dal_rate_product
from exceptions.WrongCredentials import WrongCredentials
from exceptions.AlreadyExists import AlreadyExists
from exceptions.InvalidRole import InvalidRole
from exceptions.BadFormData import BadFormData
from exceptions.ErrorRequestingFiles import ErrorRequestingFiles
from exceptions.ErrorCreatingFiles import ErrorCreatingFiles
from exceptions.NotFound import NotFound


PRODUCTS = Blueprint('products', __name__)


# add bcrypt


@PRODUCTS.route('/products')
def get_products():
    """Gets all available products"""

    products_data = dal_get_products()

    return response(
        'Successfully retreived all the products',
        200,
        {'data': {'products': products_data}}
    )


@PRODUCTS.route('/products', methods=['POST'])
def create_product():
    """Create a product"""
    try:

        _id = dal_create_product_upload_files(request.form, request.files)
        return response('Product was created', 201, {'data': {'product': str(_id)}})

    except AttributeError:
        return response('Broken JWT', 400)
    except WrongCredentials:
        return response('Invalid credentials', 400)
    except AlreadyExists:
        return response('Category exists', 409)
    except InvalidRole:
        return response('You are not a representative', 400)
    except BadFormData:
        return response('Wrong information', 400)
    except ErrorRequestingFiles:
        return response('Error requesting files', 409)


@PRODUCTS.route('/products/<_id>')
def get_product(_id):
    """Gets a single product"""
    try:

        product = dal_get_product_by_id(_id)
        return response('Found product', 200, {'data': {'product': product}})

    except WrongCredentials:
        return response('Not a valid id', 400)
    except NotFound:
        return response('Cannot find product', 400)

@PRODUCTS.route('/products/<_id>/materials', methods=['POST'])
def upload_actions(_id):
    try:

        dal_upload_files(request.form, request.files, _id)
        return response(
            'Successfully uploaded material to the product',
            201,
            {'data': {'product': 'File uploaded'}}
        )

    except AttributeError:
        return response('Broken JWT', 400)
    except WrongCredentials:
        return response('Invalid credentials', 400)
    except NotFound:
        return response('Files missing from request', 400)
    except ErrorRequestingFiles:
        return response('Error requesting files', 409)
    except ErrorCreatingFiles:
        return response('Error creating files', 409)



@PRODUCTS.route('/products/<product_id>/materials/<material_name>/rate', methods=['POST'])
def rate_material(product_id, material_name):
    """Used to rate material"""
    try:

        total_vote_value, vote_amount = dal_rate_product(request.form, product_id, material_name)
        return response(str({
            'average': total_vote_value,
            'amount': vote_amount
        }), 200)

    except WrongCredentials:
        return response('Expected jwt key', 400)
    except InvalidRole:
        return response('Have to be consumer to rate', 400)
    except BadFormData:
        return response('Expected rate key', 400)
    except FloatingPointError:
        return response('Expected rate to be int', 400)
    except ValueError:
        return response('Expected star value to be between 1 and 5', 400)