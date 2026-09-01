from app.rules.rule import Rule
from abc import abstractmethod


class TransactionRule(Rule):

    @abstractmethod
    def evaluate(self, transaction):
        pass