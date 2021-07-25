import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from bots.bot_abstract import AbstractBot


class SlackBot(AbstractBot):

    API_TOKEN = os.getenv("SLACK_API_TOKEN")
    CLIENT = WebClient(API_TOKEN)

    def __init__(self):
        super().__init__()

    def send_message(self, message):
        try:
            response = self.CLIENT.chat_postMessage(channel="C02462S8R8Q", text=message)
        except SlackApiError as e:
            print(f"got an error: {e.response['error']}")
