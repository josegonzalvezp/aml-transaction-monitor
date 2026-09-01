from app.rules.historical_rule import HistoricalRule


class TransactionFrequencyRule(HistoricalRule):

    def __init__(self, threshold, days):
        super().__init__(name="Transaction Frequency", score=30)
        self.threshold = threshold
        self.days = days

    def get_historical_transactions(self, transaction, context):
        return context.get_all_transactions(
            transaction,
            self.days
        )

    def evaluate(self, transaction, historical_transactions):
        number_of_transactions = len(historical_transactions)

        return number_of_transactions > self.threshold
