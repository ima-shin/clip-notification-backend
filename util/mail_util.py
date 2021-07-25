import os
import smtplib
import urllib.parse
from email.mime.text import MIMEText

FROM = "kirinuki-noreply@kirinuki-tuti.net"
HOST = "smtp.kirinuki-tuti.net"
USERNAME = os.getenv("MAIL_USER")
PASSWORD = os.getenv("MAIL_PASS")


def send_temp_register(to, token):
    print(token)
    url = urllib.parse.urljoin(os.getenv("APP_DOMAIN"), f"/auth/signup?{urllib.parse.urlencode({'token': token})}")
    message = f"""
    <h1>本登録はまだ完了していません</h1>
    <p>メールの受信から1時間以内に以下のURLから本登録を完了してください</p>
    <br>
    <a href={url}>{url}</a>
    <br>
    <br>
    <p>※本メールは送信専用のため、ご返信いただくことはできません。</p>
    """

    mail = MIMEText(message, "html")
    mail["Subject"] = "仮登録完了 / kirinuki"
    mail["To"] = to
    mail["From"] = FROM

    smtp_client = smtplib.SMTP(HOST, 587, timeout=10)
    smtp_client.login(USERNAME, PASSWORD)
    smtp_client.send_message(mail)
    smtp_client.quit()


def send_complete_register(to):
    message = """
    <h2>ご登録ありがとうございます！本登録が完了しました。</h2>
    <br>
    <p><a href={}>ログイン画面</a> よりログインしてご利用を開始してください</p>
    <br>
    <br>
    <p>※本メールは送信専用のため、ご返信いただくことはできません。</p>
    """

    mail = MIMEText(message, "html")
    mail["Subject"] = "本登録完了 / kirinuki"
    mail["To"] = to
    mail["From"] = FROM

    smtp_client = smtplib.SMTP(HOST, 587)
    smtp_client.login(USERNAME, PASSWORD)
    smtp_client.send_message(mail)
    smtp_client.quit()


def send_clip_upload_notification(to, num):
    link = urllib.parse.urljoin(os.getenv("APP_DOMAIN"), "/user/my-page")
    message = f"""
    <h2>新たな切り抜き動画が {num} 本、投稿されました</h2>
    <p>早速、動画をチェックしにいきましょう！</p>
    <br/><br/>
    <a href={link}>{link}</a>
    <p>※本メールは送信専用のため、ご返信いただくことはできません。</p>"""
