import datetime

from peewee import *

from util import digest_util
from entity.base_model import BaseModel

from db import db


class Users(BaseModel):
    """ユーザーモデル"""
    id = CharField(primary_key=True, max_length=64, index=True, default=digest_util.create_digest())
    email = CharField(unique=True)
    name = CharField(null=False)
    password_digest = CharField(null=False)
    publish_to = IntegerField(default=3)            # 通知先種別（デフォルト: メール）
    subscribe_status = BooleanField(default=True)   # 通知を受け取るか否か
    publish_timing = CharField(default="1800")      # 通知タイミング
    last_published_at = DateTimeField(null=True)    # 最後に通知した日時
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "users"
        database = db

    @property
    def clips(self):
        return self.clips.get()


Users.create_table()
