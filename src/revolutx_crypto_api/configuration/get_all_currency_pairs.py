def get_all_currency_pairs(client):
    """
    List all available trading pairs.
    """
    return client.send("GET", "/configuration/pairs")