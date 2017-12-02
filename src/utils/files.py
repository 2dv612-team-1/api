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
    for file_key in req_files:
        current_app.logger.info(file_key)
        if not file_key == 'files':
            raise AttributeError('Form key for files must be \'files\'')
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
        files {list} -- request.files.getlist('files')

    Returns:
        list -- filenames after time stamp has been appended
    """

    file_with_stamp = []
    file_without_stamp = []


    for file in files:
        filename = secure_filename(file.filename).split('.')
        file_folder = create_folder(path)
        time_stamp = str(time.time()).replace('.', '')
        file_time = filename[0] + '-' + time_stamp + '.' + filename[1]
        file_path = os.path.join(file_folder, file_time)
        file.save(file_path)
        file_with_stamp.append({
            'file_time': file_time,
            'file_name': filename[0]
        })

    return file_with_stamp 

def create_folder(path):
    file_folder = os.path.join(UPLOAD_FOLDER, path)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    return file_folder
