
import csv

from app.writers.alert_writer import AlertWriter


def test_alert_writer_creates_csv_without_alerts(tmp_path):
    file_path = tmp_path / "alerts.csv"

    AlertWriter(file_path)

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        rows = list(reader)

    assert rows == [
        ["alert_id", "transaction_id", "score", "broken_rules", "created_at"]
    ]
