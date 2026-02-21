def get_order(client, order_id: str):
    return client.send("GET", f"/orders/{order_id}")
