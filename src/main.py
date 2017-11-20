"""
Main system file
"""

from flask import Flask
from routes.entry import entry
from routes.representatives import representatives
from routes.admin import admin
from routes.companies import companies
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(entry)
app.register_blueprint(representatives)
app.register_blueprint(admin)
app.register_blueprint(companies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
