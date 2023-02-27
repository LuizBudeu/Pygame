from abc import ABC, abstractmethod


class Observer(ABC):
    
    @abstractmethod
    def on_notify(self, action):
        pass