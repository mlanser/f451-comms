"""Test cases for the 'comms_Twilio' module."""
from configparser import ConfigParser  # noqa: F401

import pytest
import src.f451_comms.constants as const
import src.f451_comms.providers.twilio as twilio
from pytest_mock import MockerFixture  # noqa: F401
from src.f451_comms.exceptions import MissingAttributeError


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_DEFAULT_MSG_: str = "Hello World!"
_DEFAULT_MEDIA_: str = "path/to/joker.jpg"

_TEST_ACCT_SID_: str = "_YOUR_TWILIO_SID_"
_TEST_AUTH_TOKEN_: str = "_YOUR_TWILIO_TOKEN_"
_TEST_FROM_PHONE_: str = "+12125550000"
_TEST_TO_PHONE_: str = "+12125551111"


@pytest.fixture()
def mixed_media_list():
    """Return mixed media list."""
    return [_DEFAULT_MEDIA_, "path/to/riddler.jpg"]


@pytest.fixture()
def mixed_attribs():
    """Return mixed attributes."""
    return {
        const.KWD_FROM_PHONE: _TEST_FROM_PHONE_,
        const.KWD_TO_PHONE: _TEST_TO_PHONE_,
    }


@pytest.fixture()
def twilioClient(valid_settings, mixed_attribs):
    """Return Twilio client."""
    return twilio.Twilio(
        acctSID=valid_settings.get(
            const.CHANNEL_TWILIO, const.KWD_ACCT_SID, fallback=""
        ),
        authToken=valid_settings.get(
            const.CHANNEL_TWILIO, const.KWD_AUTH_TOKEN, fallback=""
        ),
        **mixed_attribs,
    )


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_create_Twilio_object(twilioClient, valid_settings, mixed_attribs):
    """Verify ability to create a Twilio client."""
    client = twilioClient
    assert client.serviceType == const.SRV_TYPE_SMS
    assert client.serviceName == twilio._SRV_PROVIDER_
    assert client.configSection == twilio._SRV_CONFIG_SCTN_

    client = twilio.Twilio(
        valid_settings.get(const.CHANNEL_TWILIO, const.KWD_ACCT_SID, fallback=""),
        valid_settings.get(const.CHANNEL_TWILIO, const.KWD_AUTH_TOKEN, fallback=""),
        **mixed_attribs,
    )
    assert client.defaultTo[0].phone == _TEST_TO_PHONE_
    assert client.sender.phone == _TEST_FROM_PHONE_


def test_send_message(mocker, twilioClient):
    """Verify ability to send a message."""
    with pytest.raises(MissingAttributeError) as e:
        twilioClient.send_message("")
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    attribs = {
        const.KWD_TO_PHONE: "",
    }
    with pytest.raises(MissingAttributeError) as e:
        twilioClient.send_message(_DEFAULT_MSG_, **attribs)
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    attribs = {
        const.KWD_TO_PHONE: _TEST_TO_PHONE_,
    }

    mockTwilioClient = twilioClient
    mocker.patch.object(mockTwilioClient, "send_message", autospec=True)
    twilioClient.send_message(_DEFAULT_MSG_, **attribs)
    twilioClient.send_message.assert_called_once()


@pytest.mark.slow
def test_send_message_extensive(mocker, twilioClient, new_media_file) -> None:
    """Verify ability to send complex message."""
    attribs = {
        const.KWD_TO_PHONE: ["+12125550000", "+12125551111"],
        const.KWD_MEDIA: new_media_file,
    }

    mockTwilioClient = twilioClient
    mocker.patch.object(mockTwilioClient, "send_message", autospec=True)
    twilioClient.send_message(_DEFAULT_MSG_, **attribs)
    twilioClient.send_message.assert_called_once()


# from inspect import currentframe, getframeinfo
# helpers.pp(capsys, data, currentframe())
