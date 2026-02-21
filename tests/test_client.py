import unittest
from unittest.mock import patch, MagicMock
from revolutx_crypto_api.client import RevolutXClient
from revolutx_crypto_api.utils import sign_request
from revolutx_crypto_api.exceptions import RevolutXError, RevolutXAuthenticationError, RevolutXRateLimitError
import base64
import json

class TestRevolutXClient(unittest.TestCase):
    def setUp(self):
        # Sample hex ed25519 seed (32 bytes)
        self.api_key = "test_api_key"
        self.private_key = "0" * 64 
        self.client = RevolutXClient(self.api_key, self.private_key)

    def test_signature_generation(self):
        # Test based on documentation logic: timestamp + method + path + query + body
        timestamp = "1765360896219"
        method = "POST"
        path = "/api/1.0/orders"
        query = ""
        body = '{"client_order_id":"3b364427-1f4f-4f66-9935-86b6fb115d26"}'
        
        signature = sign_request(self.private_key, timestamp, method, path, query, body)
        
        # Verify it's valid base64
        try:
            decoded = base64.b64decode(signature)
            self.assertEqual(len(decoded), 64) # Ed25519 signature is 64 bytes
        except Exception as e:
            self.fail(f"Signature is not valid base64: {e}")

    @patch('requests.request')
    def test_client_send_get(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"balance": "1.0"}
        mock_response.status_code = 200
        # Important: mock raise_for_status to not do anything
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        endpoint = "/balances"
        result = self.client.send("GET", endpoint)

        self.assertEqual(result, {"balance": "1.0"})
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "GET")
        self.assertTrue(args[1].endswith("/api/1.0/balances"))
        self.assertIn("X-Revx-Signature", kwargs['headers'])

    @patch('requests.request')
    def test_client_send_post_with_body(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123"}
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        order_data = {"symbol": "BTC-USD", "side": "BUY"}
        result = self.client.send("POST", "/orders", json_body=order_data)

        self.assertEqual(result, {"id": "123"})
        args, kwargs = mock_request.call_args
        self.assertEqual(args[0], "POST")
    @patch('requests.request')
    def test_client_authentication_error(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.ok = False
        mock_response.json.return_value = {"message": "Invalid API Key", "code": "AUTH_FAILED"}
        mock_request.return_value = mock_response

        with self.assertRaises(RevolutXAuthenticationError) as cm:
            self.client.send("GET", "/balances")
        
        self.assertEqual(cm.exception.status_code, 401)
        self.assertEqual(cm.exception.api_error_code, "AUTH_FAILED")

    @patch('requests.request')
    def test_client_rate_limit_error(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.ok = False
        mock_response.json.return_value = {"message": "Too many requests"}
        mock_request.return_value = mock_response

        with self.assertRaises(RevolutXRateLimitError):
            self.client.send("GET", "/balances")

    def test_signature_with_base64_key(self):
        # 32 bytes of zeros in base64
        b64_key = base64.b64encode(b'\x00' * 32).decode('utf-8')
        timestamp = "1765360896219"
        signature = sign_request(b64_key, timestamp, "GET", "/api/1.0/balances")
        self.assertTrue(len(base64.b64decode(signature)) == 64)

if __name__ == '__main__':
    unittest.main()
