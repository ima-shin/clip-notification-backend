import os
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from bots.bot_abstract import AbstractBot


class EmailBot(AbstractBot):
    """Emailボット"""

    FROM = "kirinuki-noreply@kirinuki-tuti.net"
    HOST = "smtp.kirinuki-tuti.net"
    USERNAME = os.getenv("MAIL_USER")
    PASSWORD = os.getenv("MAIL_PASS")

    def __init__(self, to):
        super().__init__()
        self.to = to

    def send_message(self, query, num):
        url = urllib.parse.urljoin(os.getenv("APP_DOMAIN"), "/user/my-page")

        message = f"""
        <h1>Kirinuki</h1>
        <h2>{query} の切り抜き動画が {num} 本投稿されています</h2>
        <br>
        <h2>さっそくチェックしに行きましょう！！</h2>
        <a href={url}>{url}</a>
        <br>
        <br>
        <p>※本メールは送信専用のため、ご返信いただくことはできません。</p>
        """

        mail = MIMEText(message, "html")
        mail["Subject"] = "切り抜き通知 / kirinuki"
        mail["To"] = self.to
        mail["From"] = self.FROM

        smtp_client = smtplib.SMTP(self.HOST, 587, timeout=10)
        smtp_client.login(self.USERNAME, self.PASSWORD)
        smtp_client.send_message(mail)
        smtp_client.quit()
