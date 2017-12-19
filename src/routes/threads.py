from flask import Blueprint, request
from utils.jwt_handler import *
from utils.response import response
from utils.string import *
from dal import *

from dal.threads import dal_create_thread, dal_get_threads
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
    threads = dal_get_threads()
    return response('HÄÄÄÄR RICKARD', 200)


@THREADS_ROUTER.route('/threads', methods=['POST'])
def create_thread():
    """Create a thread"""
    try:
        payload = extract(request)
        thread = dal_create_thread(request.form, payload)
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
