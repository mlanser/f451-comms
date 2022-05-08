"""Slack class for f451 Communications module.

This module adds an abstraction layer to the Slack SDK and the main purpose is to provide
a standard interface for some core methods for sending Slack updates and files to
specific channels.

Note:
    - This module assumes that we have an active Slack developer account.
    - This module uses the Slack SDK to connect with the Slack service.

Todo:
    - Create ability to DM
"""
import logging
import pprint
from pathlib import PurePath
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from slack_sdk import WebClient  # type: ignore[attr-defined]
from slack_sdk.errors import SlackApiError

import f451_comms.constants as const
import f451_comms.providers.provider as provider
import f451_comms.utils as utils
from f451_comms.entity import Entity
from f451_comms.exceptions import CommunicationsError
from f451_comms.exceptions import MissingAttributeError

# =========================================================
#          G L O B A L S   A N D   H E L P E R S
# =========================================================
_SRV_CONFIG_SCTN_: str = "f451_slack"
_SRV_PROVIDER_: str = "Slack"

_MAX_MSG_LEN_: int = 320

_API_BASE_: str = "https://slack.com/api"
_API_POST_MSG_: str = "chat.postMessage"
_API_UPLOAD_FILE_: str = "files.upload"

_INVALID_BLOCK_: str = "Unable to render block"
_NO_TEXT_: str = "_NO_TEXT_"

log = logging.getLogger()
pp = pprint.PrettyPrinter(indent=4)


# =========================================================
#        M A I N   C L A S S   D E F I N I T I O N
# =========================================================
class Slack(provider.Provider):
    """Slack class for f451 Communications module.

    Use this support class to send messages via Slack SDK.

    Attributes:
        authToken:
            Slack auth token
        signingSecret:
            Slack signing secret -- reserved for future use
        appToken:
            Slack app token -- reserved for future use
    """

    def __init__(
        self,
        authToken: str,
        signingSecret: str = "",  # Reserved for future use
        appToken: str = "",  # Reserved for future use
        **kwargs: Any,
    ) -> None:
        super().__init__(const.SRV_TYPE_FORUMS, _SRV_PROVIDER_, _SRV_CONFIG_SCTN_)
        self._signingSecret: str = signingSecret
        self._appToken: str = appToken
        self._sender: Entity = Entity()
        self._client: Any = None
        self._defaultChannel: str = str(kwargs.get(const.KWD_TO_CHANNEL, ""))
        self._defaultIconEmoji: str = str(kwargs.get(const.KWD_ICON_EMOJI, ""))
        self.client = authToken
        self.sender = kwargs.get(const.KWD_FROM, kwargs.get(const.KWD_FROM_SLACK, ""))

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
            self._sender = Entity(slack=tmpList[0])

    @property
    def client(self) -> Any:
        """Return 'client' property."""
        return self._client

    @client.setter
    def client(self, authToken: str) -> None:
        """Set 'client' property."""
        try:
            log.debug("Connecting to Slack")
            self._client = WebClient(authToken)

        except SlackApiError as e:
            log.error("Unable to connect to Slack")
            raise CommunicationsError("Unable to connect to Slack") from e

    @property
    def signingSecret(self) -> str:
        """Return 'signingSecret' property."""
        return self._signingSecret

    @property
    def appToken(self) -> str:
        """Return 'appToken' property."""
        return self._appToken

    @property
    def channel(self) -> str:
        """Return 'channel' property."""
        return self._defaultChannel

    def _post_single_message(self, msgData: Dict[str, Any]) -> provider.Response:
        try:
            log.debug(
                f"Sending Slack message to '{msgData['channel'].strip()}' channel"
            )
            clientResponse = self._client.chat_postMessage(**msgData)
            log.info(f"Slack response code: {clientResponse}")
            response = self._make_response(msgData, None, None)

        except SlackApiError as e:
            log.info(f"Slack API error: {e}")
            response = self._make_response(msgData, None, e)

        return response

    def send_message(self, msg: str, **kwargs: Any) -> List[provider.Response]:
        """Post plain text Slack message to a channel.

        This method provides a standard interface for posting Slack messages
        to a given channel using the Slack SDK.

        Args:
            msg:
                simple/plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            'list' of 'Response' objects from Slack service API call. We always return a list
            even though we'll only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            MissingAttributeError: Message text is empty, or Slack channel name is empty/missing
        """
        if not msg.strip():
            log.error("Blank Slack message")
            raise MissingAttributeError("Slack message cannot be blank.")

        channel = kwargs.get(const.KWD_TO_CHANNEL, self._defaultChannel)
        if not channel.strip():
            log.error("Blank Slack channel")
            raise MissingAttributeError("Slack channel cannot be blank.")

        msgData = {
            "channel": channel,
            "text": msg,
            "username": self._sender.slack,
            "icon_emoji": process_icon_emoji(
                kwargs.get(const.KWD_ICON_EMOJI, self._defaultIconEmoji)
            ),
        }
        return [self._post_single_message(msgData)]

    def send_message_with_blocks(
        self, blocks: List[Dict[str, Any]], **kwargs: Any
    ) -> List[provider.Response]:
        """Post Slack message using blocks to a channel.

        This method provides a standard interface for posting Slack messages
        to a given channel using the Slack SDK.

        Args:
            blocks:
                'list' of Slack blocks as 'dicts'
            kwargs:
                Additional optional arguments

        Returns:
            'list' of 'Response' objects from Slack service API call. We always return a list
            even though we'll only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            MissingAttributeError: Message text is empty, or Slack channel name is empty/missing
        """
        if not blocks:
            log.error("Blank Slack blocks")
            raise MissingAttributeError("Slack message blocks cannot be blank.")

        channel = kwargs.get(const.KWD_TO_CHANNEL, self._defaultChannel)
        if not channel.strip():
            log.error("Blank Slack channel")
            raise MissingAttributeError("Slack channel cannot be blank.")

        msgData = {
            "channel": channel,
            "text": _NO_TEXT_,
            "blocks": blocks,
            "username": self._sender.slack,
            "icon_emoji": process_icon_emoji(
                kwargs.get(const.KWD_ICON_EMOJI, self._defaultIconEmoji)
            ),
        }

        return [self._post_single_message(msgData)]

    def send_message_with_file(
        self, msg: str, **kwargs: Any
    ) -> List[provider.Response]:
        """Post Slack message with file attachment to a channel.

        This method provides a standard interface for posting Slack messages
        with file attachments to a given channel using the Slack SDK.

        Note:
            Only 1 file attachment per message is allowed. If more than 1 file
            is included with the message, then only the 1st file is used.

        Args:
            msg:
                Simple/plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            'list' of 'Response' objects from Slack service API call. We always return
            a list even though we'll only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            MissingAttributeError: Message text is empty, or Slack channel name is empty/missing
        """
        if not msg.strip():
            log.error("Blank Slack message")
            raise MissingAttributeError("Slack message cannot be blank.")

        channel = kwargs.get(const.KWD_TO_CHANNEL, self._defaultChannel)
        if not channel.strip():
            log.error("Blank Slack channel")
            raise MissingAttributeError("Slack channel cannot be blank.")

        fName, fStream, fTitle = process_file_attachment(
            inFile=kwargs.get(const.KWD_ATTACHMENTS, ""),
            inTitle=kwargs.get(const.KWD_FILE_TITLE, ""),
            strict=True,
        )

        msgData = {
            "channel": channel,
            "text": _NO_TEXT_,
            "file": fStream,
            "filename": fName,
            "title": fTitle,
            "initial_comment": msg,
            "username": self._sender.slack,
            "icon_emoji": process_icon_emoji(
                kwargs.get(const.KWD_ICON_EMOJI, self._defaultIconEmoji)
            ),
        }

        return [self._post_single_message(msgData)]


