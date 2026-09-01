from app.rules.rule import Rule
from abc import abstractmethod


class HistoricalRule(Rule):

    @abstractmethod
    def get_historical_transactions(self, transaction, context):
        pass

    @abstractmethod
    def evaluate(self, transaction, historical_transactions):
        pass