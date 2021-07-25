from flask import jsonify
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest, InternalServerError
from server import app


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    print(e)
    return jsonify({"message": "Bad Request."}), e.code


@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    print(e)
    return jsonify({"message": "Unauthorized."}), e.code


@app.errorhandler(NotFound)
def handle_not_found(e):
    print(e)
    return jsonify({"message": "Resource Not Found."}), e.code


@app.errorhandler(InternalServerError)
def handle_server_error(e):
    print(e)
    return jsonify({"message": "Internal Server Error."}), e.code