# =========================================================
#              U T I L I T Y   F U N C T I O N S
# =========================================================
def process_file_attachment(
    inFile: Any,
    inTitle: str = "",
    strict: bool = False,
) -> Tuple[str, bytes, str]:
    """Process a file to be uploaded.

    'inList' can be a single string if it's only 1 attachment. Or it can
    be a list of one or more file names string.

    Note:
        We only allow 1 file to be uploaded at once. However, since
        the 'attachment' attribute can be used with multiple send
        functions (e.g. email, etc.), we need to handle situation where
        there potentially are more than 1 filename listed. In  the case
        where there are multiple filenames, we'll use the first valid
        filename in the list.

    Args:
        inFile:
            Single filename (string), or list of one or more file name strings.
        inTitle:
            Optional file title (string)
        strict:
            If 'True' then exception is raised when file does not exist, otherwise
            filename is simply skipped

    Returns:
        'Tuple[' with filename, file stream, and (optional) file title string
    """

    def _process(fName: str, fTitle: str = "") -> Tuple[str, Any, Any]:
        return PurePath(fName).name, open(fName, "rb").read(), fTitle.strip()

    tmpList = (
        inFile if isinstance(inFile, list) else utils.convert_attrib_str_to_list(inFile)
    )
    validList = [
        _process(item, inTitle)
        for item in tmpList
        if provider.verify_file(item.strip(), strict)
    ]

    return validList[0] if len(validList) else ("", b"", "")


def process_icon_emoji(inIconEmoji: str) -> str:
    """Process an 'icon_emoji' string.

    Args:
        inIconEmoji:
            Single icon emoji string.

    Returns:
        Properly formatted 'icon_emoji' string
    """
    tmpStr = inIconEmoji.strip(": ")

    return f":{tmpStr}:" if tmpStr else ""
