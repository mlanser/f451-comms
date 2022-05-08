"""Default (base) class for SMS providers in f451 Communications module.

This is a base class for SMS providers, and it holds some common methods
and attributes used across most/all SMS providers/services.
"""
import logging
import pprint
import re
from typing import Any
from typing import List

import f451_comms.constants as const
import f451_comms.utils as utils
from f451_comms.entity import dedupe_by_attribute
from f451_comms.entity import Entity
from f451_comms.exceptions import MissingAttributeError
from f451_comms.processor import AttributeProcessor
from f451_comms.providers.provider import Provider

# =========================================================
#          G L O B A L S   A N D   H E L P E R S
# =========================================================
_MAX_DEFAULT_RECIPIENTS_: int = 10  # Arbitrary limit that each SMS module can change

log = logging.getLogger()
pp = pprint.PrettyPrinter(indent=4)


# =========================================================
#          S M S   U T I L I T Y    C L A S S E S
# =========================================================
class ToPhone(AttributeProcessor):
    """Processor class for recipient ('to') phone number lists.

    Attributes:
        inList:
            Single phone number (string) or list with one or more phone numbers
        maxNum:
            Max number of phone numbers in list
        strict:
            If 'True' then exception is raised if phone number list is empty

    Raises:
        MissingAttributeError:
            If 'strict' mode and list of phone numbers is empty
    """

    def __init__(
        self,
        inList: Any,
        maxNum: int,
        strict: bool = True,
    ) -> None:
        super().__init__(
            keyword=const.KWD_TO_PHONE,
            required=const.ATTR_REQUIRED,
        )
        self._data: List[Entity] = []
        self._strict = strict
        self._minNum = 1  # we require min 1 SMS recipient
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
            log.error("Blank SMS 'to' phone number")
            self._data = []
            self._valid = False
            if self._strict:
                raise MissingAttributeError("'to' phone attribute cannot be blank.")
        else:
            self._data = tmpList
            self._valid = True

    @property
    def minNum(self) -> int:
        """Return 'data' property."""
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
        """Return 'clean' list of phone number strings."""
        return [item.phone for item in self._data]


# =========================================================
#    B A S E   S M S   C L A S S   D E F I N I T I O N
# =========================================================
class BaseSMS(Provider):
    """Base class for SMS providers.

    Attributes:
        serviceName:
            Name of SMS service (e.g. Twilio, etc.)
        configSection:
            Name of section in config files (e.g. f451_twilio, etc.)
    """

    def __init__(self, serviceName: str, configSection: str, **kwargs: Any) -> None:
        super().__init__(const.SRV_TYPE_SMS, serviceName, configSection)
        self._sender: Entity = Entity()
        self.defaultTo = kwargs.get(const.KWD_TO, kwargs.get(const.KWD_TO_PHONE, ""))
        self.sender = kwargs.get(const.KWD_FROM, kwargs.get(const.KWD_FROM_PHONE, ""))
        self.senderName = kwargs.get(const.KWD_FROM_NAME, "")

    @property
    def sender(self) -> Entity:
        """Return 'sender' property."""
        return self._sender

    @sender.setter
    def sender(self, val: Any) -> None:
        """Set 'maxNum' property."""
        if isinstance(val, Entity):
            self._sender = Entity(**val.to_dict())
        elif const.DELIM_VAL in val and const.DELIM_STD in val:
            self._sender = Entity(**utils.process_key_value_map(val))
        elif tmpList := utils.convert_attrib_str_to_list(val):
            self._sender = Entity(phone=tmpList[0])

    @property
    def senderPhone(self) -> str:
        """Return 'senderPhone' property."""
        return self._sender.phone

    @senderPhone.setter
    def senderPhone(self, val: Any) -> None:
        """Set 'senderPhone' property."""
        self._sender.phone = val

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
             Single phone number (string) or 'Entity' object, or list of
             one or more numbers or 'Entity' objects.
        maxNum:
            Max number of phone numbers

    Returns:
        List of 'Entity' objects
    """
    # Ensure we have proper lists of either phone number strings or 'Entity' objects
    if isinstance(inList, str):
        inList = utils.convert_attrib_str_to_list(inList)
    elif isinstance(inList, Entity):
        inList = [inList]

    if not isinstance(inList, list):
        return []

    # Ensure we work with unique records by converting 'list' to 'set' and
    # then convert list of phone numbers strings to list of 'Entity' objects
    tmpSet = set(inList)
    if all(isinstance(item, str) for item in tmpSet):
        outList = [
            re.sub("[^0-9+]", "", item)
            for item in tmpSet
            if utils.is_valid_phone(re.sub("[^0-9+]", "", item))
        ]
        return [Entity(phone=item) for item in set(outList)][:maxNum]

    # Ensure that all items in list of 'Entity' objects have a phone number
    elif all(isinstance(item, Entity) for item in inList):
        tmpList = dedupe_by_attribute(inList, "phone")
        return [item for item in tmpList if item.phone][:maxNum]

    return []
