from app.rules.rule import Rule
from app.models.transaction import Transaction

class RuleEngine:

    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def evaluate(self, transaction: Transaction):
        score = 0
        broken_rules = []
        for rule in self.rules:
            if rule.evaluate(transaction):
                score += rule.score
                broken_rules.append(rule)
        return score, broken_rules
    