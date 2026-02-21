def get_order_book(client, pair: str, limit: int = 50):
    return client.send("GET", f"/market-data/order-book?pair={pair}&limit={limit}")
