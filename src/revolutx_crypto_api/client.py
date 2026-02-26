import time
import requests
import json
import logging

from .utils import sign_request
from .exceptions import RevolutXError, RevolutXAuthenticationError, RevolutXRateLimitError

logger = logging.getLogger(__name__)

class RevolutXClient:
    def __init__(self, api_key: str, private_key: str):
        """
        :param api_key: X-Revx-API-Key
        :param private_key: Ed25519 private key (hex string preferred)
        """
        self.api_key = api_key
        self.private_key = private_key
        self.base_url = "https://revx.revolut.com"

    def _headers(self, method: str, path: str, query: str = "", body: str = ""):
        timestamp = str(int(time.time() * 1000))
        signature = sign_request(
            self.private_key, timestamp, method, path, query, body
        )
        return {
            "X-Revx-API-Key": self.api_key,
            "X-Revx-Timestamp": timestamp,
            "X-Revx-Signature": signature,
            "Content-Type": "application/json",
        }

    def send(self, method: str, endpoint: str, params=None, json_body=None):
        method = method.upper()
        
        # Parse endpoint for query string if present
        if "?" in endpoint:
            endpoint, url_query = endpoint.split("?", 1)
            from urllib.parse import parse_qs
            url_params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(url_query).items()}
            if params:
                merged_params = params.copy()
                merged_params.update(url_params)
                params = merged_params
            else:
                params = url_params

        if not endpoint.startswith("/api/"):
            path = f"/api/1.0{endpoint}"
        else:
            path = endpoint

        url = f"{self.base_url}{path}"

        query_string = ""
        if params:
            query_string = requests.models.PreparedRequest()._encode_params(params)

        body_string = ""
        if json_body:
            body_string = json.dumps(json_body, separators=(',', ':'))

        headers = self._headers(method, path, query_string, body_string)
        
        try:
            resp = requests.request(method, url, headers=headers,
                                    params=params, json=json_body, timeout=10)
            
            if not resp.ok:
                self._handle_error(resp)
                
            if resp.status_code == 204 or not resp.text.strip():
                return {}
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {e}")
            raise RevolutXError(f"Network error: {e}")

    def _handle_error(self, response):
        status_code = response.status_code
        try:
            error_data = response.json()
            message = error_data.get("message", response.text)
            error_code = error_data.get("code")
        except Exception:
            message = response.text
            error_code = None

        if status_code == 401:
            raise RevolutXAuthenticationError(message, status_code, error_code, response.text)
        elif status_code == 429:
            raise RevolutXRateLimitError(message, status_code, error_code, response.text)
        else:
            raise RevolutXError(f"API Error ({status_code}): {message}", status_code, error_code, response.text)
