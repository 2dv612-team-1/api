"""
Materials route
"""

from flask import Blueprint, send_from_directory
from utils.response import response
from pymongo import MongoClient

UPLOAD_FOLDER = './uploads'
MATERIALS = Blueprint('materials', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api


@MATERIALS.route('/materials/<company>/<path:filename>')
def get_file(company, filename):
    try:
        return send_from_directory(UPLOAD_FOLDER + '/' + company, filename)
    except Exception:
         return response('No such file', 400)
