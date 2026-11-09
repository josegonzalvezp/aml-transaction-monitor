# AML Transaction Monitor

A Python-based Anti-Money Laundering (AML) transaction monitoring system designed to detect potentially suspicious financial activity through configurable rules and generate alerts for further investigation.

The project is being developed incrementally, progressively introducing transaction-level and historical transaction analysis, with a focus on object-oriented programming, modular architecture, testing, and maintainability.

## Project Overview

The AML Transaction Monitor processes financial transactions and evaluates them against a set of configurable rules. When a transaction meets one or more suspicious activity criteria, the system generates an alert containing the transaction details, the triggered rules, and an aggregated risk score.

The system currently supports:

- Transaction-level rule evaluation.
- Historical transaction analysis over configurable time windows.
- Customer activity monitoring.
- Configurable rule scores and thresholds.
- CSV transaction loading and alert generation.
- Automated testing with pytest.

## Project Workflow

The application follows this general workflow:

1. **Data Loading:** Transactions are read from a CSV input file and converted into domain objects.
2. **Context Creation:** Historical transaction data is made available through `TransactionContext`.
3. **Rule Evaluation:** The `RuleEngine` evaluates each transaction against the configured monitoring rules.
4. **Alert Generation:** Transactions that trigger one or more rules generate an alert with an aggregated score.
5. **Output:** Generated alerts are exported to a CSV file for further investigation.

## Project Structure

The project follows a modular structure, separating domain models, transaction processing, rules, data loading, and output generation.

```text
aml-transaction-monitor/
|
+-- app/
|   |
|   +-- context/
|   |   +-- transaction_context.py
|   |
|   +-- engine/
|   |   +-- rule_engine.py
|   |
|   +-- exceptions/
|   |
|   +-- loaders/
|   |   +-- transaction_loader.py
|   |
|   +-- models/
|   |   +-- account.py
|   |   +-- alert.py
|   |   +-- customer.py
|   |   +-- transaction.py
|   |
|   +-- rules/
|   |   +-- cumulative_incoming_amount_rule.py
|   |   +-- cumulative_outgoing_amount_rule.py
|   |   +-- different_countries_rule.py
|   |   +-- high_risk_country_rule.py
|   |   +-- historical_rule.py
|   |   +-- incoming_outgoing_ratio_rule.py
|   |   +-- large_amount_rule.py
|   |   +-- number_beneficiaries_rule.py
|   |   +-- round_amount_rule.py
|   |   +-- rule.py
|   |   +-- same_beneficiary_rule.py
|   |   +-- transaction_frequency_rule.py
|   |   +-- transaction_rule.py
|   |
|   +-- utils/
|   |
|   +-- writers/
|       +-- alert_writer.py
|
+-- data/
|   |
|   +-- input/
|   |   +-- transactions.csv
|   |
|   +-- output/
|       +-- alerts_2026-08-09.csv
|       +-- alerts_2026-09-01.csv
|
+-- docs/
|   +-- README.md
|
+-- tests/
|   |
|   +-- context/
|   |   +-- test_transaction_context.py
|   |
|   +-- engine/
|   |
|   +-- loaders/
|   |   +-- test_transaction_loader.py
|   |
|   +-- models/
|   |   +-- test_account.py
|   |   +-- test_customer.py
|   |   +-- test_transaction.py
|   |
|   +-- rules/
|   |   +-- test_cumulative_incoming_amount_rule.py
|   |   +-- test_cumulative_outgoing_amount_rule.py
|   |   +-- test_incoming_outgoing_ratio_rule.py
|   |   +-- test_number_beneficiaries_rule.py
|   |   +-- test_same_beneficiary_rule.py
|   |   +-- test_transaction_frequency_rule.py
|   |
|   +-- writers/
|       +-- test_alert_writer.py
|
+-- main.py
+-- requirements.txt
+-- README.md
```

## Architecture and Main Components

### Domain Models

The application uses object-oriented domain models to represent the main entities involved in financial transactions:

- **Customer:** Represents a customer and their identifying information.
- **Account:** Represents a bank account, including its IBAN, country, bank, and associated customer.
- **Transaction:** Represents a financial transaction between an ordering account and a beneficiary account.
- **Alert:** Stores the information associated with a potentially suspicious transaction, including its score, triggered rules, and creation timestamp.

