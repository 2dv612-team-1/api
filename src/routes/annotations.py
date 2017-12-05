"""
Annotations
"""

from Flask import Blueprint, request
from utils.response import response
from dal.users import find_user_by_name

ANNOTAIONS = Blueprint('annotations', __name__)

@ANNOTATIONS.route('/consumers/<token>/products/<product_id>/materials/<material_name>')

def get_annotations(token, material_name):
    """Gets annotations made by one user"""

    try:
        token = request.form['jwt']
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        return response('Expected jwt key', 400)

    if payload['role'] != 'consumer':
        return response('Have to be consumer to annotate', 400)

    annotation = DB.users.find_one({
        '_id': ObjectId(username_id),
        'annotations.material_id': material_name})

    return response(str(annotation), 200)


@ANNOTATIONS.route('/consumers/<token>/products/<product_id>/materials/<material_name>/<annotations>', methods=['POST'])

def add_annotaions(token, material_name):
    """Add notation to user and material"""

    try:
        token = request.form['jwt']
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        return response('Expected jwt key', 400)

    if payload['role'] != 'consumer':
        return response('Have to be consumer to annotate', 400)

    updated = DB.users.find_one_and_update(
        {'_id': ObjectId(username_id)},
        {'$push': {'annotations': {'material_id': payload['material_id'], 'annotation': annotations}}}
        )

    return response(str(updated), 200)