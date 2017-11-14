from flask import Flask
from routes.entry import entry
from routes.users import users

app = Flask(__name__)

app.register_blueprint(entry)
app.register_blueprint(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
