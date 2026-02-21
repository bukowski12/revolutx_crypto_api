def cancel_order(client, order_id: str):
    return client.send("DELETE", f"/orders/{order_id}")
