from flask import Blueprint, jsonify
from utils.string import *

ENTRY_ROUTER = Blueprint(ENTRY, __name__)


@ENTRY_ROUTER.route(ROOT)
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
        THREADS: url(THREADS),
        SELF: ROOT
    }
    return jsonify(routes)


def set_root(root):
    def set_url(url):
        return root + url
    return set_url
