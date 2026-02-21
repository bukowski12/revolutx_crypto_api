def get_order_fills(client, order_id: str):
    return client.send("GET", f"/orders/{order_id}/fills")