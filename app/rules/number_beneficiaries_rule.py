from app.rules.historical_rule import HistoricalRule


class NumberBeneficiariesRule(HistoricalRule):

    def __init__(self, threshold, days):
        super().__init__(name="Number of Beneficiaries", score=30)
        self.threshold = threshold
        self.days = days

    def get_historical_transactions(self, transaction, context):
        return context.get_outgoing_transactions(
            transaction,
            self.days
        )

    def evaluate(self, transaction, historical_transactions):
        beneficiary_list = []
        for t in historical_transactions:
            if t.beneficiary_account.customer.customer_id not in beneficiary_list:
                beneficiary_list.append(t.beneficiary_account.customer.customer_id)

        return len(beneficiary_list) > self.threshold
