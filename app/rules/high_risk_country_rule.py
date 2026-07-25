from app.rules.rule import Rule

class HighRiskCountryRule(Rule):

    def __init__(self, countries):
        super().__init__(
            name="High Risk Country Rule",
            score=25
        )
        self.countries = countries

    def evaluate(self, transaction):
        if transaction.ordering_account.country in self.countries or transaction.beneficiary_account.country in self.countries:
            return True
        return False