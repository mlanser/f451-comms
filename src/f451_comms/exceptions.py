"""Exceptions classes for f451 Communications module.

This module holds the custom exceptions used across all providers in
the f451 Communications module.

Note:
    This module is inspired by the "Exceptions" module in the "Notifiers" module
    by Or Carmi: https://github.com/liiight/notifiers
"""
from typing import Any

# =========================================================
#          G L O B A L S   A N D   H E L P E R S
# =========================================================
_ERROR_UNKNOWN_: str = "Unknown error"


# =========================================================
#        M A I N   C L A S S   D E F I N I T I O N
# =========================================================
class f451CommsExceptionError(Exception):
    """Exception base class for f451 Communications module.

    Catch this exception to catch all custom exceptions from
    the f451 Communications module.

    Looks for ``provider``, ``message`` and ``data`` in kwargs

    Requires:
        'kwargs' keyword: 'errors'

    Args:
        args:
            exception arguments
        kwargs:
            exception kwargs
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.provider = kwargs.get("provider")
        self.message = kwargs.get("message")
        self.data = kwargs.get("data")
        self.response = kwargs.get("response")
        super().__init__(self.message)

    def __repr__(self) -> str:
        return f"<f451CommsError: {self.message}>"


class InvalidAttributeError(f451CommsExceptionError):
    """Invalid attribute error.

    Raised when given value is out of bounds and/or does not meet
    requirements for a given attribute/argument.

    Args:
        errMsg:
            error message for 'validation' failure
        args:
            exception arguments
        kwargs:
            exception kwargs
    """

    def __init__(self, errMsg: str, *args: Any, **kwargs: Any) -> None:
        kwargs["message"] = f"Invalid attribute error: {errMsg}"
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<InvalidAttributeError: {self.message}>"


class MissingAttributeError(f451CommsExceptionError):
    """Missing attribute error.

    Raised when required data attributes are missing.

    Args:
        errMsg:
            Error message for missing (required) 'attribute'
        args:
            Exception arguments
        kwargs:
            Exception kwargs
    """

    def __init__(self, errMsg: str, *args: Any, **kwargs: Any) -> None:
        kwargs["message"] = f"Missing attribute error: {errMsg}"
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<MissingAttributeError: {self.message}>"


class InvalidProviderError(f451CommsExceptionError):
    """Invalid service provider.

    Service provider is either unknown or not enabled.

    Args:
        errMsg:
            error message for missing (required) 'attribute'
        args:
            exception arguments
        kwargs:
            exception kwargs
    """

    def __init__(self, providerName: str, *args: Any, **kwargs: Any) -> None:
        self.name = providerName
        kwargs["message"] = f"Invalid service provider: {providerName}"
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<InvalidProviderError: {self.name}>"


class CommunicationsError(f451CommsExceptionError):
    """Communications error.

    This is raised when a service returns an error.

    Requires:
        'kwargs' keyword: 'errors'

    Args:
        args:
            exception arguments
        kwargs:
            exception kwargs
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.errors = kwargs.pop("errors", None)
        kwargs["message"] = (
            _ERROR_UNKNOWN_
            if self.errors is None
            else f"Communications errors: {','.join(self.errors)}"
        )
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<CommunicationsError: {self.message}>"
