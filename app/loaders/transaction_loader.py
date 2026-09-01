import pandas as pd

from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction

class TransactionLoader:
    def __init__(self, archivo):
        self.archivo = archivo

    def load(self):
        df = pd.read_csv(self.archivo, sep=";")
        df["date"] = pd.to_datetime(df["date"])
        transactions = []

        for _, row in df.iterrows():

            customer_1 = Customer(row["ordering_customer_id"], row["ordering_customer_name"])
            customer_2 = Customer(row["beneficiary_customer_id"], row["beneficiary_customer_name"])

            account_1 = Account(row["ordering_iban"], row["ordering_country"], row["ordering_bank"], customer_1)
            account_2 = Account(row["beneficiary_iban"], row["beneficiary_country"], row["beneficiary_bank"], customer_2)

            transaction = Transaction(row["transaction_id"], account_1, account_2, row["amount"], row["currency"], row["date"], row["concept"])

            transactions.append(transaction)

        return transactions