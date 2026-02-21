def get_active_orders(client, **filters):
    return client.send("GET", "/orders/active", params=filters)
