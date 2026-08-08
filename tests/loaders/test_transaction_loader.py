from app.loaders.transaction_loader import TransactionLoader


loader = TransactionLoader("data/input/transactions.csv")

transactions = loader.load()


def test_print_transaction():
    print(transactions[0])