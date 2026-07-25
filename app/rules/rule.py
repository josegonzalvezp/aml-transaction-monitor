from abc import ABC, abstractmethod

class Rule(ABC):
    def __init__(self, name: str, score: int):
        self.name = name
        self.score = score

    @abstractmethod
    def evaluate(self, transaction):
        pass