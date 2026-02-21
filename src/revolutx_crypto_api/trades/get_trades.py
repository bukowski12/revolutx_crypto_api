def get_trades(client, symbol: str = None, limit: int = 100, order_id: str = None):
    """
    Retrieve your historical trade executions.
    """
    params = {}
    if symbol: params["symbol"] = symbol
    if limit: params["limit"] = limit
    if order_id: params["order_id"] = order_id
    return client.send("GET", "/trades", params=params)
