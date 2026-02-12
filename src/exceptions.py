class RevolutXError(Exception):
    """Base exception for Revolut X API."""
    def __init__(self, message, status_code=None, api_error_code=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.api_error_code = api_error_code
        self.response_text = response_text

class RevolutXAuthenticationError(RevolutXError):
    """Raised when authentication fails."""
    pass

class RevolutXRateLimitError(RevolutXError):
    """Raised when rate limit is exceeded."""
    pass

class RevolutXOrderError(RevolutXError):
    """Raised when an order operation fails."""
    pass
