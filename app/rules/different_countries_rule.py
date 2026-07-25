from app.rules.rule import Rule

class DifferentCountriesRule(Rule):
    def __init__(self):
        super().__init__(
            name="Different Countries Rule",
            score=10
        )

    def evaluate(self, transaction):
        if transaction.ordering_account.country != transaction.beneficiary_account.country:
            return True
        return False