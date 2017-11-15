"""
Admin routes
"""

from flask import Blueprint, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb:27017')
admin = Blueprint('admin', __name__)
db = client.api

@admin.route('/admins', methods=['POST'])
def adminActions():
    """When requested create admin account"""
    if request.method == 'POST':
        default_admin = {
            'username': 'admin',
            'password': 'admin123'
        }

        db.admin.update({}, default_admin, upsert=True)

        return jsonify({
            'status': 201,
            'message': 'Admin account has been created'
        })
