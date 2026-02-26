def get_ticker(client):
    return client.send("GET", "/tickers")