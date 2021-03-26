from abc import ABC
from abc import abstractmethod


class Step(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(self, data, inputs, utils):
        pass


class StepException(Exception):  # 預防程式錯誤的停止後 須執行的動作
    pass
