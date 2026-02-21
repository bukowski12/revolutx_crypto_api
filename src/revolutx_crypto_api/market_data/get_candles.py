def get_candles(client, pair: str, timeframe: str):
    return client.send("GET", f"/market-data/candles?pair={pair}&timeframe={timeframe}")
