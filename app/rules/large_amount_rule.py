from app.rules.transaction_rule import TransactionRule

class LargeAmountRule(TransactionRule):

    def __init__(self, threshold: float):
        super().__init__(
            name="Large Amount Rule",
            score=40
        )
        self.threshold = threshold

    def evaluate(self, transaction):
        return transaction.amount > self.threshold