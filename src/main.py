"""
Main system file
"""

from flask import Flask
from routes.entry import ENTRY
from routes.representatives import REPRESENTATIVES
from routes.admin import ADMIN
from routes.companies import COMPANIES
from routes.users import USERS
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)

APP.register_blueprint(ENTRY)
APP.register_blueprint(REPRESENTATIVES)
APP.register_blueprint(USERS)
APP.register_blueprint(ADMIN)
APP.register_blueprint(COMPANIES)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True, port=80)
