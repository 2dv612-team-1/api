"""
Main system file
"""

from flask import Flask
from routes.entry import ENTRY
from routes.admin import ADMIN
from routes.companies import COMPANIES
from routes.auth import AUTH
from routes.consumers import CONSUMERS
from routes.products import PRODUCTS
from routes.categories import CATEGORIES
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

APP = Flask(__name__)
CORS(APP)
LIMITER = Limiter(
    APP,
    key_func=get_remote_address
)

LIMITER.limit("50/day;10/hour")(AUTH)

APP.register_blueprint(ENTRY)
APP.register_blueprint(CONSUMERS)
APP.register_blueprint(ADMIN)
APP.register_blueprint(COMPANIES)
APP.register_blueprint(CATEGORIES)
APP.register_blueprint(AUTH)
APP.register_blueprint(PRODUCTS)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True, port=80)
