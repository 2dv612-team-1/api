from flask import jsonify

def defaultResponse(message, status):
  return jsonify({
    'message': message,
    'status': status
  }), status
