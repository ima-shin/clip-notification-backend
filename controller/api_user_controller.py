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

    query = current_user.queries.order_by(Queries.updated_at.desc()).first()
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
    identity = get_jwt_identity()
    current_user_id = identity.get("user_id", None)
    user = user_service.find_by_id(current_user_id)

    publish_to = request.json.get('publishTo', None)
    timing = request.json.get('timing', None)
    query = request.json.get('query', None)

    data = {
        'publish_to': request.json.get('publishTo', None),
        'timing': request.json.get('timing', None),
        'query': request.json.get('query', None),
    }

    if not any([data['publish_to'], data['timing'], data['query']]):
        abort(400)

    save_user_data(user, data)

    save_queries(user, query)

    return jsonify({'message': 'ok'}), 200


def save_user_data(user, data):
    user.publish_to = data['publish_to']
    user.publish_timing = data['timing']
    user.updated_at = datetime.now()

    user_service.update(user)


def save_queries(user, query_string):
    query = Queries(
        query_id=digest_util.create_digest(),
        user=user,
        query=query_string,
        is_active=True,
        is_deleted=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    q, created = query_service.get_or_create(query)
    if not created:
        q.updated_at = datetime.now()
        query_service.update(q)
