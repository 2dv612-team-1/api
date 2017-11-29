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
        'admins': '/admins',
        'self': '/'
    }
    return jsonify(routes)
