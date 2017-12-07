"""
Annotations route
"""

from flask import Blueprint, request
from pymongo import MongoClient
from exceptions.TamperedToken import TamperedToken
from utils.response import response
from dal.users import find_user_by_name
from bson.objectid import ObjectId
import jwt

ANNOTAIONS = Blueprint('annotations', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api


@ANNOTATIONS.route('/consumers/<token>/products/<product_id>/materials/<material_name>/<annotations>', methods=['POST'])
def create_annotations():
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
        consumer = DB.users.find_one({'username': payload['username']}) 

        new_annotation = {
            '_id': ObjectId(username_id)}
            'material': filename['file_time']
            'annotations':request.form['annotations']}
        
        _id = DB.annotations.insert(new_annotation)

    return response('A note was created', 200 {'new_annotation'})


@ANNOTATIONS.route('/consumers/<token>/products/<product_id>/materials/<material_name>/<annotations>', methods=['POST'])
def update_annotations(token, material_name):
    """Update note to user and material"""
    
    try:
        token = request.form['jwt']
        payload = jwt.decode(token, 'super-secret')
    except Exception:
        return response('Expected jwt key', 400)

    if payload['role'] != 'consumer':
        return response('Have to be consumer to annotate', 400)

    updated = DB.users.find_one_and_update({
        '_id': ObjectId(username_id)},
        {'$push': {'annotations': {'material_id': payload['material_id'], 'annotation': annotations}}}
        )

    return response(str(updated), 200)


@ANNOTATIONS.route('/consumers/<token>/products/<product_id>/materials/<material_name>')
def get_annotations(token, material_name):
    """Gets one note made by one user"""

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

    if (annotation==''):
        return response('The material has no notes attached.', 400)

    return response(str(annotation), 200)


