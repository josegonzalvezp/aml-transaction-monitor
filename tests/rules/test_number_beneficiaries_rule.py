
from datetime import datetime

from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction
from app.context.transaction_context import TransactionContext
from app.rules.number_beneficiaries_rule import NumberBeneficiariesRule


def create_transaction(transaction_id, ordering_id, beneficiary_id, amount, date):

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
        amount,
        "EUR",
        date,
        "Test transaction"
    )


def test_number_beneficiaries_above_threshold():

    rule = NumberBeneficiariesRule(threshold=2, days=5)

    historical_transactions = [
        create_transaction("T1", "A", "B", 1000, datetime(2026, 1, 7)),
        create_transaction("T2", "A", "C", 1000, datetime(2026, 1, 8)),
        create_transaction("T3", "A", "D", 1000, datetime(2026, 1, 9))
    ]

    result = rule.evaluate(None, historical_transactions)

    assert result is True


def test_number_beneficiaries_below_threshold():

    rule = NumberBeneficiariesRule(threshold=3, days=5)

    historical_transactions = [
        create_transaction("T1", "A", "B", 1000, datetime(2026, 1, 7)),
        create_transaction("T2", "A", "C", 1000, datetime(2026, 1, 8))
    ]

    result = rule.evaluate(None, historical_transactions)

    assert result is False


def test_number_beneficiaries_equal_threshold():

    rule = NumberBeneficiariesRule(threshold=2, days=5)

    historical_transactions = [
        create_transaction("T1", "A", "B", 1000, datetime(2026, 1, 7)),
        create_transaction("T2", "A", "C", 1000, datetime(2026, 1, 8))
    ]

    result = rule.evaluate(None, historical_transactions)

    assert result is False


def test_number_beneficiaries_empty_history():

    rule = NumberBeneficiariesRule(threshold=2, days=5)

    result = rule.evaluate(None, [])

    assert result is False


def test_number_beneficiaries_no_duplicates():

    rule = NumberBeneficiariesRule(threshold=2, days=5)

    historical_transactions = [
        create_transaction("T1", "A", "B", 1000, datetime(2026, 1, 7)),
        create_transaction("T2", "A", "B", 2000, datetime(2026, 1, 8)),
        create_transaction("T3", "A", "B", 3000, datetime(2026, 1, 9))
    ]

    result = rule.evaluate(None, historical_transactions)

    assert result is False


def test_number_beneficiaries_get_historical_transactions():

    rule = NumberBeneficiariesRule(threshold=2, days=5)

    transactions = [
        create_transaction("T1", "A", "B", 1000, datetime(2026, 1, 5)),
        create_transaction("T2", "A", "C", 1000, datetime(2026, 1, 8)),
        create_transaction("T3", "D", "A", 1000, datetime(2026, 1, 9)),
        create_transaction("T4", "A", "D", 1000, datetime(2025, 12, 30))
    ]

    current_transaction = create_transaction(
        "T5", "A", "E", 1000, datetime(2026, 1, 10)
    )

    context = TransactionContext(transactions)

    result = rule.get_historical_transactions(
        current_transaction,
        context
    )

    result_ids = [t.transaction_id for t in result]

    assert result_ids == ["T1", "T2"]
