import os

from Crypto.Cipher import AES
import base64
import hashlib


def encrypt():
    pass_phrase = os.getenv("PASS_PHRASE")
    _pass_phrase_base64 = _trans_multiple_of_16byte(base64.b64encode(pass_phrase.encode("utf8")))
    secret_key = hashlib.sha256(pass_phrase.encode()).digest()

    default_iv = os.getenv("DEFAULT_IV")
    iv = hashlib.md5(default_iv.encode("utf8")).digest()
    crypto = AES.new(secret_key, AES.MODE_CFB, iv)

    return crypto.encrypt(_pass_phrase_base64)


def decrypt(encoded_key):
    pass_phrase = os.getenv("PASS_PHRASE")
    secret_key = hashlib.sha256(pass_phrase.encode("utf8")).digest()
    default_iv = os.getenv("DEFAULT_IV")
    iv = hashlib.md5(default_iv.encode("utf8")).digest()
    crypto = AES.new(secret_key, AES.MODE_CFB, iv)

    encoded_key_base64 = _reverse_multiple_of_16byte(encoded_key)
    encoded_key_base64 = crypto.decrypt(encoded_key_base64)

    return base64.b64decode(encoded_key_base64).decode("utf8")


def _trans_multiple_of_16byte(key):
    surplus = len(key)  % 16
    if surplus != 0:
        for i in range(16 - surplus):
            key += "_".encode("utf8")
    return key


def _reverse_multiple_of_16byte(key):
    cnt = 0
    while "_".encode("utf8") == key[-1]:
        key.pop()
        if cnt > 100:
            break
    return key
