"""
Annotations route
"""

from flask import Blueprint, request
from utils.response import response
from utils.string import *
from utils.jwt_handler import *
from config import *
from dal.users import get_user
from dal.consumer import create_annotation, update_annotations, get_annotations_for_material

ANNOTATIONS_ROUTER = Blueprint(ANNOTATIONS, __name__)


@ANNOTATIONS_ROUTER.route('/consumers/<username>/materials/<material_id>/annotations')
def get_annotations(username, material_id):
    """Get annotations

    Decorators:
        ANNOTATIONS_ROUTER

    Arguments:
        username {string} -- name of use the annotation belongs to
        material_id {string} -- material id of the file the annotation is set on
    """

    try:
        annotations = get_annotations_for_material(username, material_id)
    except Exception as e:
        return response(str(e), 400)

    return response(
        'Successfully retreived the annotations for the material',
        200,
        {DATA: {ANNOTATIONS: annotations}}
    )

@ANNOTATIONS_ROUTER.route('/consumers/<username>/materials/<material_id>/annotations', methods=['POST'])
def create_annotations(username, material_id):
    """Creates or updates annotation

    If there is already an annotation for the specified material this method will just overwrite it with a new one
    Else it creates a new annotation for that material

    Decorators:
        ANNOTATIONS_ROUTER

    Arguments:
        material_id {string} -- id of material to annotate
    """

    try:
        payload = extract(request)
        consumer = get_user(username)
    except Exception as e:
        return response(str(e), 400)


    new_annotation = {
        MATERIAL_ID: material_id,
        ANNOTATIONS: request.form[ANNOTATIONS]}

    try:
        all_annotations = consumer[DATA][ANNOTATIONS]
    except Exception:
        # NO ANNOTATIONS AT ALL CREATE NEW
        data = create_annotation(username, new_annotation)
        return response(data[MESSAGE], data[STATUS])

    found = False
    for an in all_annotations:
        if an[MATERIAL_ID] == material_id:
            # UPDATE
            found = True
            an[ANNOTATIONS] = request.form[ANNOTATIONS]

    if not found:
        # NEW
        all_annotations.append(new_annotation)


    res = update_annotations(consumer, all_annotations)
    return response(res[MESSAGE], res[STATUS])
