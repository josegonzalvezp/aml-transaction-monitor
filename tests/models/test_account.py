from app.models.account import Account
from app.models.customer import Customer

def test_account_creation():
    customer = Customer(customer_id="C001",name="Jose Gonzálvez")
    account = Account(iban="ES213345", country="Spain", bank="BBVA", customer=customer)
    
    
    assert account.iban == "ES213345"
    assert account.country == "Spain"
    assert account.bank == "BBVA"
    assert account.customer.name == "Jose Gonzálvez"
    assert account.customer.customer_id == "C001"

def test_account_str():
    customer = Customer(customer_id="C001",name="Jose Gonzálvez")
    account = Account(iban="ES213345", country="Spain", bank="BBVA", customer=customer)

    assert str(account) == "Account information: the iban is ES213345, the country is Spain and the bank BBVA. The client id is C001."

def test_account_repr():
    customer = Customer(customer_id="C001",name="Jose Gonzálvez")
    account = Account(iban="ES213345", country="Spain", bank="BBVA", customer=customer)

    assert repr(account) == "Account(iban = ES213345, country = Spain, bank = BBVA, customer = Customer(customer_id = C001, name = Jose Gonzálvez))"
