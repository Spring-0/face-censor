from abc import ABC, abstractmethod

class DetectionModel(ABC):
    @abstractmethod
    def detect(self, frame):
        pass