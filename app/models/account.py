class Account:
    def __init__(self, iban, country, bank, customer):
        self.iban = iban
        self.country = country
        self.bank = bank
        self.customer = customer

    def __str__(self):
        return f"Account information: {self.iban} - {self.country} - {self.bank} - {self.customer.name}."

    def __repr__(self):
        return f"Account(iban = {self.iban}, country = {self.country}, bank = {self.bank}, customer = {repr(self.customer)})"