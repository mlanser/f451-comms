"""Mailgun (email) class for f451 Communications module.

This module adds an abstraction layer for the Mailgun email services and the main
purpose is to provide a standard interface for some core methods for sending
emails (with or without attachments) to one or more recipients.

Note:
    - This module assumes that we have an active Mailgun developer account.
    - This module uses the Python 'requests' module to connect with the Mailgun service.
"""
import json
import logging
import pprint
from typing import Any
from typing import Dict
from typing import List

import requests

import f451_comms.constants as const
import f451_comms.utils as utils
from f451_comms.exceptions import MissingAttributeError
from f451_comms.processor import AttributeProcessor
from f451_comms.providers.email import Attachments
from f451_comms.providers.email import BaseEmail
from f451_comms.providers.email import CcEmail
from f451_comms.providers.email import ToEmail
from f451_comms.providers.provider import Response

# =========================================================
#          G L O B A L S   A N D   H E L P E R S
# =========================================================
_SRV_CONFIG_SCTN_: str = "f451_mailgun"
_SRV_PROVIDER_: str = "Mailgun"

_MIN_TAG_LEN_: int = 3
_MAX_TAG_LEN_: int = 128
_MAX_TAG_NUM_: int = 3
_MAX_RECIPIENTS_: int = 1000
_MAX_EMAIL_SIZE_: int = 25  # Max size of email incl attachments in mb

_MAX_MEDIA_: int = 10
_MAX_MEDIA_SIZE_: int = 25  # Max file seize 25MB

_METHOD_API_: str = "api"
_METHOD_SMTP_: str = "smtp"

_API_BASE_: str = "https://api.mailgun.net/v3"
_API_END_POINT_: str = "messages"

log = logging.getLogger()
pp = pprint.PrettyPrinter(indent=4)


# =========================================================
#      M A I L G U N   U T I L I T Y    C L A S S E S
# =========================================================
class Tags(AttributeProcessor):
    """Processor class for email tags.

    Attributes:
        inList:
            Single tag (string) or list with one or more tags
        maxNum:
            Max number of tags in list
        minLen:
            Min length of any tag in list
        maxLen:
            Max length of any tag in list
    """

    def __init__(self, inList: Any, maxNum: int, minLen: int, maxLen: int) -> None:
        super().__init__(
            keyword=const.KWD_TAGS,
            required=const.ATTR_OPTIONAL,
        )
        self._data: List[str] = []
        self._valid: bool = True
        self._minNum: int = 0  # 'tag' list is optional
        self.maxNum = maxNum
        self.minLen = minLen
        self.maxLen = maxLen
        self.data = inList

    @property
    def data(self) -> List[str]:
        """Return 'data' property."""
        return self._data

    @data.setter
    def data(self, inList: Any) -> None:
        """Set 'data' property."""
        self._data = process_tag_list(inList, self._maxNum, self._minLen, self._maxLen)

    @property
    def minNum(self) -> int:
        """Return 'minNum' property."""
        return self._minNum

    @property
    def maxNum(self) -> int:
        """Return 'maxNum' property."""
        return self._maxNum

    @maxNum.setter
    def maxNum(self, val: int) -> None:
        """Set 'maxNum' property."""
        # 'max' num cannot be smaller than 'min'
        self._maxNum = max(self._minNum, val, _MAX_TAG_NUM_)

    @property
    def minLen(self) -> int:
        """Return 'minLen' property."""
        return self._minLen

    @minLen.setter
    def minLen(self, val: int) -> None:
        """Set 'minLen' property."""
        # tags must have a min length
        self._minLen = max(_MIN_TAG_LEN_, val)

    @property
    def maxLen(self) -> int:
        """Return 'maxLen' property."""
        return self._maxLen

    @maxLen.setter
    def maxLen(self, val: int) -> None:
        """Set 'maxLen' property."""
        # tags must have a max length
        self._maxLen = min(_MAX_TAG_LEN_, val)

    @property
    def totNum(self) -> int:
        """Return 'totNum' property."""
        return len(self._data)

    @property
    def raw(self) -> List[str]:
        """Return 'raw' data property."""
        return self._data

    @property
    def clean(self) -> List[str]:
        """Return 'clean' data property.

        Note: tag data does not get normalized.
        """
        return self._data


