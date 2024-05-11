class NotFoundError(Exception):
    """Exception raised when a resource is not found."""

class ApiRateLimitError(Exception):
    """Exception raised when the API rate limit is exceeded."""

class BadCredentialsError(Exception):
    """Exception raised when bad credentials are provided."""
