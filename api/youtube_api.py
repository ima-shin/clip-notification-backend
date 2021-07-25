import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json
import urllib
from collections import defaultdict


class YoutubeApi(object):

    DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_API_VERSION = os.getenv("YOUTUBE_API_VERSION")
    YOUTUBE_API_SERVICE_NAME = "youtube"

    YOUTUBE = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # TODO: 要検討。約一日で投稿される数がどれくらいなのか調査する必要あり
    MAX_RESULTS = 30

    def search(self, options):
        # TODO tryで囲って適切なエラー処理を
        query = options.get("query", None)
        if not query:
            return
        try:
            response = self.YOUTUBE.search().list(
                part="id,snippet",
                q=query,
                type="video,channel",
                publishedAfter=options.get("last_published_at").isoformat() + "Z",
                maxResults=self.MAX_RESULTS,
                order="date",
                regionCode="JP",
            ).execute()
        except HttpError as e:
            print(e)
            raise Exception(e)
        except Exception as e:
            print(e)
            raise Exception(e)

        videos = []

        for res in response.get("items", []):
            if res["id"]["kind"] == "youtube#video":
                video = {
                    "clip_id": res["id"]["videoId"],
                    "clip_title": res["snippet"]["title"],
                    "channel_id": res["snippet"]["channelId"],
                    "channel_title": res["snippet"]["channelTitle"],
                    "published_at": res["snippet"]["publishedAt"],
                    "thumbnail": res["snippet"]["thumbnails"]["medium"]["url"],
                }

                videos.append(video)

        return videos
