"""Test cases for the 'comms' module."""
from configparser import ConfigParser

import pytest
import tweepy

from f451_comms.comms import Comms
from f451_comms.providers.mailgun import Mailgun
from f451_comms.providers.slack import Slack
from f451_comms.providers.twilio import Twilio
from f451_comms.providers.twitter import Twitter

# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_KWD_VERSION_SHORT_ = "-V"
_KWD_VERSION_LONG_ = "--version"
_KWD_CHANNEL_ = "--channel"
_KWD_CONFIG_ = "--config"
_KWD_SECRETS_ = "--secrets"

_TEST_DEFAULT_ = "TEST_DEFAULT"


@pytest.fixture()
def valid_string():
    """Return valid test string."""
    return "VALID TEST STRING"


@pytest.fixture()
def invalid_channel_secrets() -> ConfigParser:
    """Return invalid config data."""
    parser = ConfigParser()
    parser.read_dict({"invalid": {}})
    return parser


@pytest.fixture()
def valid_channel_map():
    """Return valid channel map."""
    channelMap = {
        "channel_map": {
            "email": "f451_mailgun",
            "sms": "f451_twilio",
            "twitter": "f451_twitter",
            "slack": "f451_slack",
            "forums": "f451_slack",
        }
    }

    parser = ConfigParser()
    parser.read_dict(channelMap)
    return parser


@pytest.fixture()
def valid_channel_list():
    """Return valid channel list."""
    return ["f451_mailgun", "f451_slack", "f451_twitter", "f451_twilio"]


@pytest.fixture()
def valid_channel_string():
    """Return valid channel string."""
    return "f451_mailgun|f451_slack|f451_twitter|f451_twilio"


@pytest.fixture()
def mockComms(mocker, valid_settings) -> Comms:
    """Return mock 'Comms' object."""
    mocker.patch.object(
        tweepy.API, "verify_credentials", autospec=True, return_value=True
    )
    return Comms(config=valid_settings)


class MockTwitterAuth:
    """Mock Twitter client."""

    @staticmethod
    def set_access_token(*args):
        """Mock method."""
        return None


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_verify_channel(
    mocker,
    mockComms,
    valid_settings,
    valid_channel_list,
    valid_channel_string,
):
    """Test ability to varify a given channel."""
    mocker.patch.object(tweepy, "OAuth1UserHandler", return_value=MockTwitterAuth)
    mocker.patch.object(tweepy.API, "verify_credentials", return_value=True)
    comms = Comms(valid_settings)

    assert comms.is_valid_channel(valid_channel_list)
    assert comms.is_valid_channel(valid_channel_string)

    assert comms.is_valid_channel(list(comms.channel_map.keys()))
    assert not comms.is_valid_channel(["INVALID"])
    assert not comms.is_valid_channel("INVALID")


def test_process_channel_list(
    mocker,
    mockComms,
    valid_channel_list,
    valid_channel_string,
    valid_channel_map,
):
    """Test ability to process a list of channels."""
    mocker.patch.object(tweepy, "OAuth1UserHandler", return_value=MockTwitterAuth)
    mocker.patch.object(tweepy.API, "verify_credentials", return_value=True)
    comms = mockComms

    val = comms.process_channel_list(valid_channel_list, False)
    assert set(val) == set(valid_channel_list)

    val = comms.process_channel_list(valid_channel_list, True)
    assert set(val) == set(valid_channel_list)

    val = comms.process_channel_list(valid_channel_string, True)
    assert set(val) == set(valid_channel_list)

    val = comms.process_channel_list(
        ["f451_mailgun", "f451_slack", "f451_twitter", "_INVALID_"], True
    )
    assert set(val) == {"f451_mailgun", "f451_slack", "f451_twitter"}

    val = comms.process_channel_list(
        ["f451_mailgun", "f451_slack", "", "_INVALID_"], True
    )
    assert set(val) == {"f451_mailgun", "f451_slack"}

    val = comms.process_channel_list(["_INVALID_", "_INVALID_", "", "_INVALID_"], True)
    assert val == []

    # Test channel map
    val = comms.process_channel_list(["email", "sms", "forums"], True)
    assert set(val) == {"f451_mailgun", "f451_twilio", "f451_slack"}

    val = comms.process_channel_list(["email", "email", "sms", "sms"], True)
    assert set(val) == {"f451_mailgun", "f451_twilio"}