class RecipientData(AttributeProcessor):
    """Processor class for email tags.

    Attributes:
        inData:
            'dict' with one or more recipient data 'dict' records
        maxNum:
            Max number of recipient data records in list
    """

    def __init__(self, inData: Any, maxNum: int) -> None:
        super().__init__(
            keyword=const.KWD_RECIPIENT_DATA,
            required=const.ATTR_OPTIONAL,
        )
        self._data: Dict[str, Any] = {}
        self._valid: bool = True
        self._minNum: int = 0  # 'recipient_data' list is optional
        self.maxNum: int = maxNum
        self.data = inData

    @property
    def data(self) -> Dict[str, Any]:
        """Return 'data' property."""
        return self._data

    @data.setter
    def data(self, inData: Any) -> None:
        """Set 'data' property."""
        self._data = dict(list(inData.items())[: self._maxNum])

    @property
    def minNum(self) -> int:
        """Return 'minNum' property."""
        return self._minNum

    @property
    def maxNum(self) -> int:
        """Return 'maxNum' property."""
        return self._maxNum

    @maxNum.setter
    def maxNum(self, val: int) -> None:
        """Set 'maxNum' property."""
        # 'max' num cannot be smaller than 'min'
        self._maxNum = max(self._minNum, val)

    @property
    def totNum(self) -> int:
        """Return 'totNum' property."""
        return len(self._data)

    @property
    def raw(self) -> Dict[str, Any]:
        """Return 'raw' data."""
        return self._data

    @property
    def clean(self) -> str:
        """Return 'data' property in JSON format."""
        return json.dumps(self._data)


