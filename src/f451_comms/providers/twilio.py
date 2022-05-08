"""Twilio (SMS) class for f451 Communications module.

This module adds an abstraction layer to the Twilio Rest API client and the main
purpose is to provide a standard interface for some core methods for sending SMS
messages to specific recipients.

Note:
    - This module assumes that we have an active Twilio developer account.
    - This module uses the Twilio REST client.
"""
import logging
import pprint
from typing import Any
from typing import List
from typing import Tuple

from twilio.base.exceptions import TwilioRestException  # type: ignore[import]
from twilio.rest import Client

import f451_comms.constants as const
from f451_comms.exceptions import CommunicationsError
from f451_comms.exceptions import MissingAttributeError
from f451_comms.providers.provider import Media
from f451_comms.providers.provider import Response
from f451_comms.providers.sms import BaseSMS
from f451_comms.providers.sms import ToPhone

# =========================================================
#          G L O B A L S   A N D   H E L P E R S
# =========================================================
_SRV_CONFIG_SCTN_: str = "f451_twilio"
_SRV_PROVIDER_: str = "Twilio"

_MAX_RECIPIENTS_: int = 1000
_MAX_MSG_LEN_: int = 1600
_MAX_MEDIA_: int = 10
_MAX_MEDIA_SIZE_: int = 25  # Max file seize 25MB

_METHOD_API_: str = "api"
_METHOD_SMTP_: str = "smtp"

_API_BASE_: str = "https://api.twilio.com/2010-04-01/Accounts"
_API_END_POINT_: str = "Messages.json"

_STATUS_FAILED_: str = "failed"
_STATUS_UNDELIVERED_: str = "undelivered"

log = logging.getLogger()
pp = pprint.PrettyPrinter(indent=4)


# =========================================================
#        M A I N   C L A S S   D E F I N I T I O N
# =========================================================
class Twilio(BaseSMS):
    """Twilio SMS class for f451 Communications module.

    Use this support class to send SMS and voice messages via Twilio API. Please
    note that the default method is SMS. However, this can be changed with the
    'method' attribute in the 'defaults' dict.

    Attributes:
        acctSID:
            Twilio account SID
        authToken:
            Twilio auth token
        fromPhone:
            'from' phone number
    """

    def __init__(
        self,
        acctSID: str,
        authToken: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(_SRV_PROVIDER_, _SRV_CONFIG_SCTN_, **kwargs)
        self._acctSID: str = acctSID
        self._authToken: str = authToken
        self._client: Any = None
        self.client = (acctSID, authToken)

    @property
    def client(self) -> Any:
        """Return 'client' property."""
        return self._client

    @client.setter
    def client(self, auth: Tuple[str, str]) -> None:
        """Set 'client' property."""
        acctSID, authToken = auth
        try:
            log.debug("Connecting to Twilio")
            self._client = Client(acctSID, authToken)

        except TwilioRestException as e:
            log.error("Unable to connect to Twilio")
            raise CommunicationsError("Unable to connect to Twilio") from e

    def _send_single_message(
        self, toPhone: str, msg: str, media: List[str], suppress: bool
    ) -> Response:
        """Send single SMS.

        This helper method sends a single SMS and returns SID from Twilio.

        Args:
            toPhone:
                Recipient phone number
            msg:
                Message to be sent
            media:
                List of media attachments
            suppress:
                If 'False' then exception will be raised if request response returns errors

        Returns:
            Response from Twilio service API call

        Raises:
            CommunicationsError: 'suppress' is 'False' and response has errors
        """
        if not self._client:
            log.error("Invalid Twilio credentials")
            raise CommunicationsError(errors=["Invalid Twilio credentials!"])

        msgData = {
            "from_": self._sender.phone,
            "to": toPhone,
            "body": msg,
            "media_url": media,
        }

        twilioResp = None
        twilioErrors = []

        try:
            log.debug(f"Sending message via Twilio to {msgData['to']}")
            twilioResp = self._client.messages.create(**msgData)

            if twilioResp.status in [_STATUS_FAILED_, _STATUS_UNDELIVERED_]:
                twilioErrors.append(
                    f"{str(twilioResp.status).upper()} [{twilioResp.error_code}]: {twilioResp.error_message}"  # noqa: B950
                )

        except TwilioRestException as err:
            twilioErrors.append(repr(err))

        response = self._make_response(msgData, twilioResp, twilioErrors)
        log.info(f"Twilio response code: {response}")

        if not suppress:
            response.raise_on_errors()

        return response

    def send_message(self, msg: str, **kwargs: Any) -> List[Response]:
        """Send SMS to one or more recipients.

        This method provides a standard interface for sending SMS messages
        using the Twilio API.

        Args:
            msg:
                Plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            'list' of 'Response' objects from Twilio service API call. We always return
            a list even though we'll only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            MissingAttributeError: Message text is empty, or 'to' and/or 'from' phone numbers
                are empty/missing
        """
        if not msg.strip():
            log.error("Blank SMS message")
            raise MissingAttributeError("SMS message cannot be blank.")

        toList = ToPhone(
            inList=kwargs.get(const.KWD_TO_PHONE, self._defaultTo),
            maxNum=_MAX_RECIPIENTS_,
        )

        if not self._sender.phone:
            log.error("Blank 'from' phone number")
            raise MissingAttributeError("'from' phone number cannot be blank.")

        media = Media(inList=kwargs.get(const.KWD_MEDIA, []), maxNum=_MAX_MEDIA_)
        suppress = kwargs.get(const.KWD_SUPPRESS_ERROR, False)

        return [
            self._send_single_message(
                toPhone=phn, msg=msg, media=media.clean, suppress=suppress
            )
            for phn in toList.clean
        ]
