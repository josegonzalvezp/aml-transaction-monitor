import pytest

from app.loaders.transaction_loader import TransactionLoader
from datetime import datetime


loader = TransactionLoader("data/input/transactions.csv")

transactions = loader.load()


def test_print_transaction():
    print(transactions[0])



def test_loader_converts_date_to_datetime(tmp_path):
    csv_content = """transaction_id;ordering_customer_id;ordering_customer_name;beneficiary_customer_id;beneficiary_customer_name;ordering_iban;ordering_country;ordering_bank;beneficiary_iban;beneficiary_country;beneficiary_bank;amount;currency;date;concept
T1;C1;Alice;C2;Bob;ES123;ES;Bank A;ES456;ES;Bank B;1000;EUR;2026-01-10;Transfer
"""

    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    loader = TransactionLoader(csv_file)
    transactions = loader.load()

    assert isinstance(transactions[0].date, datetime)


def test_loader_invalid_date_raises_error(tmp_path):
    csv_content = """transaction_id;ordering_customer_id;ordering_customer_name;beneficiary_customer_id;beneficiary_customer_name;ordering_iban;ordering_country;ordering_bank;beneficiary_iban;beneficiary_country;beneficiary_bank;amount;currency;date;concept
T1;C1;Alice;C2;Bob;ES123;ES;Bank A;ES456;ES;Bank B;1000;EUR;invalid_date;Transfer
"""

    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    loader = TransactionLoader(csv_file)

    with pytest.raises(ValueError):
        loader.load()


def test_loader_empty_date_raises_error(tmp_path):
    csv_content = """transaction_id;ordering_customer_id;ordering_customer_name;beneficiary_customer_id;beneficiary_customer_name;ordering_iban;ordering_country;ordering_bank;beneficiary_iban;beneficiary_country;beneficiary_bank;amount;currency;date;concept
T1;C1;Alice;C2;Bob;ES123;ES;Bank A;ES456;ES;Bank B;1000;EUR;;Transfer
"""

    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    loader = TransactionLoader(csv_file)

    with pytest.raises(ValueError):
        loader.load()



def test_loader_rejects_negative_amount(tmp_path):
    csv_content = (
        "transaction_id;ordering_customer_id;ordering_customer_name;"
        "beneficiary_customer_id;beneficiary_customer_name;"
        "ordering_iban;ordering_country;ordering_bank;"
        "beneficiary_iban;beneficiary_country;beneficiary_bank;"
        "amount;currency;date;concept\n"
        "T1;C1;Alice;C2;Bob;ES111;ES;Bank1;ES222;ES;Bank2;"
        "-500;EUR;2026-01-05;Test transaction\n"
    )

    file_path = tmp_path / "transactions.csv"
    file_path.write_text(csv_content, encoding="utf-8")

    loader = TransactionLoader(file_path)

    with pytest.raises(ValueError, match="Transaction amount cannot be negative"):
        loader.load()
