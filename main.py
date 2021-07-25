import datetime
import os
import time
import logging

from bots import *
from service import UsersService, ClipsService
from type import PublishTo
from api import YoutubeApi

if os.getenv("env") != "prod":
    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

# TODO: 非同期で一度にAPIを叩く回数。一瞬で5回APIを叩くことになるが、これが多いのか少ないのか。相手への負荷はどれくらいなのか...
MAX_WORKERS = 5
TIME_SLEEP = 2
TIMING = 30


user_service = UsersService()
clip_service = ClipsService()


def job(datum):
    """APIを叩き、通知を送信する"""
    youtube = YoutubeApi()
    clips = None
    try:
        clips = youtube.search(datum)
    except Exception as e:
        print(e)

    if clips:
        data_source = to_clips_model(clips, datum["user"])
        bot = datum.get("bot")
        try:
            clip_service.bulk_insert(data_source)
            bot.send_message(query=datum.get("query"), num=len(data_source))
        except Exception as e:
            # TODO: 適切なignore処理を
            print(e)

        # 各並列処理間で1秒待機する
        time.sleep(TIME_SLEEP)


def main():
    """現在時刻の前後30分以内のpublish_timingを持つユーザーを取得する"""
    users = []
    waiting_users = user_service.find_publish_timing_between(timing=TIMING)
    for user in waiting_users:
        datum = {}
        publish_to = user.publish_to  # 通知の送信先
        # botの選択
        if publish_to == PublishTo.SLACK.value:
            bot = SlackBot()
        elif publish_to == PublishTo.LINE.value:
            bot = LineBot()
        elif publish_to == PublishTo.EMAIL.value:
            bot = EmailBot(user.email)
        elif publish_to == PublishTo.FACEBOOK.value:
            bot = FacebookBot()
        elif publish_to == PublishTo.TWITTER.value:
            bot = TwitterBot()
        elif publish_to == PublishTo.DISCORD.value:
            bot = DiscordBot()
        else:
            bot = EmailBot(user.email)

        queries = list(user.queries)
        datum["last_published_at"] = user.last_published_at
        datum["query"] = queries[0].query if len(queries) > 0 else None
        datum["bot"] = bot
        datum["user"] = user

        try:
            job(datum)
            user.last_published_at = datetime.datetime.now()
        except Exception as e:
            print(e)
        users.append(user)
    # 正常に通知が送れたら、last_published_atとupdated_atを更新する
    user_service.bulk_update(users)


def to_clips_model(clips, user):
    if not clips:
        return
    """APIから取得した動画情報をClipsの辞書に変換する"""
    data_source = []
    for clip in clips:
        data = {
            "clip_id": clip["clip_id"],
            "user": user,
            "clip_title": clip["clip_title"],
            "channel_id": clip["channel_id"],
            "channel_title": clip["channel_title"],
            "published_at": clip["published_at"],
            "thumbnail_url": clip["thumbnail"],
            "is_visited": False,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
        }

        data_source.append(data)

    return data_source


if __name__ == "__main__":
    main()
