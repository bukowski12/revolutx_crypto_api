def get_historical_orders(client, **filters):
    return client.send("GET", "/orders/historical", params=filters)
