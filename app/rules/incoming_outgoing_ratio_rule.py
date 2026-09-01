from app.rules.historical_rule import HistoricalRule


class IncomingOutgoingRatioRule(HistoricalRule):

    def __init__(self, threshold, days):
        super().__init__(name="Incoming Outgoing Ratio", score=30)
        self.threshold = threshold
        self.days = days

    def get_historical_transactions(self, transaction, context):
        return context.get_all_transactions(
            transaction,
            self.days
        )

    def evaluate(self, transaction, historical_transactions):

        customer_id = transaction.ordering_account.customer.customer_id
        incoming_amount = 0
        outgoing_amount = 0

        for t in historical_transactions:
            if t.ordering_account.customer.customer_id == customer_id:
                outgoing_amount += t.amount
            elif t.beneficiary_account.customer.customer_id == customer_id:
                incoming_amount += t.amount

        if incoming_amount == 0:
            return False
    
        ratio = outgoing_amount / incoming_amount
        return ratio > self.threshold