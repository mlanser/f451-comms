"""f451 Communications module.

This module acts as a common interface to several communications modules and its
main purpose is to make it easy to send messages to several communications channels
at the same.

An application can send a message via email, Twitter, Slack, and Twilio (SMS) using
the ``send_message()`` method. It is also possible to send messages via a specific
channel using the ``send_message_via_<channel>()`` methods.

Note:
    * Store secrets (e.g. API keys, etc.) in a separate configuration file.
    * Store defaults (e.g. default channels and recipients, etc.) in a separate configuration file.
    * Use ``.ini`` files that can be parsed by the Python ConfigParser (see example files)
"""
import logging
import pprint
from configparser import ConfigParser
from typing import Any
from typing import Dict
from typing import List
from typing import Union

import f451_comms.constants as const
import f451_comms.providers.provider as provider
import f451_comms.utils as utils
from f451_comms.exceptions import InvalidProviderError
from f451_comms.providers.mailgun import Mailgun
from f451_comms.providers.slack import Slack
from f451_comms.providers.twilio import Twilio
from f451_comms.providers.twitter import Twitter

# =========================================================
#          G L O B A L S   A N D   H E L P E R S
# =========================================================
_SRV_PROVIDER_: str = "Main"
_SRV_CONFIG_SCTN_: str = "f451_main"

log = logging.getLogger()
pp = pprint.PrettyPrinter(indent=4)

typeDefProvider = Union[Mailgun, Slack, Twilio, Twitter, None]
typeDefStringLists = Union[str, List[str], None]
typeDefChannelInfo = Union[
    ConfigParser, Dict[str, str], Dict[str, Any], List[str], None
]
typeDefSendMsgResponse = Union[List[provider.Response], Any]


