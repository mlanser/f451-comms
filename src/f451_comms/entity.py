"""'Entity' data class for f451 Communications module.

This data class is used to define entities (e.g. humans, systems, bots, Yetis, ghosts, etc.) that can
can send or receive communications.

Note:
    - Some regex strings below are based on examples found in this blog post:
      https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/

Todo:
    - Verify max length for Slack names.
    - Find correct regex for email
    - Find correct regex for phone
    - Find correct regex for twitter
"""
import pprint
import re
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List

import f451_comms.utils as utils

# =========================================================
#       G L O B A L S   A N D   D E S C R I P T O R S
# =========================================================
_MIN_LEN_PHONE_: int = 11  # 10 digits plus at lest 1 for single digit country code
_MAX_LEN_PHONE_: int = 15  # total max digits incl country code
_MAX_LEN_NAME_: int = 128
_MAX_LEN_SLACK_: int = 128
_MAX_LEN_TWITTER_: int = 15

pp = pprint.PrettyPrinter(indent=4)


# =========================================================
#                  M A I N   C L A S S
# =========================================================
class Entity:
    """Base class for represting users (senders and recipients).

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
        name: str = "",
        email: str = "",
        phone: str = "",
        slack: str = "",
        twitter: str = "",
    ):
        self.name = name
        self.email = email
        self.phone = phone
        self.slack = slack
        self.twitter = twitter

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False

        flag = False

        if self.email and other.email:
            flag |= self.email.lower() == other.email.lower()

        if self.phone and other.phone:
            flag |= self.phone.strip("+") == other.phone.strip("+")

        if self.twitter and other.twitter:
            flag |= self.twitter.strip("@").lower() == other.twitter.strip("@").lower()

        if self.twitter and other.twitter:
            flag |= self.twitter.strip("@").lower() == other.twitter.strip("@").lower()

        if self.slack and other.slack:
            flag |= self.slack.strip("@").lower() == other.slack.strip("@").lower()

        if self.name and other.name:
            flag |= self.name.lower() == other.name.lower()

        return flag

    def __repr__(self) -> str:
        return f"<Entity, val={self.email or self.phone or self.twitter or self.slack or self.name}>"

    def __hash__(self) -> int:
        return hash(self.__repr__())

    @property
    def name(self) -> str:
        """Return 'name' property."""
        return self._name

    @name.setter
    def name(self, val: str = "") -> None:
        """Set 'name' property."""
        clean = val.strip()
        if clean and len(clean) > _MAX_LEN_NAME_:
            raise ValueError(f"Name cannot exceed {_MAX_LEN_NAME_} chars.")

        self._name = clean.strip()

    @property
    def email(self) -> str:
        """Return 'email' property."""
        return self._email

    @email.setter
    def email(self, val: str = "") -> None:
        """Set 'email' property."""
        clean = val.strip()
        if clean and not utils.is_valid_email(clean):
            raise ValueError(f"Invalid email address: {clean}")
        self._email = clean

    @property
    def phone(self) -> str:
        """Return 'phone' property."""
        return self._phone

    @phone.setter
    def phone(self, val: str = "") -> None:
        """Set 'phone' property."""
        clean = re.sub("[^0-9+]", "", val)
        if clean and (
            (len(clean) < _MIN_LEN_PHONE_ or len(clean) > _MAX_LEN_PHONE_)
            or not utils.is_valid_phone(clean)
        ):
            raise ValueError(f"Invalid phone number: {clean}")
        self._phone = clean or ""

    @property
    def slack(self) -> str:
        """Return 'slack' property."""
        return self._slack

    @slack.setter
    def slack(self, val: str = "") -> None:
        """Set 'slack' property."""
        clean = val.strip("@ ")
        if clean and len(clean) > _MAX_LEN_SLACK_:
            raise ValueError(f"Name cannot exceed {_MAX_LEN_SLACK_} chars.")
        self._slack = clean

    @property
    def twitter(self) -> str:
        """Return 'twitter' property."""
        return self._twitter

    @twitter.setter
    def twitter(self, val: str = "") -> None:
        """Set 'twitter' property."""
        clean = val.strip("@ ")
        if clean and not utils.is_valid_twitter(clean):
            raise ValueError(f"Invalid Twitter username: {clean}")
        self._twitter = clean

    def to_dict(self) -> Dict[str, Any]:
        """Return properties as 'dict' structure."""
        return {
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "slack": self._slack,
            "twitter": self._twitter,
        }


# =========================================================
#              U T I L I T Y   F U N C T I O N S
# =========================================================
def dedupe_by_attribute(inList: List[Entity], key: str) -> Iterator[Entity]:
    """Dedupe list of objects by key.

    Theis function will search through a given list of objects and compare the value of
    the 'key' attribute. Only one object with a given key value is kept. If an object
    does not have the 'key' attribute or of that attribute is empty/none, then the
    object is excluded from the resulting list as well.

    Args:
        inList:
            list of objects to dedupe
        key:
            object attribute to be used as key value for filtering

    Yields:
        List item
    """
    clean = set()
    for item in inList:
        val = getattr(item, key, None)
        if val and val not in clean:
            clean.add(val)
            yield item


def process_entity_list_by_key(
    inList: Any, key: str, prefix: str = "", suffix: str = "", spacer: str = ""
) -> str:
    """Process specific key/attribute in list of 'Entity' objects."""
    if not inList:
        return ""

    if isinstance(inList, Entity):
        inList = [inList]

    return utils.process_string_list(
        [getattr(item, key) for item in inList if hasattr(item, key)],
        prefix,
        suffix,
        spacer,
    )
