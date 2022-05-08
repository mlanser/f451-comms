"""Default (base) class for email providers in f451 Communications module.

This is a base class for email providers, and it holds some common methods
and attributes used across most/all email providers/services.
"""
import logging
from pathlib import PurePath
from typing import Any
from typing import List
from typing import Tuple

import f451_comms.constants as const
import f451_comms.utils as utils
from f451_comms.entity import dedupe_by_attribute
from f451_comms.entity import Entity
from f451_comms.exceptions import InvalidAttributeError
from f451_comms.exceptions import MissingAttributeError
from f451_comms.processor import AttributeProcessor
from f451_comms.providers.provider import Provider
from f451_comms.providers.provider import verify_file

# =========================================================
#          G L O B A L S   A N D   H E L P E R S
# =========================================================
_MAX_MEDIA_SIZE_: int = 25  # Max file seize 25MB
_MAX_MEDIA_: int = 10
_MAX_DEFAULT_RECIPIENTS_: int = 100  # Arbitrary limit that each email module can change

log = logging.getLogger()


# =========================================================
#        E M A I L   U T I L I T Y    C L A S S E S
# =========================================================
class ToEmail(AttributeProcessor):
    """Processor class for email 'to' address lists.

    Attributes:
        inList:
            Single email address (string) or list with one or more email addresses
        maxNum:
            Max number of email addresses in list
        strict:
            If 'True' then exception is raised if email address list is empty

    Raises:
        MissingAttributeError: 'strict' mode and list of email addresses is empty
    """

    def __init__(
        self,
        inList: Any,
        maxNum: int,
        strict: bool = True,
    ) -> None:
        super().__init__(
            keyword=const.KWD_TO_EMAIL,
            required=const.ATTR_REQUIRED,
        )
        self._data: List[Entity] = []
        self._strict = strict
        self._minNum = 1  # we require min 1 email recipient
        self.maxNum = maxNum
        self.data = inList

    @property
    def data(self) -> List[Entity]:
        """Return 'data' property."""
        return self._data

    @data.setter
    def data(self, inList: Any) -> None:
        """Set 'data' property."""
        tmpList = process_recipient_list(inList, self._maxNum)

        if len(tmpList) < self._minNum:
            log.error("'to' attribute cannot be blank")
            self._data = []
            self._valid = False
            if self._strict:
                raise MissingAttributeError("'to' attribute cannot be blank.")
        else:
            self._data = tmpList
            self._valid = True

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
    def raw(self) -> List[Entity]:
        """Return 'raw' list of 'Entity' objects."""
        return self._data

    @property
    def clean(self) -> List[str]:
        """Return 'clean' list of email address strings."""
        return [item.email for item in self._data]


class CcEmail(AttributeProcessor):
    """Processor class for email 'cc' address lists.

    Attributes:
        inList:
            Single email address (string) or list with one or more email addresses
        maxNum:
            Max number of email addresses in list
        keyword:
            Attribute keyword string
    """

    def __init__(
        self,
        inList: Any,
        maxNum: int,
        keyword: str = const.KWD_CC_EMAIL,
    ) -> None:
        super().__init__(
            keyword=keyword,
            required=const.ATTR_OPTIONAL,
        )
        self._data: List[Entity] = []
        self._valid = True
        self._minNum = 0  # 'cc' list is optional
        self._maxNum = maxNum
        self.data = inList

    @property
    def data(self) -> List[Entity]:
        """Return 'data' property."""
        return self._data

    @data.setter
    def data(self, inList: Any) -> None:
        """Set 'data' property."""
        self._data = process_recipient_list(inList, self._maxNum)

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
    def raw(self) -> List[Entity]:
        """Return 'raw' list of 'Entity' objects."""
        return self._data

    @property
    def clean(self) -> List[str]:
        """Return 'clean' list of email address strings."""
        return [item.email for item in self._data]


class Attachments(AttributeProcessor):
    """Processor class for email 'attachments' lists.

    Attributes:
        inList:
            Single filename (string) or list with one or more filenames
        inType:
            Type of email attachment (i.e. 'attachments' or 'inline')
        maxNum:
            Max number of filenames in list
    """

    def __init__(
        self,
        inList: Any,
        inType: str,
        maxNum: int,
    ) -> None:
        super().__init__(
            keyword=inType,
            required=const.ATTR_OPTIONAL,
        )
        self._data: List[Tuple[str, Tuple[str, bytes]]] = []
        self._valid = True
        self._inType = inType
        self._minNum = 0  # attachments are optional
        self.maxNum = maxNum
        self.data = inList

    @property
    def data(self) -> List[Tuple[str, Tuple[str, bytes]]]:
        """Return 'data' property."""
        return self._data

    @data.setter
    def data(self, inList: Any) -> None:
        """Set 'data' property."""
        self._data = process_attachment_list(inList, self._inType, self._maxNum)

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
    def raw(self) -> List[Tuple[str, Tuple[str, bytes]]]:
        """Return 'raw' list of file attachments."""
        return self._data

    @property
    def clean(self) -> List[Tuple[str, Tuple[str, bytes]]]:
        """Return 'clean' list of file attachments.

        Note: no processing is done. But we keep this method for consistency.
        """
        return self._data


