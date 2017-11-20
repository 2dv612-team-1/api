from flask import Blueprint, jsonify

ENTRY = Blueprint('entry', __name__)


@ENTRY.route('/')
def get_entry():
    """Displays a list of possible routes"""

    routes = {
        'companies': '/companies',
        'representatives': '/representatives(?token=jwt)',
        'admins': '/admins',
        'self': '/'
    }
    return jsonify(routes)
