from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorator import content_type
from service import ClipsService


clip = Blueprint("clip_api", __name__, url_prefix="/clip")


clips_service = ClipsService()


@clip.route("/list", methods=["GET"])
@jwt_required()
@content_type("application/json")
def get_clip_list():
    current_user = get_jwt_identity()
    clips = clips_service.find_all_by_user_id(current_user.get("user_id", None))
    clip_list = [to_json(c) for c in clips]

    return jsonify({"status": 200, "message": "OK", "clip_list": clip_list}), 200


def to_json(clip):
    """clipモデルをJSON型に"""
    clip_json = {
        "clip_id": clip.clip_id,
        "clip_title": clip.clip_title,
        "channel_id": clip.channel_id,
        "channel_title": clip.channel_title,
        "published_at": clip.published_at.isoformat(),
        "thumbnail_url": clip.thumbnail_url,
        "is_visited": clip.is_visited,
        "created_at": clip.created_at.isoformat(),
        "updated_at": clip.updated_at.isoformat(),
    }
    return clip_json
