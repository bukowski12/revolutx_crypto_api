def get_quote(client, symbol: str):
    """
    Get the latest buy/sell prices for a symbol.
    """
    params = {"symbol": symbol}
    return client.send("GET", "/public/quote", params=params)
