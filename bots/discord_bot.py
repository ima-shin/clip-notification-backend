from bots.bot_abstract import AbstractBot


class DiscordBot(AbstractBot):
    """Discordボット"""
    def __init__(self):
        super().__init__()

    def send_message(self, message):
        pass
