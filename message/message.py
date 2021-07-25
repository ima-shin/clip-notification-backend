import os
import textwrap


class Message(object):
    """メッセージ作成クラス"""
    def __init__(self, clip_num):
        self.clip_num = clip_num

    def create_message(self):
        message = f"""
        新たな切り抜き動画が {self.clip_num} 本投稿されました！
        下のURLをクリックして今すぐチェックしましょう！
        {os.getenv("APP_URL")}
        """
        message = textwrap.dedent(message)

        return message
