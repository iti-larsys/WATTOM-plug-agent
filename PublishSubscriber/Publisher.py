from abc import ABC, abstractmethod

class Publisher(ABC):

    subscribers = []

    def add(self, subscriber):
        """
        Adds a subscriber to a list of subdcrivers
        :param other:
        :return:
        """
        self.subscribers.append(subscriber)


    def notify(self,data):
        """
        Notifies all subscribers that a change has happened
        :return:
        """
        for subscriber in self.subscribers:
            subscriber.update(data)

    #Don't need to implement this thing
    #def remove(self):
    #    pass