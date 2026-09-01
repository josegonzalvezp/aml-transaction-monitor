from datetime import timedelta

class TransactionContext:
    def __init__(self, transactions):
        self.transactions = transactions

    def get_outgoing_transactions(self, transaction, days):

        customer_id = transaction.ordering_account.customer.customer_id
        start_date = transaction.date - timedelta(days=days)

        historical_transactions = [
            t for t in self.transactions
            if t.ordering_account.customer.customer_id == customer_id
            and start_date <= t.date <= transaction.date
        ]

        return historical_transactions

    def get_incoming_transactions(self, transaction, days):

        customer_id = transaction.beneficiary_account.customer.customer_id
        start_date = transaction.date - timedelta(days=days)

        historical_transactions = [
                    t for t in self.transactions
                    if t.beneficiary_account.customer.customer_id == customer_id
                    and start_date <= t.date <= transaction.date
                ]
        
        return historical_transactions

    def get_all_transactions(self, transaction, days):

        customer_id = transaction.ordering_account.customer.customer_id
        start_date = transaction.date - timedelta(days=days)

        historical_transactions = [
            t for t in self.transactions
            if (
            t.ordering_account.customer.customer_id == customer_id
            or
            t.beneficiary_account.customer.customer_id == customer_id
        ) and start_date <= t.date <= transaction.date
        ]

        return historical_transactions

    def get_all_same_ord_ben_transactions(self, transaction, days):
    
            customer_id_ord = transaction.ordering_account.customer.customer_id
            customer_id_ben = transaction.beneficiary_account.customer.customer_id
            start_date = transaction.date - timedelta(days=days)
    
            historical_transactions = [
                t for t in self.transactions
                if (
                t.ordering_account.customer.customer_id == customer_id_ord
                and
                t.beneficiary_account.customer.customer_id == customer_id_ben
            ) and start_date <= t.date <= transaction.date
            ]
    
            return historical_transactions

    