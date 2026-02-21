def get_public_order_book(client, symbol: str, depth: int = 50):
    """
    Get the current order book for a symbol.
    """
    params = {"symbol": symbol, "depth": depth}
    return client.send("GET", "/public/order-book", params=params)