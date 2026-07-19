class Transaction:
    def __init__(self, transaction_id, ordering_account, beneficiary_account, amount, currency, date, concept):
        self.transaction_id = transaction_id
        self.ordering_account = ordering_account
        self.beneficiary_account = beneficiary_account
        self.amount = amount
        self.currency = currency
        self.date = date
        self.concept = concept
    
    def __str__(self):
        return f"{self.ordering_account.iban} -> {self.beneficiary_account.iban} \n {self.amount} {self.currency}"
    
    def __repr__(self):
        return f"Transaction(transaction_id = {self.transaction_id}, ordering_account = {repr(self.ordering_account)}, beneficiary_account = {repr(self.beneficiary_account)}, amount = {self.amount}, currency = {self.currency}, date = {self.date}, concept = {self.concept})"