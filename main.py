from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.alert import Alert

from app.loaders.transaction_loader import TransactionLoader

from app.writers.alert_writer import AlertWriter

from app.rules.large_amount_rule import LargeAmountRule
from app.rules.high_risk_country_rule import HighRiskCountryRule
from app.rules.different_countries_rule import DifferentCountriesRule
from app.rules.round_amount_rule import RoundAmountRule

from app.engine.rule_engine import RuleEngine

from datetime import datetime


ALERT_THRESHOLD = 60




def create_sample_transaction():


    customer_1 = Customer(
        customer_id="C001",
        name="Jose Gonzálvez"
    )

    customer_2 = Customer(
        customer_id="C002",
        name="Javier"
    )


    account_1 = Account(
        iban="ES213345",
        country="Spain",
        bank="BBVA",
        customer=customer_1
    )

    account_2 = Account(
        iban="IR987654",
        country="Iran",
        bank="Bank Melli",
        customer=customer_2
    )



    transaction = Transaction(
        transaction_id=123,
        ordering_account=account_1,
        beneficiary_account=account_2,
        amount=20000,
        currency="EUR",
        date="19-07-2026",
        concept="Party"
    )

    return transaction

def create_rules():
    rules = [
        LargeAmountRule(threshold=10000),
        HighRiskCountryRule(countries=['Iran', 'China', 'Russia']),
        DifferentCountriesRule(),
        RoundAmountRule()
    ]
    return rules

def print_results(score, broken_rules):

    print(f"Risk Score: {score}")

    if score > 0:
        print("\nBroken Rules:")

        for rule in broken_rules:
            print(f"- {rule.name} ({rule.score} points)")


def main():

    alert_id = 1

    loader = TransactionLoader("data/input/transactions.csv")

    transactions = loader.load()

    #transaction = create_sample_transaction()
    
    rules = create_rules()
    
    engine = RuleEngine(rules)

    today = datetime.now().strftime("%Y-%m-%d")

    writer = AlertWriter(f"data/output/alerts_{today}.csv")

    for transaction in transactions:

        score, broken_rules = engine.evaluate(transaction)

        #print_results(score, broken_rules)
    

        if score > ALERT_THRESHOLD:
        #    print('\nAn alert is created.\n')
            alert = Alert(alert_id, transaction, score, broken_rules, datetime.now())
        #    print(alert)

            writer.write(alert)

            alert_id += 1


if __name__ == '__main__':
    main()

