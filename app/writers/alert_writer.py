import csv

class AlertWriter:
    def __init__(self, archivo):
        self.archivo = archivo

        with open(self.archivo, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
        
            writer.writerow(["alert_id", "transaction_id", "score", "broken_rules", "created_at"])

    def write(self, alert):

        broken_rules = ", ".join(
                rule.name for rule in alert.broken_rules
        )


        with open(self.archivo, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")

            writer.writerow([alert.alert_id, alert.transaction.transaction_id, alert.score, broken_rules, alert.created_at])

            
