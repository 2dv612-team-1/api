from .mongo_client import db_conn
from utils.string import *
from utils.jwt_handler import *
from config import *

from exceptions.BadFormData import BadFormData

"""
    db_conn.threads => client.api.threads
"""


def dal_create_thread(form, payload):
    """Create Thread"""

    thread = dict()
    add = set(thread, form)

    try:
        add(TITLE)
    except Exception:
        raise BadFormData('Title is missing from request')

    try:
        add(CATEGORY)
    except Exception:
        raise BadFormData('Category is missing')

    try:
        add(SUBCATEGORY)
    except Exception:
        subcategory = ''

    try:
        add(PRODUCT)
    except Exception:
        raise BadFormData('Product is missing')

    try:
        add(MESSAGE)
    except Exception:
        raise BadFormData('Message is missing')

    thread.update({REPLIES: list()})

    try:
        _id = db_conn.threads.insert(thread)
    except Exception:
        raise BadFormData('Could not create thread with supplied data')

    return str(_id)


def dal_get_user_threads(username):
    """Gets user threads"""

    threads = db_conn.threads.find({NAME: username})
    return threads


def set(dict, form):
    """A nice version for updating dict"""
    def add(name):
        dict.update({name: form[name]})
    return add
