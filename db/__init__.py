import os

from peewee import *


db = MySQLDatabase(
    os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
    port=3306, host=os.getenv("DB_HOST"), charset="utf8mb4"
)

try:
    db.connect()
except OperationalError as e:
    print(e)
    raise OperationalError
