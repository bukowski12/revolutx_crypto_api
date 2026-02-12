def get_last_trades(client, symbol: str):
    """
    Get the most recent trades for a symbol.
    """
    params = {"symbol": symbol}
    return client.send("GET", "/public/last-trades", params=params)
