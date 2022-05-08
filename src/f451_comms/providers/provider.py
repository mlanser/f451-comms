"""Interface/base classes used in f451 Communications module.

This module holds various base classes used for various service
providers (e.g. email, Slack, Twilio, Twitter, etc.).
"""
import imghdr
import logging
import pprint
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional

from requests import Response as reqResponse
from rich import print as rprint
from rich.pretty import pprint as rpp
from rich.rule import Rule

import f451_comms.constants as const
import f451_comms.utils as utils
from f451_comms.exceptions import CommunicationsError
from f451_comms.exceptions import InvalidAttributeError
from f451_comms.processor import AttributeProcessor

__all__ = [
    "Media",
    "Response",
    "Provider",
    "verify_file",
    "verify_media_file",
    "process_media_list",
]

# =========================================================
#          G L O B A L S   A N D   H E L P E R S
# =========================================================
_MAX_MEDIA_SIZE_: int = 25  # Max file seize 25MB
_MAX_MEDIA_: int = 10

log = logging.getLogger()
pp = pprint.PrettyPrinter(indent=4)


# =========================================================
#       C O M M O N   U T I L I T Y    C L A S S E S
# =========================================================
class Media(AttributeProcessor):
    """Processor class for 'media' lists.

    Attributes:
        inList:
            Single filename (string) or list with one or more filenames
        maxNum:
            Max number of filenames in list
    """

    def __init__(self, inList: Any, maxNum: int) -> None:
        super().__init__(
            keyword=const.KWD_MEDIA,
            required=const.ATTR_OPTIONAL,
        )
        self._data: List[str] = []
        self._minNum = 0  # attachments are optional
        self._maxNum = max(
            self._minNum, maxNum
        )  # 'max' num cannot be smaller than 'min'
        self._valid = True
        self.data = inList

    @property
    def data(self) -> List[str]:
        """Return 'data' property."""
        return self._data

    @data.setter
    def data(self, inList: Any) -> None:
        """Set 'data' property."""
        self._data = process_media_list(inList, self._maxNum)

    @property
    def minNum(self) -> int:
        """Return 'minNum' property."""
        return self._minNum

    @property
    def maxNum(self) -> int:
        """Return 'maxNum' property."""
        return self._maxNum

    @property
    def totNum(self) -> int:
        """Return 'totNum' property."""
        return len(self._data)

    @property
    def raw(self) -> List[str]:
        """Return raw value from 'data' property."""
        return self._data

    @property
    def clean(self) -> List[str]:
        """Return normalized value from 'data' property."""
        return self._data


# =========================================================
#       C O R E   C L A S S   D E F I N I T I O N S
# =========================================================
class Response:
    """Generic response class.

    This class provides a standard interface for responses from sending messages
    via various communication services.

    Attributes:
        status:
            Response status string. const.STATUS_SUCCESS or const.STATUS_SUCCESS
        provider:
            Provider name that returned that response. Correlates to :attr:'~notifiers.core.Provider.name'
        data:
            The notification data that was used for the notification
        response:
            The response object that was returned. Usually :class:'requests.Response'
        errors:
            Holds a list of errors if relevant

    Note:
        This class is inspired by the "Response" class in the "Notifiers" module
        by Or Carmi: https://github.com/liiight/notifiers
    """

    def __init__(
        self,
        status: str,
        provider: str,
        data: Any,
        response: Optional[reqResponse] = None,
        errors: Any = None,
    ):
        self.status = status
        self.provider = provider
        self.data = data
        self.response = response
        self.errors = errors

    def __repr__(self) -> str:
        return f"<Response,provider={self.provider.capitalize()},status={self.status}, errors={self.errors}>"  # noqa: B950

    def raise_on_errors(self) -> None:
        """Raise exception on error in request response.

        Raises:
             CommunicationsError: if request response has errors
        """
        if self.errors:
            raise CommunicationsError(
                provider=self.provider,
                data=self.data,
                errors=self.errors,
                response=self.response,
            )

    @property
    def isOK(self) -> bool:
        """Return 'true' (boolean) if no errors."""
        return self.errors is None


