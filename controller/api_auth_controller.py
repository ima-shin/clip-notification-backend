from flask import Blueprint, request, abort, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from decorator import content_type
from service import UsersService, TempUserServices
from entity import Users
from type import ApiErrorType, PublishTo

from util import digest_util, mail_util

auth = Blueprint("auth_api", __name__, url_prefix="/auth")


user_service = UsersService()
temp_user_service = TempUserServices()


@auth.route("/token/verify", methods=["GET"])
@jwt_required()
@content_type("application/json")
def verify_access_token():
    """アクセストークンを検証する"""
    identity = get_jwt_identity()
    if not identity:
        return abort(400)

    new_access_token = create_access_token(identity=identity)
    return jsonify({"message": "OK", "access_token": new_access_token}), 200


@auth.route("/login", methods=["POST"])
@content_type("application/json")
def login():
    # Google認証後、ユーザーデータを保存する
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = user_service.find_by_email(email)
    if user and check_password_hash(user.password_digest, password):
        # userオブジェクトをJSON形式に変換
        user_json = {"user_id": user.id}
        access_token = create_access_token(identity=user_json)
        refresh_token = create_refresh_token(identity=user_json)
        response = {
            "status": 200, "tokens": {"user_id": user.id, "access_token": access_token, "refresh_token": refresh_token}
        }
        return jsonify(response), 200
    else:
        # 認証失敗
        return abort(400)


@auth.route("/temp/save", methods=["POST"])
@content_type("application/json")
def save_temp_user():
    """ユーザー仮登録"""
    payload = request.json
    email = payload.get("email")

    if not email:
        abort(400)

    exist = user_service.find_by_email(email)
    if exist:
        return jsonify(
            {"status": 200, "message": "User already exists", "type": ApiErrorType.USER_ALREADY_EXISTS.value}
        ), 200

    token = digest_util.create_digest()

    temp_user_service.create(email, token)

    mail_util.send_temp_register(to=email, token=token)

    return jsonify({"status": 200, "message": "OK", "options": None}), 200


@auth.route("/temp/fetch", methods=["GET"])
@content_type("application/json")
def fetch_temp_user():
    """仮登録ユーザー存在確認"""
    token = request.args.get("token")
    if not token:
        return jsonify({"message": "Invalid url."}), 400

    temp_user = temp_user_service.find_by_token(token)
    if not temp_user:
        return jsonify({"message": "Temp user doesn't exist."}), 400
    elif temp_user.expirations < datetime.now():
        return jsonify({"message": "This token has been expired."}), 401

    return jsonify({"status": 200, "message": "OK", "email": temp_user.email}), 200


@auth.route("/user/signup", methods=["POST"])
@content_type("application/json")
def signup():
    """ユーザー本登録"""
    payload = request.json

    user_id = digest_util.create_digest()
    token = payload.get("token")
    password = payload.get("password")

    exist_temp = temp_user_service.find_by_token(token)
    if not exist_temp:
        return jsonify({"message": "Temp user doesn't exist."}), 401

    exist_user = user_service.find_by_email(exist_temp.email)
    if not exist_user:
        user = Users()
        user.id = user_id
        user.email = exist_temp.email
        user.password_digest = generate_password_hash(password)
        user.publish_to = PublishTo.EMAIL.value
        user.created_at = datetime.now()
        user.updated_at = datetime.now()
        user_service.create(user)

        return jsonify({"status": 200, "message": "OK"}), 200

    else:
        return abort(401)
