import datetime

from peewee import *
from entity.base_model import BaseModel
from db import db


class TempUsers(BaseModel):
    """
    仮登録ユーザーモデル
    id
    email
    token
    expirations
    created_at
    updated_at
    """
    id = CharField(max_length=64, primary_key=True)
    email = CharField(null=False)
    token = CharField(null=False)
    expirations = DateTimeField(null=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "temp_users"
        database = db


TempUsers.create_table()
