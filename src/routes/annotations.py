"""
Annotations route
"""

from flask import Blueprint, request
from utils.response import response
from dal.users import get_user
from dal.consumer import create_annotation, update_annotations, get_annotations_for_material
import jwt

ANNOTATIONS = Blueprint('annotations', __name__)


@ANNOTATIONS.route('/consumers/<username>/materials/<material_id>/annotations')
def get_annotations(username, material_id):
    try:
        annotations = get_annotations_for_material(username, material_id)
    except Exception as e:
        return response(str(e), 418)

    return response(
        'Successfully retreived the annotations for the material',
        200,
        {'data': {'annotations': annotations}}
    )

@ANNOTATIONS.route('/consumers/<username>/materials/<material_id>/annotations', methods=['POST'])
def create_annotations(username, material_id):
    """Create a note"""

    try:
        token = request.form['jwt']
    except Exception:
        return response('No JWT', 400)

    try:
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        return response('Tampered token', 400)

    if payload['role'] != 'consumer':
        return response('You are not a consumer', 400)

    try:
        consumer = get_user(payload['username'])
    except Exception:
        #TODO: Custom exception
        return response('User doesn\'t exist', 400)

    new_annotation = {
        'material_id': material_id,
        'annotations':request.form['annotations']}

    try:
        all_annotations = consumer['data']['annotations']
    except Exception as e:
        # NO ANNOTATIONS AT ALL CREATE NEW
        data = create_annotation(consumer, new_annotation)
        return response(data['res'], data['code'])

    found = False
    for an in all_annotations:
        if an['material_id'] == material_id:
            # UPDATE
            found = True
            an['annotations'] = request.form['annotations']

    if not found:
        # NEW
        all_annotations.append(new_annotation)


    data = update_annotations(consumer, all_annotations)
    return response(data['res'], data['code'])

