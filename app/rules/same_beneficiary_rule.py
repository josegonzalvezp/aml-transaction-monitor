from app.rules.historical_rule import HistoricalRule


class SameBeneficiaryRule(HistoricalRule):

    def __init__(self, threshold, days):
        super().__init__(name="Same Beneficiary", score=30)
        self.threshold = threshold
        self.days = days

    def get_historical_transactions(self, transaction, context):
        return context.get_all_same_ord_ben_transactions(
            transaction,
            self.days
        )

    def evaluate(self, transaction, historical_transactions):
        return len(historical_transactions) > self.threshold
