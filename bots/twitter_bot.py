from bots.bot_abstract import AbstractBot


class TwitterBot(AbstractBot):
    """Twitterボット"""
    def __init__(self):
        super().__init__()

    def send_message(self, message):
        pass
