from app.rules.rule import Rule

class LargeAmountRule(Rule):

    def __init__(self, threshold: float):
        super().__init__(
            name="Large Amount Rule",
            score=40
        )
        self.threshold = threshold

    def evaluate(self, transaction):
        if transaction.amount > self.threshold:
            return True
        return False