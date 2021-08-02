import datetime

from werkzeug.security import check_password_hash

from db import db
from entity import Users, Clips, Queries


TIMING = 60


class UsersService(object):
    """Usersサービスクラス"""
    def __init__(self):
        self.db = db

    def identify(self, email, password_digest):
        user = self.find_by_email(email)
        if user and check_password_hash(user.password_digest, password_digest):
            return user

    def find_by_id(self, user_id):
        return Users.get_or_none(Users.id == user_id)

    def find_by_email(self, email):
        return Users.get_or_none(Users.email == email)

    def find_publish_timing_between(self, before=datetime.datetime.now() - datetime.timedelta(minutes=30),
                                    later=datetime.datetime.now() + datetime.timedelta(minutes=30), timing=30):
        """指定時間内のpublish_timingを持つユーザーを全て取得（ただし通知をONにしているかつ前後60分以内に通知を実行していないユーザーのみ）"""
        later_TIMING = later
        later_TIMING_int = time_to_int(later_TIMING)
        before_TIMING = before
        before_TIMING_int = time_to_int(before_TIMING)
        return Users.select().join(Queries.user == Users.id).where(
            Users.subscribe_status &
            (Users.publish_timing >= before_TIMING_int) &
            (Users.publish_timing <= later_TIMING_int) &
            ~(Users.last_published_at.between(before_TIMING, later_TIMING))
        ).order_by(Queries.updated_at.desc())

    def create(self, user):
        with self.db.transaction():
            user.save(force_insert=True)

    def bulk_insert(self, users):
        if not users:
            return

        with self.db.atomic():
            Users.insert_many(users).on_conflict("ignore").execute()

    def update(self, user):
        with self.db.atomic():
            user.save()

    def bulk_update(self, users):
        if not users:
            return

        with self.db.atomic():
            Users.bulk_update(users, fields=["last_published_at", "updated_at"])


def time_to_int(time):
    """datetimeからHHMM型の文字列を抽出する"""
    return int(time.strftime("%H%M"))
