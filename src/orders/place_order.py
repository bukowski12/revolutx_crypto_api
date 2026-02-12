def place_order(client, order_config: dict):
    """
    Place a new Limit or Market order.
    :param order_config: Dictionary containing client_order_id, symbol, side, and order_configuration.
    """
    return client.send("POST", "/orders", json_body=order_config)
