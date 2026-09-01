from app.rules.transaction_rule import TransactionRule

class RoundAmountRule(TransactionRule):

    def __init__(self):
        super().__init__(
            name="Round Amount Rule",
            score=8
        )
    
    def evaluate(self, transaction):
        if transaction.amount % 1000 == 0:
            return True
        return False