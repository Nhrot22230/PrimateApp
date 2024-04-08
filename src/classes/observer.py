from abc import ABC, abstractmethod

class Subject(ABC):
    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self):
        pass

    @abstractmethod
    def notify(self, value=None):
        pass