from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from werkzeug.routing import Rule
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest, InternalServerError
from argparse import ArgumentParser
from decorator import content_type
import os
from datetime import timedelta
from controller.api_auth_controller import auth as auth_blue_print
from controller.api_clip_controller import clip as clip_blue_print
from controller.api_user_controller import user as user_blue_print

app = Flask(__name__)

app.secret_key = os.getenv("APP_SECRET")

jwt = JWTManager(app)

app.register_blueprint(auth_blue_print)
app.register_blueprint(clip_blue_print)
app.register_blueprint(user_blue_print)

app.config["JSON_SORT_KEYS"] = False
app.config["JWT_TOKEN_LOCATION"] = "headers"
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_DECODE_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=300)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_ENCODE_ISSUER"] = "@kirinuki-tuti.net"
app.config["JWT_DECODE_ISSUER"] = "@kirinuki-tuti.net"
app.config["JWT_AUTH_URL_RULE"] = "/api/auth"
app.config["JWT_HEADER_TYPE"] = ""  # Bearerとかつけるのめんどくさいのでprefixは無しで


@jwt.invalid_token_loader
def invalid_token_loader(response):
    print(f"invalid token {response}")
    return jsonify(response)


@jwt.expired_token_loader
def expired_token_loader(headers, payload):
    """期限切れのアクセストークンが送られてきたときに発火"""
    print(f"token expired {headers}")
    return jsonify(
        {"status": 401, "require_refresh": True, "message": "Token has expired. "}
    ), 401


@app.route("/auth/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
@content_type("application/json")
def token_refresh():
    """header内のリフレッシュトークンを見て、validなら新しいaccess_tokenを返す"""
    identity = get_jwt_identity()
    if not identity:
        return jsonify({"status": 400, "message": "Invalid refresh token."}), 400

    access_token = create_access_token(identity=identity)
    return jsonify({"status": 200, "message": "OK", "access_token": access_token}), 200


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


class CustomURLPrefix(Rule):
    def __init__(self, string, *args, **kwargs):
        super(CustomURLPrefix, self).__init__(os.getenv("API_ROOT") + string, *args, **kwargs)


# app.url_rule_class = CustomURLPrefix

@app.errorhandler(BadRequest)
@app.errorhandler(Unauthorized)
@app.errorhandler(NotFound)
@app.errorhandler(InternalServerError)
def error_handler(e):
    res = jsonify({"error": {"name": e.name, "description": e.description}})
    return res, e.code


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=int(os.environ.get('PORT', 8000)), help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    arg_parser.add_argument('--host', default='0.0.0.0', help='host')
    options = arg_parser.parse_args()

    app.run(host=options.host, port=options.port, debug=True if not os.getenv("env") == "prod" else False)
