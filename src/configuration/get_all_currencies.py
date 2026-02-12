def get_all_currencies(client):
    return client.send("GET", "/configuration/currencies")
