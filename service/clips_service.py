from db import db
from entity import Clips


class ClipsService(object):
    """Clipsサービスクラス"""

    def __init__(self):
        self.db = db

    def find_by_id(self, clip_id):
        return Clips.get_or_none(Clips.clip_id == clip_id)

    def find_by_create_at_greater_than(self, date):
        return Clips.get_or_none(Clips.created_at > date)

    def find_top_15_date_after(self, date):
        return Clips.select().where(Clips.created_at > date).order_by(Clips.created_at.desc()).limit(15)

    def find_all_by_user_id(self, user_id):
        return Clips.select().where(Clips.user_id == user_id).order_by(Clips.created_at.desc())

    def create(self, clip):
        pass

    def bulk_insert(self, clips):
        if not clips:
            return

        with self.db.atomic():
            Clips.insert_many(clips).on_conflict("ignore").execute()

    def update(self, clip):
        if not clip:
            return

        pass

    def bulk_update(self, clips):
        if not clips:
            return

        pass