def test_is_valid_channel(
    mocker,
    mockComms,
    valid_settings,
    valid_channel_list,
    valid_channel_string,
):
    """Test ability to check if channel is valid."""
    mocker.patch.object(tweepy, "OAuth1UserHandler", return_value=MockTwitterAuth)
    mocker.patch.object(tweepy.API, "verify_credentials", return_value=True)
    comms = Comms(valid_settings)

    assert comms.is_valid_channel(valid_channel_list)
    assert comms.is_valid_channel(valid_channel_string)

    assert comms.is_valid_channel(list(comms.channel_map.keys()))

    assert not comms.is_valid_channel(["INVALID"])
    assert not comms.is_valid_channel("INVALID")


def test_is_enabled_channel(
    mocker,
    mockComms,
    valid_settings,
    valid_channel_list,
    valid_channel_string,
):
    """Test ability to check if channel is enabled."""
    mocker.patch.object(tweepy, "OAuth1UserHandler", return_value=MockTwitterAuth)
    mocker.patch.object(tweepy.API, "verify_credentials", return_value=True)
    comms = Comms(valid_settings)

    assert comms.is_enabled_channel(valid_channel_list)
    assert comms.is_enabled_channel(valid_channel_string)

    assert not comms.is_enabled_channel(["INVALID"])
    assert not comms.is_enabled_channel("INVALID")


def test_static_init_mailgun(valid_settings):
    """Test ability initialize a Mailgun client."""
    val = Comms._init_mailgun(valid_settings)
    assert isinstance(val, Mailgun)


def test_static_init_mailgun_fail(invalid_channel_secrets):
    """Verify that Mailgun client is not initialized with invalid settings."""
    val = Comms._init_mailgun(invalid_channel_secrets)
    assert val is None


def test_static_init_twilio(valid_settings):
    """Test ability initialize a Twilio client."""
    val = Comms._init_twilio(valid_settings)
    assert isinstance(val, Twilio)


def test_static_init_twilio_fail(invalid_channel_secrets):
    """Verify that Twilio client is not initialized with invalid settings."""
    val = Comms._init_twilio(invalid_channel_secrets)
    assert val is None


def test_static_init_slack(valid_settings):
    """Test ability initialize a Slack client."""
    val = Comms._init_slack(valid_settings)
    assert isinstance(val, Slack)


def test_static_init_slack_fail(invalid_channel_secrets):
    """Verify that Slack client is not initialized with invalid settings."""
    val = Comms._init_slack(invalid_channel_secrets)
    assert val is None


def test_static_init_twitter(mocker, valid_settings):
    """Test ability initialize a Twitter client."""
    mocker.patch.object(tweepy, "OAuth1UserHandler", return_value=MockTwitterAuth)
    mocker.patch.object(tweepy.API, "verify_credentials", return_value=True)
    val = Comms._init_twitter(valid_settings)
    assert isinstance(val, Twitter)


def test_static_init_twitter_fail(mocker, invalid_channel_secrets):
    """Verify that Twitter client is not initialized with invalid settings."""
    mocker.patch.object(tweepy, "OAuth1UserHandler", return_value=MockTwitterAuth)
    mocker.patch.object(tweepy.API, "verify_credentials", return_value=True)
    val = Comms._init_twitter(invalid_channel_secrets)
    assert val is None


def test_init_config_and_obj_props(mocker, valid_settings, valid_channel_list):
    """Test ability initialize several clients."""
    mocker.patch.object(tweepy, "OAuth1UserHandler", return_value=MockTwitterAuth)
    mocker.patch.object(tweepy.API, "verify_credentials", return_value=True)
    communications = Comms(valid_settings)

    assert communications.Mailgun is not None
    assert communications.Twilio is not None
    assert communications.Slack is not None
    assert communications.Twitter is not None

    assert len(communications.valid_channels) == len(valid_channel_list)


def test_default_channels(mocker, valid_settings, default_channels_string):
    """Test ability verify default channels."""
    mocker.patch.object(tweepy, "OAuth1UserHandler", return_value=MockTwitterAuth)
    mocker.patch.object(tweepy.API, "verify_credentials", return_value=True)
    communications = Comms(valid_settings)
    defaultChannels = default_channels_string.split("|")
    assert sorted(communications.default_channels) == sorted(defaultChannels)


# from inspect import currentframe, getframeinfo
# helpers.pp(capsys, data, currentframe())
# helpers.pp(capsys, Hdrs['sql'], currentframe())
# helpers.pp(capsys, Hdrs['raw'], currentframe())
# helpers.pp(capsys, dataFName, currentframe())
# helpers.pp(capsys, tblName, currentframe())
# helpers.pp(capsys, dataOut, currentframe())
# helpers.pp(capsys, dataIn, currentframe())
