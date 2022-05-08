"""Test cases for 'utils' module."""
from configparser import ConfigParser

import pytest

import f451_comms.utils as utils


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_DEFAULT_TEST_STRING_ = "DEFAULT_TEST_STRING"

_VALID_EMAIL_STRINGS_ = [
    "one@example.com",
    "two@example.com",
    "three@example.com",
    "first.last@example.com",
    "under_score@example.com",
    "beep@boop.io",
    "one+two@example.com",
]

_INVALID_EMAIL_STRINGS_ = [
    "",
    "one@example",
    "two.com",
    "three",
    "first.last.example.com",
    "under_score@example_com",
    "beep@boop@io",
]

_VALID_PHONE_STRINGS_ = [
    "+12125550000",
    "+112125551111",
    "+1112125552222",
]

_INVALID_PHONE_STRINGS_ = [
    "ABC",
    "+1 (212) 555-1111",
    "+1-212-555-2222",
    "+1-212-555",
    "+1-212",
    "12223334444",
]

_VALID_TWITTER_STRINGS_ = [
    "one",
    "twothree",
    "four_five",
    "six456789012345",
]

_INVALID_TWITTER_STRINGS_ = [
    "this_is_a_really_long_twitter_name",
    "one.two",
    "three@four",
    "first-last",
    "under+score",
]

_TRUE_VALUES_ = ["True", "trUe", "t", 1, "1", True]
_FALSE_VALUES_ = ["False", "noTrue", "F", 0, "0", False]


@pytest.fixture()
def valid_channel_map():
    """Return valid channel map info."""
    return {
        "email": "f451_mailgun",
        "sms": "f451_twilio",
        "twitter": "f451_twitter",
        "slack": "f451_slack",
        "forums": "f451_slack",
    }


@pytest.fixture()
def mixed_email_address_list():
    """Return valid email address strings."""
    return _VALID_EMAIL_STRINGS_


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_process_key_value_map(valid_channel_map):
    """Test processing key-value maps."""
    expectedMap = valid_channel_map
    mapString = "email:f451_mailgun|sms:f451_twilio|twitter:f451_twitter|slack:f451_slack|forums:f451_slack"
    mapList = [
        "email:f451_mailgun",
        "sms:f451_twilio",
        "twitter:f451_twitter",
        "slack:f451_slack",
        "forums:f451_slack",
    ]

    # Happy path
    processedMap = utils.process_key_value_map(mapString)
    assert processedMap == expectedMap

    processedMap = utils.process_key_value_map(mapList)
    assert processedMap == expectedMap

    # Not so happy paths
    mapList = ["email:", ":", "", "slack:f451_slack", "forums:f451_slack"]
    processedMap = utils.process_key_value_map(mapList)
    assert processedMap == {"slack": "f451_slack", "forums": "f451_slack"}

    mapString = "email:f451_mailgun:sms:f451_twilio"
    processedMap = utils.process_key_value_map(mapString)
    assert processedMap == {"email": "f451_mailgun"}

    mapString = "email:f451_mailgun:sms f451_twilio|twitter|f451_twitter|slack:f451_slack|:f451_slack"
    processedMap = utils.process_key_value_map(mapString)
    assert processedMap == {"email": "f451_mailgun", "slack": "f451_slack"}


@pytest.mark.parametrize(
    "mapList", [[], [" ", ": ", ""], "email:", "email|f451_mailgun", ":|"]
)
def test_process_key_value_map_always_return_empty(mapList):
    """Test processing empty key-value maps."""
    processedMap = utils.process_key_value_map(mapList)
    assert processedMap == {}


@pytest.mark.parametrize("testData", _VALID_EMAIL_STRINGS_)
def test_is_valid_email_is_true(testData):
    """Test validating email address strings."""
    assert utils.is_valid_email(testData)


@pytest.mark.parametrize("testData", _INVALID_EMAIL_STRINGS_)
def test_is_valid_email_is_false(testData):
    """Test validating email address strings."""
    assert not utils.is_valid_email(testData)


@pytest.mark.parametrize("testData", _VALID_PHONE_STRINGS_)
def test_is_valid_phone_is_true(testData):
    """Test validating phone number strings."""
    assert utils.is_valid_phone(testData)


@pytest.mark.parametrize("testData", _INVALID_PHONE_STRINGS_)
def test_is_valid_phone_is_false(testData):
    """Test validating phone number strings."""
    assert not utils.is_valid_phone(testData)


@pytest.mark.parametrize("testData", _VALID_TWITTER_STRINGS_)
def test_is_valid_twitter_is_true(testData):
    """Test validating Twitter name strings."""
    assert utils.is_valid_twitter(testData)


