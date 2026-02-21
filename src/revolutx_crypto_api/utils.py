import base64
import nacl.signing
import nacl.encoding

def sign_request(private_key: str, timestamp: str,
                 method: str, path: str, query: str = "", body: str = "") -> str:
    """
    Signs a request for Revolut X API.
    The string to sign is: timestamp + method + path + query + body
    """
    # Support for various private key formats
    raw_private = None
    if isinstance(private_key, str):
        try:
            # Try Hex first
            raw_private = bytes.fromhex(private_key)
        except ValueError:
            try:
                # Try Base64
                raw_private = base64.b64decode(private_key)
            except Exception:
                raw_private = private_key.encode('utf-8')
    else:
        raw_private = private_key

    # Use cryptography to parse PKCS8/DER/PEM if needed
    try:
        from cryptography.hazmat.primitives import serialization
        try:
            # Try loading as PEM/DER to extract raw seed
            # Note: We wrap it in try-except because it might already be raw 32 bytes
            if b"BEGIN PRIVATE KEY" in raw_private:
                key_obj = serialization.load_pem_private_key(raw_private, password=None)
            else:
                key_obj = serialization.load_der_private_key(raw_private, password=None)
            
            raw_private = key_obj.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
        except Exception:
            # If it's already 32 bytes or not a standard format, keep it as is
            pass
    except ImportError:
        pass

    if len(raw_private) != 32:
        # Fallback for common PKCS8 offset if cryptography is missing or fails
        if len(raw_private) == 48 and raw_private.startswith(b'\x30\x2e'):
             raw_private = raw_private[16:]
        else:
             raw_private = raw_private[:32]

    sk = nacl.signing.SigningKey(raw_private)
    message = f"{timestamp}{method}{path}{query}{body}".encode('utf-8')
    signed = sk.sign(message).signature
    return base64.b64encode(signed).decode('utf-8')
