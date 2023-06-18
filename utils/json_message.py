from flask import jsonify


def json_message(message, status=200):
    return jsonify({"message": message}), status