# =========================================================
#        M A I N   C L A S S   D E F I N I T I O N
# =========================================================
class Comms(provider.Provider):
    """Main class for f451 Communications module.

    Use this main class as default interface to send messages to any of the
    installed/enabled communications channels.

    All available channels and associated attributes (e.g. API keys, etc.) are
    defined during initialization of the class.

    Attributes:
        config:
            set of attributes for 'secrets' such as API keys, general
            attributes, and default settings
    """

    def __init__(self, config: Any = None) -> None:
        super().__init__(const.SRV_TYPE_MAIN, _SRV_PROVIDER_, _SRV_CONFIG_SCTN_)

        settings = utils.process_config(config, False)

        self.default_channels = settings
        self.channel_map = settings
        self.channels = settings

    @property
    def channels(self) -> typeDefChannelInfo:
        """Return 'channels' property."""
        return self._channels

    @channels.setter
    def channels(self, settings: ConfigParser) -> None:
        """Set 'channels' property."""
        self._channels = {
            const.CHANNEL_MAILGUN: self._init_mailgun(settings),
            const.CHANNEL_SLACK: self._init_slack(settings),
            const.CHANNEL_TWILIO: self._init_twilio(settings),
            const.CHANNEL_TWITTER: self._init_twitter(settings),
        }

    @property
    def Mailgun(self) -> typeDefProvider:
        """Return 'Mailgun' client."""
        return self._channels[const.CHANNEL_MAILGUN]

    @property
    def Twilio(self) -> typeDefProvider:
        """Return 'Twilio' client."""
        return self._channels[const.CHANNEL_TWILIO]

    @property
    def Slack(self) -> typeDefProvider:
        """Return 'Slack' client."""
        return self._channels[const.CHANNEL_SLACK]

    @property
    def Twitter(self) -> typeDefProvider:
        """Return 'Twitter' client."""
        return self._channels[const.CHANNEL_TWITTER]

    @property
    def valid_channels(self) -> List[str]:
        """Return 'senderName' property."""
        return list(self._channels.keys())

    @property
    def channel_map(self) -> typeDefChannelInfo:
        """Return 'channel_map' property."""
        return self._channel_map

    @channel_map.setter
    def channel_map(self, settings: ConfigParser) -> None:
        """Set 'channel_map' property."""
        self._channel_map = utils.process_key_value_map(
            settings.get(const.CHANNEL_MAIN, const.KWD_CHANNEL_MAP, fallback="")
        )

    def is_valid_channel(self, inChannels: typeDefStringLists) -> bool:
        """Check if communications channel is valid."""
        tmpList = self._normalize_channel_list(inChannels)
        return (
            all(self._verify_channel(ch, True) for ch in tmpList) if tmpList else False
        )

    def is_enabled_channel(self, inChannels: typeDefStringLists) -> bool:
        """Check if communications channel is enabled."""
        tmpList = self._normalize_channel_list(inChannels)
        return (
            all(ch in self._channels and self._channels[ch] for ch in tmpList)
            if tmpList
            else False
        )

    @property
    def default_channels(self) -> typeDefChannelInfo:
        """Return 'default_channels' property."""
        return self._default_channels

    @default_channels.setter
    def default_channels(self, settings: ConfigParser) -> None:
        """Set 'default_channels' property."""
        self._default_channels = str(
            settings.get(const.CHANNEL_MAIN, const.KWD_CHANNELS, fallback="")
        ).split(const.DELIM_STD)

    def _verify_channel(self, chName: str, force: bool) -> bool:
        return (
            (chName != "" and (chName in self._channels or chName in self._channel_map))
            if force
            else (chName != "")
        )

    @staticmethod
    def _normalize_channel_list(inChannels: typeDefStringLists) -> List[str]:
        if inChannels:
            if isinstance(inChannels, str):
                return inChannels.split(const.DELIM_STD)
            elif all(isinstance(ch, str) for ch in inChannels):
                return inChannels

        return []

    @staticmethod
    def _init_mailgun(settings: ConfigParser) -> typeDefProvider:
        """Initialize Mailgun client."""
        if not settings.has_section(const.CHANNEL_MAILGUN):
            return None

        fromName = settings.get(
            const.CHANNEL_MAIN,
            const.KWD_FROM,
            fallback=settings.get(
                const.CHANNEL_MAILGUN, const.KWD_FROM_NAME, fallback=""
            ),
        )

        defaultTo = settings.get(
            const.CHANNEL_MAIN,
            const.KWD_TO,
            fallback=settings.get(
                const.CHANNEL_MAILGUN, const.KWD_TO_EMAIL, fallback=""
            ),
        )

        return Mailgun(
            apiKey=settings.get(const.CHANNEL_MAILGUN, const.KWD_PRIV_KEY, fallback=""),
            fromDomain=settings.get(
                const.CHANNEL_MAILGUN, const.KWD_FROM_DOMAIN, fallback=""
            ),
            from_name=fromName,
            to_email=defaultTo,
            subject=settings.get(const.CHANNEL_MAILGUN, const.KWD_SUBJECT, fallback=""),
            tags=settings.get(const.CHANNEL_MAILGUN, const.KWD_TAGS, fallback=""),
            tracking=settings.get(
                const.CHANNEL_MAILGUN, const.KWD_TRACKING, fallback=""
            ),
            testmode=settings.get(
                const.CHANNEL_MAILGUN, const.KWD_TESTMODE, fallback=""
            ),
        )

    @staticmethod
    def _init_slack(settings: ConfigParser) -> typeDefProvider:
        """Initialize Slack client."""
        if not settings.has_section(const.CHANNEL_SLACK):
            return None

        fromSlack = settings.get(
            const.CHANNEL_MAIN,
            const.KWD_FROM,
            fallback=settings.get(
                const.CHANNEL_SLACK, const.KWD_FROM_SLACK, fallback=""
            ),
        )

        defaultChannel = settings.get(
            const.CHANNEL_SLACK, const.KWD_TO_CHANNEL, fallback=""
        )

        return Slack(
            authToken=settings.get(
                const.CHANNEL_SLACK, const.KWD_AUTH_TOKEN, fallback=""
            ),
            signingSecret=settings.get(
                const.CHANNEL_SLACK, const.KWD_SIGN_SECRET, fallback=""
            ),
            appToken=settings.get(
                const.CHANNEL_SLACK, const.KWD_APP_TOKEN, fallback=""
            ),
            to_channel=defaultChannel,
            from_slack=fromSlack,
            icon_emoji=settings.get(
                const.CHANNEL_SLACK, const.KWD_ICON_EMOJI, fallback=""
            ),
        )

    @staticmethod
    def _init_twilio(settings: ConfigParser) -> typeDefProvider:
        """Initialize Twilio client."""
        if not settings.has_section(const.CHANNEL_TWILIO):
            return None

        fromPhone = settings.get(
            const.CHANNEL_MAIN,
            const.KWD_FROM,
            fallback=settings.get(
                const.CHANNEL_TWILIO, const.KWD_FROM_PHONE, fallback=""
            ),
        )

        defaultTo = settings.get(
            const.CHANNEL_MAIN,
            const.KWD_TO,
            fallback=settings.get(
                const.CHANNEL_TWILIO, const.KWD_TO_PHONE, fallback=""
            ),
        )

        return Twilio(
            acctSID=settings.get(const.CHANNEL_TWILIO, const.KWD_ACCT_SID, fallback=""),
            authToken=settings.get(
                const.CHANNEL_TWILIO, const.KWD_AUTH_TOKEN, fallback=""
            ),
            from_phone=fromPhone,
            to_phone=defaultTo,
        )

    @staticmethod
    def _init_twitter(settings: ConfigParser) -> typeDefProvider:
        """Initialize Twitter client."""
        if not settings.has_section(const.CHANNEL_TWITTER):
            return None

        defaultTo = settings.get(
            const.CHANNEL_MAIN,
            const.KWD_TO,
            fallback=settings.get(
                const.CHANNEL_TWITTER, const.KWD_TO_TWITTER, fallback=""
            ),
        )

        return Twitter(
            usrKey=settings.get(const.CHANNEL_TWITTER, const.KWD_USER_KEY, fallback=""),
            usrSecret=settings.get(
                const.CHANNEL_TWITTER, const.KWD_USER_SECRET, fallback=""
            ),
            authToken=settings.get(
                const.CHANNEL_TWITTER, const.KWD_AUTH_TOKEN, fallback=""
            ),
            authSecret=settings.get(
                const.CHANNEL_TWITTER, const.KWD_AUTH_SECRET, fallback=""
            ),
            to_twitter=defaultTo,
            tags=settings.get(const.CHANNEL_TWITTER, const.KWD_TAGS, fallback=""),
        )

    def process_channel_list(
        self, inList: typeDefStringLists, strict: bool = False
    ) -> List[str]:
        """Process list of channel names and convert them to list of strings.

        The purpose of this method is to process a list with one or more channel
        names and placing them into a list.

        Args:
            inList:
                Single string or list with one or more strings
            strict:
                If 'True' then include only valid and enabled channel names

        Returns:
            String with zero or more channel names
        """
        tmpList = (
            inList
            if isinstance(inList, list)
            else utils.convert_attrib_str_to_list(inList)
        )

        return [
            ch
            for ch in [
                self._channel_map[item] if item in self._channel_map else item
                for item in [
                    tmp.strip()
                    for tmp in tmpList
                    if self._verify_channel(tmp.strip(), strict)
                ]
            ]
            if self.is_enabled_channel(ch)
        ]

    def send_message(self, msg: str, **kwargs: Any) -> typeDefSendMsgResponse:
        """Send message to one or more channels.

        This method sends a given message to one or more channels at
        the same time. The 'channels' keyword argument defines which
        communication channels to use.

        The keyword arguments can also include additional message data
        such as HTML for emails and Slack blocks.

        Args:
            msg:
                Simple/plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            List of 'response' records. We always return a list even though we
            may only have a single item. This allows us to be consistent across
            all 'send_message()' functions.

        Raises:
            InvalidProviderError: Channel/service provider is not valid/active
        """
        chList = kwargs.get(const.KWD_CHANNELS, self._default_channels)
        channels = self.process_channel_list(inList=chList, strict=True)

        if not channels:
            log.error(f"Invalid communication channel(s): {chList}")
            raise InvalidProviderError("Invalid communication channel(s)).")

        return [
            self._channels[ch].send_message(msg, **kwargs)  # type: ignore[union-attr]
            for ch in channels
            if self._channels[ch]
        ]

    def send_message_via_mailgun(
        self, msg: str, **kwargs: Any
    ) -> typeDefSendMsgResponse:
        """Send email via Mailgun.

        This method sends a given message via email using the Mailgun service
        provider. The keyword arguments can also include additional message
        data such as an HTML version of the message.

        Args:
            msg:
                Simple/plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            List of 'response' records from email Mailgun service. We always return a list
            even though we may only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            InvalidProviderError: Mailgun service is not valid/active
        """
        if self._channels[const.CHANNEL_MAILGUN]:
            return self._channels[const.CHANNEL_MAILGUN].send_message(msg, **kwargs)  # type: ignore[union-attr]  # noqa: B950

        log.error(f"'{const.CHANNEL_MAILGUN}' is not a valid communication channel")
        raise InvalidProviderError(
            f"'{const.CHANNEL_MAILGUN}' is not a valid communication channel."
        )

    def send_message_via_slack(self, msg: Any, **kwargs: Any) -> typeDefSendMsgResponse:
        """Send message via Slack.

        This method sends a given message via Slack. The 'kwargs' arguments can
        also include additional message data such Slack blocks.

        Args:
            msg:
                simple/plain text version of message to be sent. The 'msg' argument
                can also be a 'list' of Slack blocks.
            kwargs:
                Additional optional arguments

        Returns:
            List of 'response' records from Slack. We always return a list
            even though we may only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            InvalidProviderError: Slack channel is not valid/active
        """
        if self._channels[const.CHANNEL_SLACK]:
            if isinstance(msg, list):
                return self._channels[const.CHANNEL_SLACK].send_message_with_blocks(  # type: ignore[union-attr]  # noqa: B950
                    msg, **kwargs
                )
            else:
                return self._channels[const.CHANNEL_SLACK].send_message(msg, **kwargs)  # type: ignore[union-attr]  # noqa: B950

        log.error(
            f"ERROR: '{const.CHANNEL_SLACK}' is not a valid communication channel"
        )
        raise InvalidProviderError(
            f"'{const.CHANNEL_SLACK}' is not a valid communication channel."
        )

    def send_message_via_twilio(
        self, msg: str, **kwargs: Any
    ) -> typeDefSendMsgResponse:
        """Send SMS via Twilio.

        This method sends a given message via SMS (using Twilio) to one or
        more recipients. The phone numbers of the recipients must be specified
        in the 'to_phone' keyword argument.

        Args:
            msg:
                Simple/plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            List of 'response' records from Twilio SMS service. We always return a list
            even though we may only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            InvalidProviderError: Twilio service is not valid/active
        """
        if self._channels[const.CHANNEL_TWILIO]:
            return self._channels[const.CHANNEL_TWILIO].send_message(msg, **kwargs)  # type: ignore[union-attr]  # noqa: B950

        log.error(f"'{const.CHANNEL_TWILIO}' is not a valid communication channel")
        raise InvalidProviderError(
            f"'{const.CHANNEL_TWILIO}' is not a valid communication channel."
        )

    def send_message_via_twitter(
        self, msg: str, **kwargs: Any
    ) -> typeDefSendMsgResponse:
        """Send message via Twitter.

        This method sends a given message via Twitter either as 'status update' or as
        DM to a specific recipient. If the latter, then the recipient must be specified
        in the 'kwargs' arguments.

        Args:
            msg:
                simple/plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            List of 'response' records from Twitter. We always return a list
            even though we may only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            InvalidProviderError: Twitter channel is not valid/active
        """
        if self._channels[const.CHANNEL_TWITTER]:
            return self._channels[const.CHANNEL_TWITTER].send_message(msg, **kwargs)  # type: ignore[union-attr]  # noqa: B950

        log.error(
            f"ERROR: '{const.CHANNEL_TWITTER}' is not a valid communication channel"
        )
        raise InvalidProviderError(
            f"'{const.CHANNEL_TWITTER}' is not a valid communication channel."
        )
