from app.models.account import Account
from app.models.customer import Customer
from app.models.transaction import Transaction

def test_transaction_creation():
    customer_1 = Customer(customer_id="C001",name="Jose Gonzálvez")
    account_1 = Account(iban="ES213345", country="Spain", bank="BBVA", customer=customer_1)
    customer_2 = Customer(customer_id="C002",name="Javier")
    account_2 = Account(iban="GE6789", country="Germany", bank="DB", customer=customer_2)

    transaction = Transaction(transaction_id = 123, ordering_account = account_1, beneficiary_account = account_2, amount = 5000, currency = "EUR", date="19-07-2026", concept = "Party")

    assert transaction.transaction_id == 123
    assert transaction.ordering_account == account_1
    assert transaction.beneficiary_account == account_2
    assert transaction.amount == 5000
    assert transaction.currency == "EUR"
    assert transaction.concept == "Party"
    assert transaction.date == "19-07-2026"

def test_transaction_str():
    customer_1 = Customer(customer_id="C001",name="Jose Gonzálvez")
    account_1 = Account(iban="ES213345", country="Spain", bank="BBVA", customer=customer_1)
    customer_2 = Customer(customer_id="C002",name="Javier")
    account_2 = Account(iban="GE6789", country="Germany", bank="DB", customer=customer_2)

    transaction = Transaction(transaction_id = 123, ordering_account = account_1, beneficiary_account = account_2, amount = 5000, currency = "EUR", date="19-07-2026", concept = "Party")

    assert str(transaction) == "ES213345 -> GE6789 \n 5000 EUR"

def test_transaction_repr():
    customer_1 = Customer(customer_id="C001",name="Jose Gonzálvez")
    account_1 = Account(iban="ES213345", country="Spain", bank="BBVA", customer=customer_1)
    customer_2 = Customer(customer_id="C002",name="Javier")
    account_2 = Account(iban="GE6789", country="Germany", bank="DB", customer=customer_2)

    transaction = Transaction(transaction_id = 123, ordering_account = account_1, beneficiary_account = account_2, amount = 5000, currency = "EUR", date="19-07-2026", concept = "Party")

    expected = (
        "Transaction("
        "transaction_id = 123, "
        "ordering_account = Account(iban = ES213345, country = Spain, bank = BBVA, customer = Customer(customer_id = C001, name = Jose Gonzálvez)), "
        "beneficiary_account = Account(iban = GE6789, country = Germany, bank = DB, customer = Customer(customer_id = C002, name = Javier)), "
        "amount = 5000, currency = EUR, date = 19-07-2026, concept = Party)"
    )

    assert repr(transaction) == expected