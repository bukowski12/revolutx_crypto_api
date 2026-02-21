def get_all_trades(client, **filters):
    return client.send("GET", "/trades", params=filters)
