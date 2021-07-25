import datetime

from peewee import *
from entity.base_model import BaseModel
from entity.user import Users
from db import db


class Clips(BaseModel):
    """動画情報モデル"""
    clip_id = CharField(primary_key=True)  # ビデオID
    user = ForeignKeyField(Users, backref="clips", on_delete="CASCADE")
    clip_title = CharField(null=False)            # ビデオタイトル
    channel_id = CharField(null=False)            # チャンネルID
    channel_title = CharField(null=False)         # チャンネル名
    published_at = DateTimeField(null=False)      # 投稿日
    thumbnail_url = CharField(null=False)         # サムネイルURL
    is_visited = BooleanField(default=False)      # 訪問済みフラグ

    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "clips"
        database = db


Clips.create_table()
