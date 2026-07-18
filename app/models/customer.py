class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
    
    def __str__(self):
        return f"The client has id {self.customer_id} and its name is {self.name}."

    def __repr__(self):
        return f"Customer(customer_id = {self.customer_id}, name = {self.name})"


