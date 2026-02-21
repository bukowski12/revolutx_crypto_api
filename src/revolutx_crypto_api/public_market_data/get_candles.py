def get_candles(client, symbol: str, timeframe: str, start: int = None, end: int = None):
    """
    Get historical price data (OHLCV).
    :param timeframe: GRANULARITY_ONE_MINUTE, GRANULARITY_FIVE_MINUTES, etc.
    """
    params = {"symbol": symbol, "timeframe": timeframe}
    if start: params["start"] = start
    if end: params["end"] = end
    return client.send("GET", "/public/candles", params=params)
