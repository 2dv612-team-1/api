"""
Main system file
"""

from flask import Flask
from routes.entry import ENTRY_ROUTER
from routes.admin import ADMIN_ROUTER
from routes.companies import COMPANIES_ROUTER
from routes.auth import AUTH_ROUTER
from routes.consumers import CONSUMERS_ROUTER
from routes.products import PRODUCTS_ROUTER
from routes.categories import CATEGORIES_ROUTER
from routes.materials import MATERIALS_ROUTER
from routes.annotations import ANNOTATIONS_ROUTER

from flask_cors import CORS
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

APP = Flask(__name__)
CORS(APP)
# LIMITER = Limiter(
#     APP,
#     key_func=get_remote_address
# )

# LIMITER.limit("50/day;10/hour")(AUTH)

APP.register_blueprint(ENTRY_ROUTER)
APP.register_blueprint(CONSUMERS_ROUTER)
APP.register_blueprint(ADMIN_ROUTER)
APP.register_blueprint(COMPANIES_ROUTER)
APP.register_blueprint(CATEGORIES_ROUTER)
APP.register_blueprint(MATERIALS_ROUTER)
APP.register_blueprint(AUTH_ROUTER)
APP.register_blueprint(PRODUCTS_ROUTER)
APP.register_blueprint(ANNOTATIONS_ROUTER)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True, port=80)
