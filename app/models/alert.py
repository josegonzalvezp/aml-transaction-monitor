class Alert:
    def __init__(self, alert_id, transaction, score, broken_rules, created_at):
        self.alert_id = alert_id
        self.transaction = transaction
        self.score = score
        self.broken_rules = broken_rules
        self.created_at = created_at
    
    def __str__(self):
        rules = ", ".join(rule.name for rule in self.broken_rules)            
        return f"Alert information: {self.alert_id}  -  {self.score}  -  {rules}  -  {self.created_at}"

    def __repr__(self):
        return f"Alert(alert_id = {self.alert_id}, transaction = {self.transaction}, score = {self.score}, broken_rules = {self.broken_rules}, created_at = {self.created_at})"
    

