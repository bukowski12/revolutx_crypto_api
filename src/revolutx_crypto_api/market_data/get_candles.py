def get_candles(client, symbol: str, interval: str):
    """
    Get historical OHLCV data.
    :param symbol: e.g. "BTC-EUR"
    :param interval: e.g. "60" (minutes)
    """
    # Path parameter style: /api/1.0/candles/{symbol}
    return client.send("GET", f"/candles/{symbol}", params={"interval": interval})
