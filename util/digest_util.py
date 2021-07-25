import hashlib
import os
import random
import string


def create_digest():
    key = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    sha256 = hashlib.sha256(key.encode()).hexdigest()
    return sha256