# =========================================================
#   B A S E   E M A I L   C L A S S   D E F I N I T I O N
# =========================================================
class BaseEmail(Provider):
    """Base class for email providers.

    Attributes:
        serviceName:
            Name of email service (e.g. Mailgun, etc.)
        configSection:
            Name of section in config files (e.g. f451_mailgun, etc.)
    """

    def __init__(self, serviceName: str, configSection: str, **kwargs: Any) -> None:
        super().__init__(const.SRV_TYPE_EMAIL, serviceName, configSection)
        self._sender: Entity = Entity()
        self._defaultSubject: str = str(kwargs.get(const.KWD_SUBJECT, ""))
        self.defaultTo = kwargs.get(const.KWD_TO, kwargs.get(const.KWD_TO_EMAIL, ""))
        self.defaultTags = kwargs.get(const.KWD_TAGS, "")
        self.sender = kwargs.get(const.KWD_FROM, kwargs.get(const.KWD_FROM_EMAIL, ""))
        self.senderName = kwargs.get(const.KWD_FROM_NAME, "")

    @property
    def sender(self) -> Entity:
        """Return 'sender' property."""
        return self._sender

    @sender.setter
    def sender(self, val: Any) -> None:
        """Set 'sender' property."""
        if isinstance(val, Entity):
            self._sender = val
        elif const.DELIM_VAL in val and const.DELIM_STD in val:
            self._sender = Entity(**utils.process_key_value_map(val))
        elif tmpList := utils.convert_attrib_str_to_list(val):
            self._sender = Entity(email=tmpList[0])

    @property
    def senderEmail(self) -> str:
        """Return 'senderEmail' property."""
        return self._sender.email

    @senderEmail.setter
    def senderEmail(self, val: Any) -> None:
        """Set 'senderEmail' property."""
        self._sender.email = val

    @property
    def senderName(self) -> str:
        """Return 'senderName' property."""
        return self._sender.name

    @senderName.setter
    def senderName(self, val: Any) -> None:
        """Set 'senderName' property."""
        self._sender.name = val

    @property
    def defaultTo(self) -> List[Entity]:
        """Return 'defaultTo' property."""
        return self._defaultTo

    @defaultTo.setter
    def defaultTo(self, val: Any) -> None:
        """Set 'defaultTo' property."""
        if isinstance(val, Entity):
            self._defaultTo = [val]
        elif const.DELIM_VAL in val and const.DELIM_STD in val:
            self._defaultTo = [Entity(**utils.process_key_value_map(val))]
        else:
            self._defaultTo = process_recipient_list(val, _MAX_DEFAULT_RECIPIENTS_)

    @property
    def defaultSubject(self) -> str:
        """Return 'defaultSubject' property."""
        return self._defaultSubject

    @property
    def defaultTags(self) -> List[str]:
        """Return 'defaultTags' property."""
        return self._defaultTags

    @defaultTags.setter
    def defaultTags(self, val: str) -> None:
        """Set 'defaultTags' property."""
        self._defaultTags = utils.convert_attrib_str_to_list(val)

    def send_message(self, msg: str, **kwargs: Any) -> Any:
        """Stub for 'send_message()' method."""
        pass


# =========================================================
#              U T I L I T Y   F U N C T I O N S
# =========================================================
def process_recipient_list(inList: Any, maxNum: int) -> List[Entity]:
    """Process list of recipients and return list of 'Entity' objects.

    Args:
        inList:
             Single email address (string) or 'Entity' object, or list of
             one or more email addresses or 'Entity' objects.
        maxNum:
            Max number of email addresses

    Returns:
        List of 'Entity' objects
    """
    # Ensure we have proper lists of either email address strings or 'Entity' objects
    if isinstance(inList, str):
        inList = utils.convert_attrib_str_to_list(inList)
    elif isinstance(inList, Entity):
        inList = [inList]

    if not isinstance(inList, list):
        return []

    # Ensure we work with unique records by converting 'list' to 'set' and
    # then convert list of email address strings to list of 'Entity' objects
    tmpSet = set(inList)
    if all(isinstance(item, str) for item in tmpSet):
        outList = [
            item.lower().strip()
            for item in tmpSet
            if utils.is_valid_email(item.strip())
        ]
        return [Entity(email=item) for item in outList][:maxNum]

    # Ensure that all items in list of 'Entity' objects have an email address
    elif all(isinstance(item, Entity) for item in inList):
        tmpList = dedupe_by_attribute(inList, "email")
        return [item for item in tmpList if item.email][:maxNum]

    return []


def process_attachment_list(
    inList: Any,
    inType: str = const.KWD_ATTACHMENTS,
    maxNum: int = _MAX_MEDIA_,
    strict: bool = False,
) -> List[Tuple[str, Tuple[str, bytes]]]:
    """Process a list of email attachments.

    'inList' can be a single string if it's only 1 attachment. Or it can
    be a list of one or more file names string.

    Args:
        inList:
            Single filename (string), or list of one or more file name strings.
        inType:
            File type label i.e. 'attachment' or 'inline'
        maxNum:
            Max number of files/attachments
        strict:
            If 'True' then exception is raised when file does not exist, otherwise
            filename is simply skipped

    Returns:
        List of tuples
    """

    def _process(
        fName: str, fType: str = const.KWD_ATTACHMENTS
    ) -> Tuple[str, Tuple[str, bytes]]:
        if fType not in [const.KWD_ATTACHMENTS, const.KWD_INLINE]:
            raise InvalidAttributeError(
                f"Attachment type must be '{const.KWD_ATTACHMENTS}' or '{const.KWD_INLINE}'."
            )

        return fType, (PurePath(fName).name, open(fName, "rb").read())

    tmpList = (
        inList if isinstance(inList, list) else utils.convert_attrib_str_to_list(inList)
    )
    fileList = [
        _process(item, inType) for item in tmpList if verify_file(item.strip(), strict)
    ]

    return fileList[:maxNum]
