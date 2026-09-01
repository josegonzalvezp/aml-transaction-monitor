from app.rules.historical_rule import HistoricalRule


class CumulativeOutgoingAmountRule(HistoricalRule):

    def __init__(self, threshold, days):
        super().__init__(name="Cumulative Outgoing Amount", score=30)
        self.threshold = threshold
        self.days = days

    def get_historical_transactions(self, transaction, context):
        return context.get_outgoing_transactions(
            transaction,
            self.days
        )

    def evaluate(self, transaction, historical_transactions):
        return sum(t.amount for t in historical_transactions) > self.threshold
