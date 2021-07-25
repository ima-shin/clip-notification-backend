from abc import ABCMeta, abstractmethod


class AbstractBot(metaclass=ABCMeta):
    """ボット抽象クラス"""
    def __init__(self):
        pass

    @abstractmethod
    def send_message(self, query, num):
        """メッセージ送信抽象メソッド"""
        pass
