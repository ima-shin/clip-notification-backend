from db import db
from entity import TempUsers
from datetime import datetime, timedelta
from util import digest_util


class TempUserServices(object):
    """TempUsersサービスクラス"""

    def __init__(self):
        self.db = db

    def find_by_token(self, token):
        return TempUsers.get_or_none(TempUsers.token == token)

    def create(self, email, token):
        with self.db.transaction():
            temp_user = TempUsers()
            temp_user.id = digest_util.create_digest()
            temp_user.email = email
            temp_user.token = token
            temp_user.expirations = datetime.now() + timedelta(hours=1)
            temp_user.created_at = datetime.now()
            temp_user.updated_at = datetime.now()

            temp_user.save(force_insert=True)