# =========================================================
#        M A I N   C L A S S   D E F I N I T I O N
# =========================================================
class Mailgun(BaseEmail):
    """Email class for f451 Communications module.

    Use this support class to send email via Mailgun service.

    Attributes:
        apiKey:
            Mailgun API key
        fromDomain:
            Mailgun domain
    """

    def __init__(
        self,
        apiKey: str,
        fromDomain: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(_SRV_PROVIDER_, _SRV_CONFIG_SCTN_, **kwargs)
        self._apiKey: str = apiKey
        self._fromDomain: str = fromDomain
        self._tracking: bool = utils.convert_str_to_bool(
            kwargs.get(const.KWD_TRACKING, False)
        )
        self._testmode: bool = utils.convert_str_to_bool(
            kwargs.get(const.KWD_TESTMODE, False)
        )

    @property
    def settings(self) -> Dict[str, Any]:
        """Return 'settings' property."""
        return {
            "senderName": self.senderName,
            "senderEmail": self.senderEmail,
            "defaultTo": self.defaultTo,
            "defaultTags": self.defaultTags,
            "defaultSubject": self.defaultSubject,
        }

    def _make_sender_string(self) -> str:
        """Create mailgun 'sender' string."""
        return (
            f"{self._sender.name} <mailgun@{self._fromDomain}>"
            if self._sender.name
            else f"<mailgun@{self._fromDomain}>"
        )

    def _assemble_msg_data(self, msg: str, **kwargs: Any) -> Dict[str, Any]:
        """Create message data record.

        This data record is posted to the Mailgun API. It can get rather large as it
        designed to hold all data required to construct the email.

        Args:
            msg:
                Plain version form of email message
            kwargs:
                Additional optional arguments

        Returns:
            'dict' with email data

        Raises:
            MissingAttributeError: Email message or subject line is missing
        """
        subject = kwargs.get(const.KWD_SUBJECT, self._defaultSubject)
        if not msg.strip() or not subject.strip():
            log.error("Blank email message and/or subject")
            raise MissingAttributeError(
                "Email message or subject line cannot be blank."
            )

        toList = ToEmail(
            inList=kwargs.get(const.KWD_TO_EMAIL, self._defaultTo),
            maxNum=_MAX_RECIPIENTS_,
        )
        ccList = CcEmail(
            inList=kwargs.get(const.KWD_CC_EMAIL, []),
            maxNum=min(_MAX_RECIPIENTS_ - len(toList.raw), _MAX_RECIPIENTS_),
        )
        bccList = CcEmail(
            inList=kwargs.get(const.KWD_BCC_EMAIL, []),
            maxNum=min(
                _MAX_RECIPIENTS_ - len(toList.raw) - len(ccList.raw), _MAX_RECIPIENTS_
            ),
        )
        tags = Tags(
            inList=kwargs.get(const.KWD_TAGS, self._defaultTags),
            maxNum=_MAX_TAG_NUM_,
            minLen=_MIN_TAG_LEN_,
            maxLen=_MAX_TAG_LEN_,
        )
        recipientData = RecipientData(
            inData=kwargs.get(const.KWD_RECIPIENT_DATA, {}), maxNum=_MAX_RECIPIENTS_
        )

        return {
            "from": self._make_sender_string(),
            "to": toList.clean,
            "cc": ccList.clean,
            "bcc": bccList.clean,
            "subject": subject.strip(),
            "text": msg.strip(),
            "html": (kwargs.get(const.KWD_HTML, "")).strip(),
            "recipient-variables": recipientData.clean,
            "o:tag": tags.clean,
            "o:tracking": kwargs.get(const.KWD_TRACKING, self._tracking),
            "o:testmode": kwargs.get(const.KWD_TESTMODE, False),
        }

    def send_message(self, msg: str, **kwargs: Any) -> List[Response]:
        """Send email to one or more recipients.

        Note that the 'text' version of the message is included in the 'msg' param
        to ensure API consistency with our communications modules/components.

        Args:
            msg:
                Plain text version of email message
            kwargs:
                Additional optional arguments

        Returns:
            'list' of 'Response' objects from Mailgun service API call. We always return
            a list even though we'll only have a single item. This allows us to be consistent
            across all 'send_message()' functions.
        """
        msgData = self._assemble_msg_data(msg, **kwargs)

        attachments = Attachments(
            inList=kwargs.get(const.KWD_ATTACHMENTS, []),
            inType=const.KWD_ATTACHMENTS,
            maxNum=_MAX_MEDIA_,
        )
        inline = Attachments(
            inList=kwargs.get(const.KWD_ATTACHMENTS, []),
            inType=const.KWD_INLINE,
            maxNum=_MAX_MEDIA_,
        )

        reqResp = None
        reqErrors = []
        try:
            log.debug(f"Sending message via Mailgun to {msgData['to']}")
            reqResp = requests.post(
                url=f"{_API_BASE_}/{self._fromDomain}/{_API_END_POINT_}",
                auth=("api", self._apiKey),
                data=msgData,
                files=(attachments.clean + inline.clean),  # type: ignore[arg-type]
            )
            reqResp.raise_for_status()

        except requests.exceptions.HTTPError as errHttp:
            reqErrors.append(repr(errHttp))
        except requests.exceptions.Timeout as errTime:
            reqErrors.append(repr(errTime))
        except requests.exceptions.TooManyRedirects as errRedir:
            reqErrors.append(repr(errRedir))
        except requests.exceptions.RequestException as errReq:
            reqErrors.append(repr(errReq))

        response = self._make_response(msgData, reqResp, reqErrors)
        log.info(f"Mailgun response code: {response}")

        if not kwargs.get(const.KWD_SUPPRESS_ERROR, False):
            response.raise_on_errors()

        return [response]


# =========================================================
#              U T I L I T Y   F U N C T I O N S
# =========================================================
def process_tag_list(
    inList: Any,
    maxNum: int,
    minTagLen: int,
    maxTagLen: int,
) -> List[str]:
    """Process tag list and ensure that there are max N items.

    Args:
        inList:
            Single tag (string) or list with one or more tags
        maxNum:
            Max number of tags in list
        minTagLen:
            Min length of any tag in list
        maxTagLen:
            Max length of any tag in list

    Returns:
        List with zero or more tag strings
    """

    def _process(inTag: str, maxLen: int) -> str:
        asciiTag = str(inTag.encode(encoding="ascii", errors="replace"), "ascii")
        return asciiTag[:maxLen]

    tmpList = (
        inList if isinstance(inList, list) else utils.convert_attrib_str_to_list(inList)
    )
    tagList = [
        _process(item.strip(), maxTagLen)
        for item in tmpList
        if item.strip() and len(item.strip()) >= minTagLen
    ]

    return tagList[:maxNum]
