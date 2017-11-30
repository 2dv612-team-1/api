"""
Files utils
"""

import os
import time
from flask import current_app
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './materials'
ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_request_files(request_files):
    """Verifies the request files

    Checks if the request files are present and correctly named as well as makes sure the file extension type is accepted

    Arguments:
        requst_files {request.files} -- The files from flask request object

    Raises:
        AttributeError -- 'Files missing from request'
        AttributeError -- 'Form key for files must be \'file\''
        AttributeError -- 'File type extension <extension> is not allowed'
    """

    req_files = request_files
    if len(req_files) < 1:
        raise AttributeError('Files missing from request')
    for file_key in req_files:
        current_app.logger.info(file_key)
        if not file_key == 'file':
            raise AttributeError('Form key for files must be \'file\'')
    files = req_files.getlist('file')
    for file in files:
        if not allowed_file(file.filename):
            raise AttributeError('File type extension \'' + file.filename.rsplit('.', 1)[1] + '\' is not allowed')

def create_file_path(company, product):
    return os.path.join(company, product)

def save(path, files):
    """Saves the files to the specified path which should be based on company and product name

    Creates folder if not exists and places file in there based on company and product name

    Arguments:
        path {string} -- A path string created by joining company name with product name
    """

    for file in files:
        filename = secure_filename(file.filename)
        file_folder = create_folder(path)
        file_path = os.path.join(file_folder, filename)
        file.save(file_path)

def create_folder(path):
    file_folder = os.path.join(UPLOAD_FOLDER, path)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    return file_folder
