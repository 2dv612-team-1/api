from flask import jsonify

def defaultResponse(message, status, rest={}):
  default = {
    'message': message,
    'status': status
  }
  default.update(rest)
  return jsonify(default), status
