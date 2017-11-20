"""
Main system file
"""

from flask import Flask
from routes.entry import entry
from routes.representatives import representatives
from routes.admin import admin
from routes.companies import companies
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)

APP.register_blueprint(entry)
APP.register_blueprint(representatives)
APP.register_blueprint(admin)
APP.register_blueprint(companies)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True, port=80)
