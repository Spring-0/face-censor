from abc import ABC, abstractmethod

class CensoringMethod(ABC):
    @abstractmethod
    def apply(self, frame, bbox):
        pass