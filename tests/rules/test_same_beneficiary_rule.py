
from datetime import datetime

from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction
from app.rules.same_beneficiary_rule import SameBeneficiaryRule


def create_transaction(
    transaction_id,
    ordering_customer_id,
    beneficiary_customer_id,
    date
):
    ordering_customer = Customer(ordering_customer_id, ordering_customer_id)
    beneficiary_customer = Customer(beneficiary_customer_id, beneficiary_customer_id)

    ordering_account = Account(
        f"ES{ordering_customer_id}",
        "ES",
        "Bank A",
        ordering_customer
    )

    beneficiary_account = Account(
        f"ES{beneficiary_customer_id}",
        "ES",
        "Bank B",
        beneficiary_customer
    )

    return Transaction(
        transaction_id,
        ordering_account,
        beneficiary_account,
        1000,
        "EUR",
        datetime.strptime(date, "%Y-%m-%d"),
        "Test transaction"
    )


def test_same_beneficiary_above_threshold():
    rule = SameBeneficiaryRule(threshold=2, days=30)

    historical_transactions = [
        create_transaction("T1", "A", "B", "2026-01-01"),
        create_transaction("T2", "A", "B", "2026-01-02"),
        create_transaction("T3", "A", "B", "2026-01-03"),
    ]

    assert rule.evaluate(None, historical_transactions) is True


def test_same_beneficiary_below_threshold():
    rule = SameBeneficiaryRule(threshold=3, days=30)

    historical_transactions = [
        create_transaction("T1", "A", "B", "2026-01-01"),
        create_transaction("T2", "A", "B", "2026-01-02"),
    ]

    assert rule.evaluate(None, historical_transactions) is False


def test_same_beneficiary_equal_threshold():
    rule = SameBeneficiaryRule(threshold=2, days=30)

    historical_transactions = [
        create_transaction("T1", "A", "B", "2026-01-01"),
        create_transaction("T2", "A", "B", "2026-01-02"),
    ]

    assert rule.evaluate(None, historical_transactions) is False


def test_same_beneficiary_empty_history():
    rule = SameBeneficiaryRule(threshold=0, days=30)

    assert rule.evaluate(None, []) is False


def test_same_beneficiary_get_historical_transactions():
    rule = SameBeneficiaryRule(threshold=2, days=5)

    current_transaction = create_transaction(
        "T5", "A", "B", "2026-01-10"
    )

    transactions = [
        create_transaction("T1", "A", "B", "2026-01-05"),
        create_transaction("T2", "A", "B", "2026-01-08"),
        create_transaction("T3", "B", "A", "2026-01-09"),
        create_transaction("T4", "A", "C", "2026-01-09"),
        create_transaction("T6", "A", "B", "2025-12-30"),
    ]

    from app.context.transaction_context import TransactionContext

    context = TransactionContext(transactions)

    result = rule.get_historical_transactions(current_transaction, context)

    assert [t.transaction_id for t in result] == ["T1", "T2"]


def test_same_beneficiary_does_not_reverse_direction():
    rule = SameBeneficiaryRule(threshold=0, days=30)

    current_transaction = create_transaction(
        "T3", "A", "B", "2026-01-10"
    )

    transactions = [
        create_transaction("T1", "B", "A", "2026-01-05"),
        create_transaction("T2", "A", "B", "2026-01-08"),
    ]

    from app.context.transaction_context import TransactionContext

    context = TransactionContext(transactions)

    result = rule.get_historical_transactions(current_transaction, context)

    assert [t.transaction_id for t in result] == ["T2"]
