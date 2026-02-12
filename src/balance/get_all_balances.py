def get_balances(client):
    """
    Retrieve all crypto exchange account balances.
    """
    return client.send("GET", "/balances")