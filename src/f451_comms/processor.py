"""Interface/base class for 'attribs' processors used in f451 Communications module.

This module is a base class for attribute processor objects used to handle various
message attributes across all services in the f451 Communications module.
"""
from abc import ABC
from abc import abstractmethod
from typing import Any


# =========================================================
#        M A I N   C L A S S   D E F I N I T I O N
# =========================================================
class AttributeProcessor(ABC):
    """Attribute validator base class for SciLab Communications module.

    Args:
        keyword:
            'attribs' keyword string
        required:
            'attrib' is required if True, else it's optional
    """

    def __init__(self, keyword: str, required: bool) -> None:
        self._valid = False
        self._keyword = keyword
        self._required = required

    def __repr__(self) -> str:
        return f"<AttributeProcessor, attribute={self._keyword}>"

    @property
    def keyword(self) -> str:
        """Return 'keyword' property."""
        return self._keyword

    @property
    def isRequired(self) -> bool:
        """Return 'isRequired' property."""
        return self._required

    @property
    def isValid(self) -> bool:
        """Return 'isValid' property."""
        return self._valid

    @property
    @abstractmethod
    def raw(self) -> Any:
        """Stub for class method/property."""
        pass

    @property
    @abstractmethod
    def clean(self) -> Any:
        """Stub for class method/property."""
        pass
