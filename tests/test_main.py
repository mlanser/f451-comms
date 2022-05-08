"""Test cases for the '__main__' module."""
import sys  # noqa: F401
from configparser import ConfigParser
from inspect import currentframe  # noqa: F401
from inspect import getframeinfo  # noqa: F401
from unittest import mock  # noqa: F401

import pytest
from faker import Faker  # noqa: F401

from f451_comms import __app_name__
from f451_comms import __main__
from f451_comms import __version__


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_KWD_VERSION_SHORT_ = "-V"
_KWD_VERSION_LONG_ = "--version"
_KWD_CHANNEL_ = "--channel"
_KWD_CONFIG_ = "--config"
_KWD_SECRETS_ = "--secrets"


@pytest.fixture()
def valid_attribs():
    """Return valid test attribs."""
    return {"one": False, "two": "something"}


@pytest.fixture()
def valid_string():
    """Return valid test string."""
    return "VALID TEST STRING"


@pytest.fixture
def fake_filesystem(fs):  # pylint:disable=invalid-name
    """Init fake filesystem.

    Variable name 'fs' causes a pylint warning. Provide a longer name
    acceptable to pylint for use in tests.
    """
    yield fs


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
@pytest.mark.parametrize("kwd", [_KWD_VERSION_SHORT_, _KWD_VERSION_LONG_])
def test_main_show_version(capsys, kwd):
    """Test display of app version."""
    with pytest.raises(SystemExit) as e:
        __main__.main([kwd])

    captured = capsys.readouterr()
    result = captured.out

    assert __app_name__ in result
    assert __version__ in result

    assert e.type == SystemExit
    assert e.value.code == 0


def test_main_fail_on_invalid_channels(capsys, invalid_string):
    """Test failing on invalid channel names."""
    with pytest.raises(SystemExit) as e:
        __main__.main([_KWD_CHANNEL_, invalid_string])

    captured = capsys.readouterr()
    result = captured.out

    assert e.type == SystemExit
    assert e.value.code == 1
    assert invalid_string in result


def test_main_fail_on_invalid_config_file(invalid_file):
    """Test failing on missing config files."""
    with pytest.raises(ValueError) as e:
        __main__.main([_KWD_CONFIG_, invalid_file])

    assert e.type == ValueError


def test_main_fail_on_invalid_secrets_file(invalid_file):
    """Test failing on invalid secrets file."""
    with pytest.raises(ValueError) as e:
        __main__.main([_KWD_SECRETS_, invalid_file])

    assert e.type == ValueError


def test_ini_parser(new_config_file):
    """Test initializing parser with valid config file."""
    # Provide as single item
    parser = __main__.init_ini_parser(new_config_file)
    assert isinstance(parser, ConfigParser)

    # Provide as list of items
    parser = __main__.init_ini_parser([new_config_file])
    assert isinstance(parser, ConfigParser)


def test_ini_parsers_fail_on_invalid(invalid_file):
    """Test failing on invalid config file."""
    # Provide as single item
    with pytest.raises(ValueError) as e:
        __main__.init_ini_parser(invalid_file)
    assert e.type == ValueError

    # Provide as list of items
    with pytest.raises(ValueError) as e:
        __main__.init_ini_parser([invalid_file])
    assert e.type == ValueError


# from inspect import currentframe, getframeinfo
# helpers.pp(capsys, data, currentframe())