class Provider(ABC):
    """Base class for service providers.

    Attributes:
        serviceType:
            communication/service type (e.g. email,  SMS, etc.)
        serviceName:
            communication/service name (e.g. Mailgun, Twilio, etc.)
        configSection:
            name of section in config files (e.g. f451_mailgun, f451_twilio, etc.)
    """

    def __init__(
        self,
        serviceType: str,
        serviceName: str,
        configSection: str,
    ) -> None:
        self._srvtype = serviceType
        self._srvName = serviceName
        self._sctnName = configSection

    def __repr__(self) -> str:
        return f"<Provider, type={self._srvtype}, name={self._srvName}>"

    @property
    def serviceType(self) -> str:
        """Return 'serviceType' property."""
        return self._srvtype

    @property
    def serviceName(self) -> str:
        """Return 'serviceName' property."""
        return self._srvName

    @property
    def configSection(self) -> str:
        """Return 'configSection' property."""
        return self._sctnName

    def _make_response(
        self,
        data: Any = None,
        response: Optional[reqResponse] = None,
        errors: Any = None,
    ) -> Response:
        """Generate 'Response' object.

        Args:
            data:
                Data that was submitted during call to 'send_message()' (and similar) methods
            response:
               'requests.Response' class if available
            errors:
                List of errors if available

        Returns:
            'Response' object

        Note:
            This method is inspired by the "create_response" method in the "Notifiers" module
            by Or Carmi: https://github.com/liiight/notifiers
        """
        status = const.STATUS_FAILURE if errors else const.STATUS_SUCCESS
        return Response(
            status=status,
            provider=self._srvName,
            data=data,
            response=response,
            errors=errors,
        )

    @abstractmethod
    def send_message(self, msg: str, **kwargs: Any) -> Any:
        """Stub for 'send_message()' method."""
        pass


# =========================================================
#              U T I L I T Y   F U N C T I O N S
# =========================================================
def verify_file(fName: str, strict: bool) -> bool:
    """Verify that a file exists.

    This function will raise an exception if 'strict' is set to 'True'.

    Args:
        fName:
            Single filename (string).
        strict:
            If 'True' then exception is raised when file does not exist

    Returns:
        'True' if files exists. If file does not exist or filename is
        blank (and 'strict' is set to 'False') then we return 'False'.

    Raises:
        InvalidAttributeError: If file does not exist
    """
    if strict and (not Path(fName).exists() or not fName.strip()):
        log.error(f"File '{fName or '<blank>'}' does not exist.")
        raise InvalidAttributeError(f"File '{fName or '<blank>'}' does not exist.")

    return Path(fName).exists() if fName.strip() else False


def verify_media_file(fName: str, validFmts: List[str], strict: bool) -> bool:
    """Verify that an image file exists and has proper format.

    This function will raise an exception if 'strict' is set to 'True'.

    Args:
        fName:
            Single filename (string).
        validFmts:
            'list' of valid image formats (e.g. jpeg, png, etc.)
        strict:
            If 'True' then exception is raised when file does not exist

    Returns:
        'True' if files exists. If file does not exist or filename is
        blank (and 'strict' is set to 'False') then we return 'False'.

    Raises:
        InvalidAttributeError: If file does not exist
    """
    if strict and not (imghdr.what(fName) in validFmts and fName.strip()):
        log.error(f"File '{fName or '<blank>'}' is not a valid media file.")
        raise InvalidAttributeError(
            f"File '{fName or '<blank>'}'  is not a valid media file."
        )

    return Path(fName).exists() if fName.strip() else False


def process_media_list(
    inList: Any,
    maxNum: int = _MAX_MEDIA_,
    strict: bool = False,
) -> List[str]:
    """Process list of media files.

    'inList' can be a single string if it's only 1 attachment. Or it can
    be a list of one or more file names string.

    Args:
        inList:
            Single filename (string), or list of one or more file name strings.
        maxNum:
            Max number of media files
        strict:
            If 'True' then exception is raised when file does not exist, otherwise
            filename is simply skipped

    Returns:
        String with zero or more filenames
    """
    tmpList = (
        inList if isinstance(inList, list) else utils.convert_attrib_str_to_list(inList)
    )
    fileList = [item.strip() for item in tmpList if verify_file(item.strip(), strict)]

    return fileList[:maxNum]


def pretty_print_response_records(inData: Any) -> None:
    """Helper: Pretty print response records."""

    def _print_item(item: Any, printRule: bool = False) -> None:
        if printRule:
            rprint(Rule())

        rprint(type(item))
        rpp(item, expand_all=True)

    recList = inData if isinstance(inData, list) else [inData]

    for i, rec in enumerate(recList):
        if isinstance(rec, list):
            for ii, subRec in enumerate(rec):
                _print_item(subRec, i > 0 and ii > 0)

        else:
            _print_item(rec, i > 0)
