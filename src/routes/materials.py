"""
Materials route
"""

from flask import Blueprint, send_from_directory
from pymongo import MongoClient

UPLOAD_FOLDER = './uploads'
MATERIALS = Blueprint('materials', __name__)
CLIENT = MongoClient('mongodb:27017')
DB = CLIENT.api


@MATERIALS.route('/materials/<company>/<path:filename>')
def get_file(company, filename):
    return send_from_directory(UPLOAD_FOLDER + '/' + company, filename)