@pytest.mark.parametrize("testData", _INVALID_TWITTER_STRINGS_)
def test_is_valid_twitter_is_false(testData):
    """Test validating Twitter name strings."""
    assert not utils.is_valid_twitter(testData)


def test_convert_attrib_str_to_list():
    """Test converting attribute strings to lists of attributes."""
    val = utils.convert_attrib_str_to_list("apple|banana|orange", "|")
    assert set(val) == {"apple", "banana", "orange"}

    val = utils.convert_attrib_str_to_list("apple|", "|")
    assert set(val) == {"apple"}

    val = utils.convert_attrib_str_to_list("apple", "|")
    assert set(val) == {"apple"}

    val = utils.convert_attrib_str_to_list("1|2|3|4|5", "|")
    assert set(val) == {"1", "2", "3", "4", "5"}

    val = utils.convert_attrib_str_to_list("1|2|3|4|5", "|", int)
    assert set(val) == {1, 2, 3, 4, 5}


@pytest.mark.parametrize("testData", _TRUE_VALUES_)
def test_convert_str_to_bool_is_true(testData):
    """Test converting string values to boolean values."""
    assert utils.convert_str_to_bool(testData)


@pytest.mark.parametrize("testData", _FALSE_VALUES_)
def test_convert_str_to_bool_is_false(testData):
    """Test converting string values to boolean values."""
    assert not utils.convert_str_to_bool(testData)


def test_process_string_list():
    """Test processing lists of string."""
    val = utils.process_string_list(["apple", "banana", "orange"], "_p_", "_s_", "_j_")
    assert val == "_p_apple_s__j__p_banana_s__j__p_orange_s_"

    val = utils.process_string_list(["apple", "banana", "orange"], "", "", "")
    assert val == "applebananaorange"

    val = utils.process_string_list(["apple", "", "orange"], "_p_", "_s_", "_j_")
    assert val == "_p_apple_s__j__p_orange_s_"

    val = utils.process_string_list(["apple", "", ""], "_p_", "_s_", "_j_")
    assert val == "_p_apple_s_"

    val = utils.process_string_list(["", "", ""], "_p_", "_s_", "_j_")
    assert val == ""

    val = utils.process_string_list([], "_p_", "_s_", "_j_")
    assert val == ""

    val = utils.process_string_list("apple|banana|orange", "_p_", "_s_", "_j_")
    assert val == "_p_apple_s__j__p_banana_s__j__p_orange_s_"


def test_static_parse_attrib(valid_attribs_dict, default_test_key, default_test_val):
    """Test parsing attribute lists."""
    val = utils.parse_attribs(valid_attribs_dict, default_test_key)
    assert val == default_test_val

    val = utils.parse_attribs(valid_attribs_dict, "INVALID_KEY")
    assert val is None

    val = utils.parse_attribs(valid_attribs_dict, "INVALID_KEY", _DEFAULT_TEST_STRING_)
    assert val == _DEFAULT_TEST_STRING_

    val = utils.parse_attribs(
        "INVALID_STRUCTURE", default_test_key, _DEFAULT_TEST_STRING_
    )
    assert val == _DEFAULT_TEST_STRING_


def test_static_convert_str_to_dict(valid_config_string, valid_config_dict):
    """Test converting strings to `dict` structures."""
    val = utils.convert_config_str_to_dict(valid_config_string)
    assert val == valid_config_dict

    with pytest.raises(ValueError) as e:
        utils.convert_config_str_to_dict("NO:SECTION")
    assert e.type == ValueError
    assert "NO:SECTION" in e.value.args[0]

    with pytest.raises(ValueError) as e:
        utils.convert_config_str_to_dict("|FOO:BAR")
    assert e.type == ValueError
    assert "Section label" in e.value.args[0]  # TODO - create better check

    with pytest.raises(ValueError) as e:
        utils.convert_config_str_to_dict("SECTION|")
    assert e.type == ValueError
    assert "Section items" in e.value.args[0]  # TODO - create better check


def test_static_process_config(valid_config_string, valid_config_dict, valid_config):
    """Test processing config files/values."""
    val = utils.process_config(valid_config_string)
    assert isinstance(val, ConfigParser)

    val = utils.process_config(valid_config_dict)
    assert isinstance(val, ConfigParser)

    val = utils.process_config(valid_config)
    assert isinstance(val, ConfigParser)

    with pytest.raises(ValueError) as e:
        utils.process_config(["TEST", "INVALID", "TYPE"])
    assert e.type == ValueError
    assert "list" in e.value.args[0]


def test_static_parse_defaults(valid_config, valid_attribs_dict, default_test_section):
    """Test parsing default settings/values."""
    val = utils.parse_defaults(valid_config, [default_test_section])
    assert val == valid_attribs_dict
