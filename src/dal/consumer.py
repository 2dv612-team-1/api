from .mongo_client import db_conn
from exceptions.AnnotationsNotFound import AnnotationsNotFound
from utils.string import *

"""Create consumer account, if consumer account with given username and password does not already exist"""


def create_consumer(form):
    username = form[USERNAME]
    password = form[PASSWORD]

    if db_conn.users.find({USERNAME: username}).count() != 0:
        return True
    else:

        user = {
            USERNAME: username,
            PASSWORD: password,
            ROLE: CONSUMER
        }

        db_conn.users.insert(user)
        return False

def create_annotation(user, annotations):
    """Creates a new annotation for a specific product

    Arguments:
        user {mongo object} -- user to add the annotation to
        annotations {json object} -- {'material_id': 123abc, 'annotations': 'Some comments about this material'}
    """

    try:
        db_conn.users.find_one_and_update({'_id': user['_id']}, {'$push': {'data.annotations': annotations}})
    except Exception as e:
        return {'res': 'Failed', 'code': 500}

    return {'res': 'GREAT SUCCESS', 'code': 201}

def update_annotations(user, annotations):
    """Update annotations for a specific product

    Arguments:
        user {mongo object} -- user to update the annotation on
        annotations {array of json object} -- updated annotations collection (array)
    """

    try:
        db_conn.users.find_one_and_update({'_id': user['_id']}, {'$set': {'data.annotations': annotations}})
    except Exception as e:
        return {'res': 'Failed', 'code': 500}

    return {'res': 'GREAT SUCCESS', 'code': 200}

def get_annotations_for_material(username, material_id):

    try:
        found_annotations = db_conn.users.aggregate([
            {'$match': {'username': username}},
            {'$unwind': '$data.annotations'},
            {
                '$project': {
                    'material_id': '$data.annotations.material_id',
                    'annotations': '$data.annotations.annotations'
                }
            },
            {'$match': {'material_id': material_id}}
        ])
    except Exception as e:
        raise AnnotationsNotFound('Annotations for material not found')

    if len(list(found_annotations)) < 1:
        raise AnnotationsNotFound('Annotations for material not found')

    annotations = {}
    for x in found_annotations:
        annotations['material_id'] = x['material_id']
        annotations['annotations'] = x['annotations']

    return annotations