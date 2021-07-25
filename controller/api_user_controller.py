from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorator import content_type
from service import UsersService, QueryService
from entity import Queries
from util import digest_util

user = Blueprint("user_api", __name__, url_prefix="/user")

user_service = UsersService()
query_service = QueryService()


@user.route("/info", methods=["GET"])
@jwt_required()
@content_type("application/json")
def get_user_info():

    identity = get_jwt_identity()
    current_user_id = identity.get("user_id", None)
    current_user = user_service.find_by_id(current_user_id)

    query = current_user.queries.first()
    query = query.query if query else None

    payload = {
        "user_id": current_user.id,
        "email": current_user.email,
        "publish_to": current_user.publish_to,
        "publish_timing": current_user.publish_timing,
        "query": query,
        "created_at": current_user.created_at.isoformat(),
        "updated_at": current_user.updated_at.isoformat(),
    }

    return jsonify({"content": payload, "message": "OK"}), 200


@user.route("/info/update", methods=["POST"])
@jwt_required()
@content_type("application/json")
def update_user_info():
    return


@user.route("/settings/update", methods=["POST"])
@jwt_required()
@content_type("application/json")
def update_notification_setting():
    print('update_notification_setting start;')
    identity = get_jwt_identity()
    current_user_id = identity.get("user_id", None)
    user = user_service.find_by_id(current_user_id)

    publish_to = request.json.get('publishTo', None)
    timing = request.json.get('timing', None)
    query = request.json.get('query', None)

    if not any([publish_to, timing, query]):
        abort(400)

    if publish_to:
        user.publish_to = publish_to
        user.updated_at = datetime.now()

    if timing:
        user.publish_timing = timing
        user.updated_at = datetime.now()

    if query:
        q = Queries(
            query_id=digest_util.create_digest(),
            user=user,
            is_active=True,
            is_deleted=False,
            create_at=datetime.now(),
            updated_at=datetime.now(),
        )

        q, created = query_service.get_or_create(q)
        if created:
            q.updated_at = datetime.now()
            query_service.update(q)

    return jsonify({'message': 'ok'}), 200
