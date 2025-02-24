class BaseException(Exception):
    """Base class for all exceptions raised by this package."""

    pass


class APIError(BaseException):
    """Exception raised for errors in the API response."""

    pass


class InvalidMobileNumberError(BaseException):
    """Exception raised for invalid mobile number format."""

    pass
