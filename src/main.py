"""
Main system file
"""

from flask import Flask
from routes.entry import ENTRY
from routes.representatives import REPRESENTATIVES
from routes.admin import ADMIN
from routes.companies import COMPANIES
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

APP = Flask(__name__)
CORS(APP)
LIMITER = Limiter(
    APP,
    key_func=get_remote_address,
    default_limits=["50 per day", "10 per hour"]
)

APP.register_blueprint(ENTRY)
APP.register_blueprint(REPRESENTATIVES)
APP.register_blueprint(ADMIN)
APP.register_blueprint(COMPANIES)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True, port=80)
