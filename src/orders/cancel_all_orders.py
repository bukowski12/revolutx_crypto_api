def cancel_all_orders(client, symbol: str = None):
    """
    Cancel all active orders or filter by symbol.
    """
    params = {}
    if symbol: params["symbol"] = symbol
    return client.send("DELETE", "/orders", params=params)