Transaction amounts are validated to prevent negative values.

### Rules

The monitoring logic is implemented through a modular rule system.

The project distinguishes between two types of rules:

- **TransactionRule:** Evaluates individual transaction characteristics.
- **HistoricalRule:** Evaluates transaction behaviour using historical activity.

This structure allows new monitoring rules to be introduced without modifying the core evaluation engine.

### Transaction Context

`TransactionContext` provides access to historical transactions associated with a customer.

It supports retrieving:

- Outgoing transactions.
- Incoming transactions.
- All transactions involving a customer.
- Transactions between a specific ordering customer and beneficiary customer.

Historical queries use configurable time windows and include transactions within the defined date boundaries.

### Rule Engine

`RuleEngine` is responsible for evaluating transactions against the configured rules.

It collects the rules triggered by each transaction and aggregates their scores to determine whether an alert should be generated.

### Data Loading

`TransactionLoader` uses pandas to read transaction data from CSV files.

It converts the input records into domain objects and handles date conversion and validation before returning the transactions to the application.

### Alert Generation and Output

When a transaction triggers monitoring rules, an `Alert` is generated.

`AlertWriter` exports alerts to CSV files, including:

- Alert ID.
- Transaction ID.
- Aggregated score.
- Triggered rules.
- Creation timestamp.

The output file is created with its headers even when no alerts are generated.

## Current Monitoring Rules

The project currently implements ten monitoring rules.

### Transaction-Level Rules

| Rule | Description |
|---|---|
| Large Amount | Detects transactions exceeding a configured amount threshold. |
| Round Amount | Detects transactions involving round monetary amounts. |
| Different Countries | Identifies transactions where the ordering and beneficiary accounts belong to different countries. |
| High Risk Country | Detects transactions involving countries classified as high risk. |

### Historical Rules

| Rule | Description |
|---|---|
| Cumulative Incoming Amount | Detects customers receiving a cumulative amount above a configured threshold within a time window. |
| Cumulative Outgoing Amount | Detects customers sending a cumulative amount above a configured threshold within a time window. |
| Incoming/Outgoing Ratio | Identifies unusual relationships between a customer's incoming and outgoing transaction amounts. |
| Number of Beneficiaries | Detects customers sending money to an unusually high number of different beneficiaries. |
| Same Beneficiary | Identifies repeated transactions between the same ordering customer and beneficiary. |
| Transaction Frequency | Detects unusually frequent transaction activity within a configured period. |

Each rule has its own evaluation logic and configurable parameters, such as thresholds, time windows, and risk scores.

## Testing

The project uses **pytest** for automated testing.

Tests are organized by component, covering:

- Domain model behaviour and validation.
- Transaction loading and date handling.
- Historical transaction retrieval and filtering.
- Individual historical monitoring rules.
- Alert CSV generation.

The test suite also covers edge cases, including invalid dates, negative transaction amounts, empty alert outputs, and transactions with unsorted dates.

To run the complete test suite:

```bash
python -m pytest -v
```

## Technologies

- **Python:** Main programming language.
- **Pandas:** CSV data loading and processing.
- **Pytest:** Automated testing.
- **Git:** Version control.

## Development Roadmap

The project is being developed incrementally:

| Version | Scope | Status |
|---|---|---|
| V1 | Initial domain models, transaction loading, basic monitoring rules, rule engine, and alert generation. | Completed |
| V2 | Improved object-oriented design and expanded transaction-level monitoring capabilities. | Completed |
| V3 | Historical transaction analysis, `TransactionContext`, and historical monitoring rules. | Completed |
| V3.1 | Expanded test coverage, date handling, edge-case validation, and code robustness improvements. | Completed |

## Future Improvements

Potential areas for further development include:

- Additional AML monitoring rules and more advanced behavioural patterns.
- Improved configuration management for monitoring rules and thresholds.
- More efficient processing of large transaction datasets.
- Database integration instead of relying exclusively on CSV files.
- API integration to expose monitoring functionality.
- More advanced alert prioritization and investigation workflows.
- Logging and improved exception handling.

## Project Objective

This project aims to build a modular and extensible AML transaction monitoring system while applying Python software development principles.

It serves as a practical project to strengthen skills in object-oriented programming, software architecture, data processing, automated testing, and financial crime prevention.