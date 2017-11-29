"""
Files util
"""

import os
from flask import current_app
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './materials'
ALLOWED_EXTENSIONS = set(['pdf'])

class files:
    """File handler

    Handles uploaded files on the server
    """

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def check_request_files(self, request_files):
        """Verifies the request files

        Checks if the request files are present and correctly named as well as makes sure the file extension type is accepted

        Arguments:
            requst_files {request.files} -- The files from flask request object

        Raises:
            AttributeError -- 'Files missing from request'
            AttributeError -- 'Form key for files must be \'file\''
            AttributeError -- 'File type extension <extension> is not allowed'
        """

        self.request_files = request_files
        if len(request_files) < 1:
            raise AttributeError('Files missing from request')
        for file_key in request_files:
            current_app.logger.info(file_key)
            if not file_key == 'file':
                raise AttributeError('Form key for files must be \'file\'')
        files = request_files.getlist('file')
        for file in files:
            if not self.allowed_file(file.filename):
                raise AttributeError('File type extension \'' + file.filename.rsplit('.', 1)[1] + '\' is not allowed')

    def create_folder(self, path):
        file_folder = os.path.join(UPLOAD_FOLDER, path)
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)
        return file_folder

    def create_file_path(self, company, product):
        self.path = os.path.join(company, product)

    def save(self):
        """Saves the files to the specified path which should be based on company and product name

        Creates folder if not exists and places file in there based on company and product name

        Arguments:
            path {string} -- A path string created by joining company name with product name
        """

        files = self.request_files.getlist('file')
        for file in files:
            filename = secure_filename(file.filename)
            file_folder = self.create_folder(self.path)
            file_path = os.path.join(file_folder, filename)
            file.save(file_path)