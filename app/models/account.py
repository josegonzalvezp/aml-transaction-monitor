class Account:
    def __init__(self, iban, country, bank, customer):
        self.iban = iban
        self.country = country
        self.bank = bank
        self.customer = customer

    def __str__(self):
        return f"Account information: the iban is {self.iban}, the country is {self.country} and the bank {self.bank}. The client id is {self.customer.customer_id}."

    def __repr__(self):
        return f"Account(iban = {self.iban}, country = {self.country}, bank = {self.bank}, customer = Customer(customer_id = {self.customer.customer_id}, name = {self.customer.name}))"