from entity.base_model import BaseModel
from entity.user import Users
from peewee import *
from db import db


class Queries(BaseModel):
    """クエリモデル"""
    query_id = CharField(primary_key=True)
    user = ForeignKeyField(Users, backref="queries", on_delete="CASCADE")
    query = CharField(max_length=255, null=False, unique=True)
    is_active = BooleanField(default=True)
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)

    class Meta:
        db_table = "queries"
        database = db


Queries.create_table()
