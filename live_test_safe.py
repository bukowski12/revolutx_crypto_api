import os
import json
from dotenv import load_dotenv
from revolutx_crypto_api.client import RevolutXClient
from revolutx_crypto_api.configuration.get_all_currency_pairs import get_all_currency_pairs
from revolutx_crypto_api.balance.get_all_balances import get_balances
from revolutx_crypto_api.orders.get_active_orders import get_active_orders
from revolutx_crypto_api.market_data.get_candles import get_candles

def main():
    # Load credentials from .env
    load_dotenv()
    api_key = os.getenv("api_key")
    private_key = os.getenv("private_key")

    if not api_key or not private_key:
        print("Error: api_key or private_key not found in .env file.")
        return

    print("--- Initializing Revolut X Client ---")
    client = RevolutXClient(api_key=api_key, private_key=private_key)

    try:
        # 1. Test Public Endpoint (Safe)
        print("\n1. Testing Public Endpoint: get_all_currency_pairs()...")
        pairs = get_all_currency_pairs(client)
        print(f"Success! Found {len(pairs)} pairs.")

        # 2. Test Private Endpoint: get_balances() (Safe)
        print("\n2. Testing Private Endpoint: get_balances()...")
        balances = get_balances(client)
        print("Success! Balances retrieved.")

        # 3. Test Private Endpoint: get_active_orders() (Safe)
        print("\n3. Testing Private Endpoint: get_active_orders()...")
        orders = get_active_orders(client)
        print(f"Success! Found {len(orders)} active orders.")
        print(json.dumps(orders, indent=2))

        # 4. Test Candles Endpoint (Safe)
        print("\n4. Testing Candles Endpoint: get_candles()...")
        candles = get_candles(client, symbol="BTC-EUR", interval="60")
        print("Success! Candles retrieved.")
        print(json.dumps(candles, indent=2))

    except Exception as e:
        print(f"\nAn error occurred during the test: {e}")
        if hasattr(e, 'response_text'):
            print(f"API Response: {e.response_text}")

if __name__ == "__main__":
    main()
