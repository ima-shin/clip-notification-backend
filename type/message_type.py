from enum import Enum


class MessageType(Enum):
    """メッセージタイプ"""
    # メール件名
    SUBJECT_TEMP_REGISTER = "仮登録完了 / kirinuki"
    SUBJECT_USER_REGISTER = "本登録完了 / kirinuki"
    SUBJECT_UPLOAD_NOTIFICATION = "切り抜き動画が投稿されました / kirinuki"

    # フォームエラー
    GENERAL_FORM_ERROR = "入力内容に不備があります"
    USER_ALREADY_EXISTS = "すでに登録済みのユーザーです"
    INVALID_URL = "不正なURLです"

    # 認証エラー
    URL_TOKEN_EXPIRED = "リンクの有効期限が切れているか、未登録です。もう一度仮登録からやり直してください。"
    INVALID_EMAIL_OR_PASS = "メールアドレスとパスワードの組み合わせが間違っています"
    LOGIN_REQUIRED = "ログインが必要です"

    # 正常系
    SIGNUP_COMPLETED = "登録が完了しました。"
    LOGIN_COMPLETED = "ログインに成功しました。"
