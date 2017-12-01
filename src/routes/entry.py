from flask import Blueprint, jsonify

ENTRY = Blueprint('entry', __name__)


@ENTRY.route('/')
def get_entry():
    """Displays a list of possible routes"""

    routes = {
        'auth': '/auth',
        'products': '/products',
        'consumers': '/consumers',
        'companies': '/companies',
        'categories': '/categories',
        'admins': '/admins',
        'materials': '/materials',
        'self': '/'
    }
    return jsonify(routes)
