from flask import Blueprint, request
from utils.jwt_handler import *
from utils.response import response
from utils.string import *
from dal import *

from dal.threads import dal_create_thread, dal_get_threads, dal_get_thread, dal_create_reply
from dal.companies import dal_add_unread, dal_get_unread_threads

from exceptions.WrongCredentials import WrongCredentials
from exceptions.NotFound import NotFound
from exceptions.AlreadyExists import AlreadyExists
from exceptions.InvalidRole import InvalidRole
from exceptions.BadFormData import BadFormData
from exceptions.ErrorRequestingFiles import ErrorRequestingFiles
from exceptions.ErrorCreatingFiles import ErrorCreatingFiles

THREADS_ROUTER = Blueprint(THREADS, __name__)


@THREADS_ROUTER.route('/threads')
def get_threads():

    threads_data = dal_get_threads()

    return response(
        'Successfully retrieved all the threads',
        200,
        {DATA: {THREADS: threads_data}}
    )


@THREADS_ROUTER.route('/threads', methods=['POST'])
def create_thread():
    """Create a thread"""
    try:
        payload = extract(request)
        thread = dal_create_thread(request.form, payload)
        dal_add_unread(request.form, thread)
        return response('Thread was created', 201, {DATA: {THREADS: thread}})

    except AttributeError:
        return response('Tampered token', 400)
    except NoJWT as e:
        return response(str(e), 403)
    except WrongCredentials:
        return response('Invalid credentials', 400)
    except InvalidRole:
        return response('You are not a representative', 400)
    except BadFormData as e:
        return response(str(e), 400)


@THREADS_ROUTER.route('/threads/<_id>')
def get_thread(_id):
    """Gets a single thread"""

    try:
        thread = dal_get_thread(_id)
        return response("Got the tråd", 200, {DATA: thread})
    except NotFound as e:
        return response(str(e), 404)
    except Exception:
        return response('Everything broke', 500)


@THREADS_ROUTER.route('/threads/<_id>/replies', methods=['POST'])
def create_reply(_id):
    """Posts reply to thread"""

    try:
        payload = extract(request)
        dal_create_reply(request.form, payload, _id)
        return response('Reply created', 201)
    except BadFormData as e:
        return response(str(e), 404)
    except Exception:
        return response('Everything broke', 500)


@THREADS_ROUTER.route('/threads/unread', methods=['POST'])
def get_unread_threads():
    try:
        payload = extract(request)
        authorized_role(payload, REPRESENTATIVE)
        comp_username = payload['owner']

        threads_data = dal_get_unread_threads(comp_username)

        return response(
            'Successfully retrieved all the unread-threads',
            200,
            {DATA: {THREADS: threads_data}}
        )

    except BadFormData:
        return response(str(e), 400)
    except InvalidRole:
        return response('You are not a representative', 400)
    except Exception:
        return response('Everything broke', 500)
