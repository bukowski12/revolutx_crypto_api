def get_ticker(client):
    return client.send("GET", "/market-data/ticker")