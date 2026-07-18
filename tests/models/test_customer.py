from app.models.customer import Customer

def test_customer_creation():
    customer = Customer(
        customer_id="C001",
        name="Jose Gonzálvez"
    )

    assert customer.customer_id == "C001"
    assert customer.name == "Jose Gonzálvez"


def test_customer_str():
    customer = Customer(
        customer_id="C001",
        name="José García"
    )

    assert str(customer) == "The client has id C001 and its name is José García."


def test_customer_repr():
    customer = Customer(
        customer_id="C001",
        name="José García"
    )

    assert repr(customer) == "Customer(customer_id = C001, name = José García)"

