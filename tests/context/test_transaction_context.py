
from datetime import datetime

from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction
from app.context.transaction_context import TransactionContext


def create_transaction(
    transaction_id,
    ordering_id,
    beneficiary_id,
    date
):
    ordering_customer = Customer(ordering_id, ordering_id)
    beneficiary_customer = Customer(beneficiary_id, beneficiary_id)

    ordering_account = Account(
        f"IBAN_{ordering_id}",
        "Spain",
        "Bank A",
        ordering_customer
    )

    beneficiary_account = Account(
        f"IBAN_{beneficiary_id}",
        "Spain",
        "Bank B",
        beneficiary_customer
    )

    return Transaction(
        transaction_id,
        ordering_account,
        beneficiary_account,
        1000,
        "EUR",
        date,
        "Test transaction"
    )


def create_test_data():
    transactions = [
        create_transaction("T1", "A", "C", datetime(2026, 1, 5)),
        create_transaction("T2", "D", "A", datetime(2026, 1, 7)),
        create_transaction("T3", "A", "B", datetime(2026, 1, 8)),
        create_transaction("T4", "X", "Y", datetime(2026, 1, 9)),
        create_transaction("T5", "A", "B", datetime(2026, 1, 10)),
        create_transaction("T6", "A", "C", datetime(2025, 12, 30)),
        create_transaction("T7", "A", "C", datetime(2026, 1, 11)),
    ]

    return transactions


def test_get_outgoing_transactions():

    transactions = create_test_data()
    context = TransactionContext(transactions)

    current_transaction = transactions[4]

    result = context.get_outgoing_transactions(
        current_transaction,
        days=5
    )

    result_ids = [t.transaction_id for t in result]

    assert result_ids == ["T1", "T3", "T5"]


def test_get_incoming_transactions():

    transactions = create_test_data()
    context = TransactionContext(transactions)

    current_transaction = transactions[4]

    result = context.get_incoming_transactions(
        current_transaction,
        days=5
    )

    result_ids = [t.transaction_id for t in result]

    assert result_ids == ["T3", "T5"]



def test_get_all_transactions():

    transactions = create_test_data()
    context = TransactionContext(transactions)

    current_transaction = transactions[4]

    result = context.get_all_transactions(
        current_transaction,
        days=5
    )

    result_ids = [t.transaction_id for t in result]

    assert result_ids == ["T1", "T2", "T3", "T5"]


def test_get_all_same_ord_ben_transactions():

    transactions = create_test_data()
    context = TransactionContext(transactions)

    current_transaction = transactions[4]

    result = context.get_all_same_ord_ben_transactions(
        current_transaction,
        days=5
    )

    result_ids = [t.transaction_id for t in result]

    assert result_ids == ["T3", "T5"]


def test_get_outgoing_transactions_empty_history():

    transactions = create_test_data()
    context = TransactionContext(transactions)

    current_transaction = transactions[4]

    result = context.get_outgoing_transactions(
        current_transaction,
        days=0
    )

    assert result == [current_transaction]


def test_get_outgoing_transactions_empty_history():

    transactions = create_test_data()

    current_transaction = transactions[4]

    other_transactions = [
        t for t in transactions
        if t.transaction_id == "T4"
    ]

    context = TransactionContext(other_transactions)

    result = context.get_outgoing_transactions(
        current_transaction,
        days=5
    )

    assert result == []


def test_get_outgoing_transactions_includes_start_date():

    transactions = create_test_data()
    context = TransactionContext(transactions)

    current_transaction = transactions[4]

    result = context.get_outgoing_transactions(
        current_transaction,
        days=5
    )

    result_ids = [t.transaction_id for t in result]

    assert "T1" in result_ids



def test_get_outgoing_transactions_excludes_future_transactions():

    transactions = create_test_data()
    context = TransactionContext(transactions)

    current_transaction = transactions[4]

    result = context.get_outgoing_transactions(
        current_transaction,
        days=5
    )

    result_ids = [t.transaction_id for t in result]

    assert "T7" not in result_ids



def test_get_all_transactions_same_customer():

    transaction = create_transaction(
        "T8",
        "A",
        "A",
        datetime(2026, 1, 10)
    )

    context = TransactionContext([transaction])

    result = context.get_all_transactions(
        transaction,
        days=5
    )

    assert len(result) == 1
    assert result[0].transaction_id == "T8"



def test_get_all_same_ord_ben_transactions_multiple():

    transactions = [
        create_transaction("T1", "A", "B", datetime(2026, 1, 5)),
        create_transaction("T2", "A", "B", datetime(2026, 1, 7)),
        create_transaction("T3", "A", "C", datetime(2026, 1, 8)),
        create_transaction("T4", "B", "A", datetime(2026, 1, 9)),
    ]

    context = TransactionContext(transactions)

    current_transaction = transactions[3]

    result = context.get_all_same_ord_ben_transactions(
        current_transaction,
        days=5
    )

    result_ids = [t.transaction_id for t in result]

    assert result_ids == ["T4"]






def test_get_outgoing_transactions_unsorted_dates():
    transactions = [
        create_transaction("T1", "A", "B", datetime(2026, 1, 8)),
        create_transaction("T2", "A", "C", datetime(2026, 1, 5)),
        create_transaction("T3", "A", "D", datetime(2026, 1, 10)),
        create_transaction("T4", "A", "E", datetime(2025, 12, 30)),
        create_transaction("T5", "B", "A", datetime(2026, 1, 9)),
    ]

    context = TransactionContext(transactions)

    current_transaction = create_transaction(
        "T6", "A", "F", datetime(2026, 1, 10)
    )

    result = context.get_outgoing_transactions(
        current_transaction,
        days=5
    )

    assert {t.transaction_id for t in result} == {"T1", "T2", "T3"}

