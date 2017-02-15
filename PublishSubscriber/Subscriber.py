from abc import ABC, abstractmethod

class Subscriber(ABC):

    @abstractmethod
    def update(self,data):
        """
        What a subscriber after the publisher receive a value
        :param data:
        :return:
        """
        pass
