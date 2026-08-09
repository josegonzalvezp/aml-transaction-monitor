# AML Transaction Monitor

A Python-based Anti-Money Laundering (AML) transaction monitoring system designed to detect potentially suspicious financial activity through configurable rules and generate alerts for further investigation.

The project is being developed incrementally, starting with transaction-level rule evaluation and progressively moving towards historical and behavioral analysis.

---

## Project Overview

The system analyzes financial transactions and assigns a **risk score** based on the rules triggered by each transaction.

When the score exceeds a configurable threshold, an **Alert** is generated containing the relevant information about the transaction and the rules that were triggered.

The current version processes transactions from a CSV file and generates a separate alerts file for each execution day, allowing the resulting alerts to be reviewed independently by an AML analyst.

### Current workflow

```text
transactions.csv
       │
       ▼
TransactionLoader
       │
       ▼
List[Transaction]
       │
       ▼
RuleEngine
       │
       ├── Large Amount
       ├── Round Amount
       ├── Different Countries
       └── High Risk Country
       │
       ▼
Risk Score
       │
       ▼
Score > Alert Threshold?
       │
      YES
       │
       ▼
      Alert
       │
       ▼
  AlertWriter
       │
       ▼
alerts_YYYY-MM-DD.csv
       │
       ▼
    AML Analyst
```

---

## Project Structure

```text
aml-transaction-monitor/
│
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── account.py
│   │   ├── transaction.py
│   │   └── alert.py
│   │
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── rule.py
│   │   ├── large_amount_rule.py
│   │   ├── round_amount_rule.py
│   │   ├── different_countries_rule.py
│   │   └── high_risk_country_rule.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── rule_engine.py
│   │
│   ├── loaders/
│   │   ├── __init__.py
│   │   └── transaction_loader.py
│   │
│   └── writers/
│       ├── __init__.py
│       └── alert_writer.py
│
├── data/
│   └── transactions.csv
│
├── tests/
│   ├── models/
│   └── loaders/
│
├── main.py
├── README.md
└── requirements.txt
```

---

## Domain Model

### Customer

Represents a customer participating in financial transactions.

Main attributes:

* `customer_id`
* `name`

### Account

Represents a bank account belonging to a customer.

Main attributes:

* `iban`
* `country`
* `bank`
* `customer`

### Transaction

Represents a financial transaction between two accounts.

Main attributes:

* `transaction_id`
* `ordering_account`
* `beneficiary_account`
* `amount`
* `currency`
* `date`
* `concept`

### Rule

Defines a condition that can identify potentially suspicious transaction activity.

Each rule evaluates a transaction and returns whether the rule has been broken.

Rules also have an associated risk score.

### Alert

Represents a potentially suspicious transaction detected by the monitoring system.

An alert contains information such as:

* Alert ID
* Risk score
* Broken rules
* Creation timestamp
* Transaction information

---

## Current Rules

The current implementation includes four transaction-level rules.

### Large Amount Rule

Triggers when the transaction amount exceeds a configurable threshold.

Example:

```text
Transaction amount: €20,000
Threshold: €10,000

→ Rule triggered
```

### Round Amount Rule

Detects transactions with round amounts according to the configured rule.

Example:

```text
€5,000
€10,000
€20,000

→ Rule triggered
```

### Different Countries Rule

Detects transactions where the ordering and beneficiary accounts belong to different countries.

### High Risk Country Rule

Detects transactions involving countries included in the configured high-risk country list.

---

## Rule Engine

The `RuleEngine` receives a collection of rules and evaluates each transaction against all of them.

```text
Transaction
     │
     ├── Rule 1 → True
     ├── Rule 2 → False
     ├── Rule 3 → True
     └── Rule 4 → True
              │
              ▼
        Risk Score
              +
        Broken Rules
```

Each triggered rule contributes its configured score to the transaction's total risk score.

If the total score exceeds the configured alert threshold, an `Alert` is generated.

This approach allows new monitoring rules to be added without modifying the core evaluation logic.

---

## Data Loading

Transactions are currently loaded from a CSV dataset using `pandas`.

The `TransactionLoader` is responsible for:

1. Reading the CSV file.
2. Iterating through the transaction records.
3. Creating the corresponding `Customer` objects.
4. Creating the corresponding `Account` objects.
5. Creating the corresponding `Transaction` objects.
6. Returning a list of transactions.

The rest of the application does not need to know how the data was originally loaded.

---

## Alert Output

Detected alerts are exported to a daily CSV file.

Example:

```text
data/
└── alerts/
    ├── alerts_2026-08-09.csv
    ├── alerts_2026-08-10.csv
    └── alerts_2026-08-11.csv
```

The output is designed to provide an AML analyst with a manageable set of alerts to investigate for each execution day.

The current output contains information such as:

* `alert_id`
* `transaction_id`
* `score`
* `broken_rules`
* `created_at`

The `transaction_id` provides a direct reference back to the original transaction in the input dataset.

---

## Testing

The project uses `pytest` for automated testing.

Tests are being developed alongside the application classes to verify the behavior of individual components.

Current testing includes model and transaction loading functionality.

Tests can be executed from the project root with:

```bash
pytest
```

---

## Technologies

* **Python**
* **pandas**
* **pytest**
* **Git / GitHub**
* Object-Oriented Programming (OOP)
* CSV data processing

---

## Development Roadmap

### V1 — Transaction-level monitoring ✅

The first version established the core monitoring engine.

Implemented:

* Domain models
* Customer
* Account
* Transaction
* Rule abstraction
* Multiple transaction-level rules
* RuleEngine
* Risk scoring
* Alert generation
* Automated tests

The first version was initially designed around processing a single transaction.

---

### V2 — Batch processing and daily alert generation ✅

The second version moved the system from a single manually created transaction to a dataset-based workflow.

Implemented:

* CSV transaction dataset
* `TransactionLoader`
* Loading multiple transactions
* Batch transaction processing
* Daily alert output
* `AlertWriter`
* CSV-based alert reports
* Automated tests for the transaction loader

The system can now process a complete transaction dataset and generate a separate alert report for each execution day.

---

### V3 — Historical transaction analysis 🔜

The next major evolution will introduce **historical analysis**.

Instead of evaluating every transaction independently, the system will be able to consider groups of transactions belonging to the same customer or account over a period of time.

Potential rules include:

* Multiple transactions within a short time period
* Cumulative transaction amounts over a defined period
* Structuring / transaction splitting
* Sudden changes in transaction behavior
* Unusual numbers of countries or counterparties
* Behavioral deviations from historical activity

Example:

```text
Customer C001

€9,800
€9,700
€9,900
€9,600
€9,800
     │
     ▼
€48,800 within a short period
     │
     ▼
Historical / behavioral rule
     │
     ▼
Potential Alert
```

---

### Future Improvements

Possible future developments include:

* Historical customer profiles
* More sophisticated behavioral rules
* Database integration
* Persistent transaction and alert storage
* Configurable rule definitions
* Improved alert prioritization
* Risk scoring calibration
* Logging
* Configuration files
* API integration
* Dashboard for AML analysts
* Performance improvements for large datasets

---

## Project Objective

This project is intended as a practical Python project to explore how an AML transaction monitoring system can be designed using:

* Object-Oriented Programming
* Modular architecture
* Automated testing
* Data processing
* Rule-based risk assessment
* Batch processing
* Alert generation

The long-term goal is to evolve the initial rule-based system into a more realistic monitoring platform capable of identifying both **individual suspicious transactions and suspicious behavioral patterns across transaction history**.
