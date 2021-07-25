from enum import Enum


class PublishTo(Enum):
    """通知先種別"""
    SLACK = 0
    LINE = 1
    EMAIL = 2
    TWITTER = 3
    FACEBOOK = 4
    DISCORD = 5
