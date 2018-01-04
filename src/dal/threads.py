from .mongo_client import db_conn
from utils.string import *
from utils.jwt_handler import *
from config import *
from bson.objectid import ObjectId
from exceptions.BadFormData import BadFormData
from exceptions.NotFound import NotFound
from exceptions.WrongCredentials import WrongCredentials
import datetime

"""
    db_conn.threads => client.api.threads
"""


def dal_create_thread(form, payload):
    """Create Thread"""

    thread = dict()
    add = set(thread, form)

    try:
        thread.update({NAME: payload[USERNAME]})
    except Exception:
        raise BadFormData('No username')

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
    thread.update({TIMESTAMP: str(datetime.datetime.now()).split('.')[0]})

    try:
        _id = db_conn.threads.insert(thread)
    except Exception:
        raise BadFormData('Could not create thread with supplied data')

    return str(_id)


def dal_get_user_threads(username):
    """Gets user threads"""

    threads = db_conn.threads.find({NAME: username})

    return list(map(lambda thread: dict(
        map(lambda key: [key, str(thread[key]) if key == ID else thread[key]], thread.keys())), threads))


def dal_get_threads():
    threads = db_conn.threads.find()

    return list(map(lambda thread: dict(
        map(lambda key: [key, str(thread[key]) if key == ID else thread[key]], thread.keys())), threads))


def dal_get_thread(_id):
    try:
        thread = db_conn.threads.find_one({ID: ObjectId(_id)})
    except Exception:
        raise NotFound('Could not find thread')

    thread_data = list(
        map(lambda key: [key, str(thread[key]) if key == ID else thread[key]], thread.keys()))

    return dict(thread_data)


def dal_create_reply(form, payload, _id):

    reply = dict()
    add = set(reply, payload)

    try:
        add(USERNAME)
    except Exception:
        raise WrongCredentials('No username in jwt')

    try:
        add(ROLE)
    except Exception:
        raise WrongCredentials('No role in jwt')

    reply.update({TIMESTAMP: str(datetime.datetime.now()).split('.')[0]})

    try:
        reply.update({MESSAGE: form[MESSAGE]})
    except Exception:
        raise BadFormData('Message is missing')

    try:
        db_conn.threads.find_one_and_update(
            {ID: ObjectId(_id)},
            {'$push': {REPLIES: reply}}
        )
    except Exception:
        raise BadFormData('That thread does not exist')


def dal_get_favourites(username):
    """Gets threads with users reply"""

    # Fetches threads which includes replies from user
    threads = db_conn.threads.find({'replies.username': username})

    # Converts appropriate thread data to strings
    return list(map(lambda thread: dict(
        map(lambda key: [key, str(thread[key]) if key == ID else thread[key]], thread.keys())), threads))


def set(dict, form):
    """A nice version for updating dict"""
    def add(name):
        dict.update({name: form[name]})
    return add
