def get_private_trades(client, **filters):
    return client.send("GET", "/trades/private", params=filters)