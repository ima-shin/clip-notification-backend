from flask import Blueprint, request, abort, jsonify
from decorator import content_type

from util import decrypt

bot = Blueprint("bot_callback", __name__, url_prefix="/bot")


@bot.route("/error", methods=["POST"])
@content_type("application/json")
def error():
    pass