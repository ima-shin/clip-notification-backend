from db import db
from entity import Queries


class QueryService(object):
    """クエリサービスクラス"""

    def __init__(self):
        self.db = db

    def find_by_and_user_id(self, query_id, user_id):
        return Queries.select().where(Queries.user_id == user_id).order_by(Queries.updated_at.desc())

    def find_by_user_id_and_is_active(self, user_id):
        return Queries.select().where(
            (Queries.user_id == user_id) and
            (Queries.is_active == True)
        ).order_by(Queries.updated_at.desc())

    def find_by_query_name_and_user_id(self, query, user_id):
        return Queries.select().where(
            (Queries.query == query) and
            (Queries.user_id == user_id)
        ).first()

    def get_or_create(self, query):
        with self.db.atomic():
            return Queries.get_or_create(
                query=query.query,
                user=query.user,
                defaults={
                    "query_id": query.query_id,
                    "is_active": query.is_active,
                    "is_deleted": query.is_deleted,
                    "created_at": query.created_at,
                    "updated_at": query.updated_at,
                }
            )

    def bulk_insert(self, queries):
        if not queries:
            return

        with self.db.atomic():
            Queries.insert_many(queries).on_conflict("ignore").execute()

    def update(self, query):
        if not query:
            return
        with self.db.atomic():
            query.save()
