from flask import Blueprint, jsonify
from utils.string import *

ENTRY = Blueprint('entry', __name__)


@ENTRY.route(ROOT)
def get_entry():
    """Displays a list of possible routes"""

    url = set_root(ROOT)

    routes = {
        AUTH: url(AUTH),
        PRODUCTS: url(PRODUCTS),
        CONSUMERS: url(CONSUMERS),
        COMPANIES: url(COMPANIES),
        ADMINS: url(ADMINS),
        MATERIALS: url(MATERIALS),
        CATEGORIES: url(CATEGORIES),
        SELF: ROOT
    }
    return jsonify(routes)


def set_root(root):
    def set_url(url):
        return root + url
    return set_url
