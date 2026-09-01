from app.rules.transaction_rule import TransactionRule
from app.rules.historical_rule import HistoricalRule
from app.models.transaction import Transaction
from app.context.transaction_context import TransactionContext

class RuleEngine:

    def __init__(self, rules: list[Rule], transactions: list):
        self.rules = rules
        self.context = TransactionContext(transactions)

    def evaluate(self, transaction: Transaction):
        score = 0
        broken_rules = []
        for rule in self.rules:
            if isinstance(rule, TransactionRule):
                if rule.evaluate(transaction):
                    score += rule.score
                    broken_rules.append(rule)
            elif isinstance(rule, HistoricalRule):
                historical_transactions = rule.get_historical_transactions(transaction, self.context)
                if rule.evaluate(transaction, historical_transactions):
                    score += rule.score
                    broken_rules.append(rule)
        return score, broken_rules
    