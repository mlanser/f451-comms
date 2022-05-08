"""Test cases for 'entity' module."""
import pytest

import f451_comms.entity as entity


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_MIXED_ENTITY_LIST_WITH_THREE_VALID_ONE_DUPE_ = {
    "name": [
        entity.Entity(
            name="Name",
            email="foo@example.com",
            phone="+12125550001",
            twitter="foo",
            slack="foo",
        ),
        entity.Entity(
            name="Name",
            email="bar@example.com",
            phone="+12125550002",
            twitter="bar",
            slack="bar",
        ),
        entity.Entity(
            name="Fizz",
            email="fizz@example.com",
            phone="+12125550003",
            twitter="fizz",
            slack="fizz",
        ),
        entity.Entity(
            name="Bang",
            email="bang@example.com",
            phone="+12125550004",
            twitter="bang",
            slack="bang",
        ),
    ],
    "email": [
        entity.Entity(
            name="Foo",
            email="email@example.com",
            phone="+12125550001",
            twitter="foo",
            slack="foo",
        ),
        entity.Entity(
            name="Bar",
            email="email@example.com",
            phone="+12125550002",
            twitter="bar",
            slack="bar",
        ),
        entity.Entity(
            name="Fizz",
            email="fizz@example.com",
            phone="+12125550003",
            twitter="fizz",
            slack="fizz",
        ),
        entity.Entity(
            name="Bang",
            email="bang@example.com",
            phone="+12125550004",
            twitter="bang",
            slack="bang",
        ),
    ],
    "phone": [
        entity.Entity(
            name="Foo",
            email="foo@example.com",
            phone="+12125550001",
            twitter="foo",
            slack="foo",
        ),
        entity.Entity(
            name="Bar",
            email="bar@example.com",
            phone="+12125550002",
            twitter="bar",
            slack="bar",
        ),
        entity.Entity(
            name="Fizz",
            email="fizz@example.com",
            phone="+12125550002",
            twitter="fizz",
            slack="fizz",
        ),
        entity.Entity(
            name="Bang",
            email="bang@example.com",
            phone="+12125550004",
            twitter="bang",
            slack="bang",
        ),
    ],
    "twitter": [
        entity.Entity(
            name="Foo",
            email="foo@example.com",
            phone="+12125550001",
            twitter="foo",
            slack="foo",
        ),
        entity.Entity(
            name="Bar",
            email="bar@example.com",
            phone="+12125550001",
            twitter="same",
            slack="bar",
        ),
        entity.Entity(
            name="Fizz",
            email="fizz@example.com",
            phone="+12125550003",
            twitter="fizz",
            slack="fizz",
        ),
        entity.Entity(
            name="Bang",
            email="bang@example.com",
            phone="+12125550004",
            twitter="same",
            slack="bang",
        ),
    ],
    "slack": [
        entity.Entity(
            name="Foo",
            email="foo@example.com",
            phone="+12125550001",
            twitter="foo",
            slack="foo",
        ),
        entity.Entity(
            name="Bar",
            email="bar@example.com",
            phone="+12125550001",
            twitter="bar",
            slack="same",
        ),
        entity.Entity(
            name="Fizz",
            email="fizz@example.com",
            phone="+12125550003",
            twitter="fizz",
            slack="same",
        ),
        entity.Entity(
            name="Bang",
            email="bang@example.com",
            phone="+12125550004",
            twitter="bang",
            slack="bang",
        ),
    ],
}

_INVALID_EMAIL_STRINGS_ = [
    r"test",
    r"test@",
    r"test@example",
    r"@example.com",
    r"example.com",
    r".com",
    r"foo@bar@example.com",
    r"foo\@example.com",
    r"foo:example.com",
    r"foo bar@example.com",
]

_INVALID_PHONE_STRINGS_ = [
    r"123456789",
    r"+123456789",
    r"1234567890",
    r"12345678901",
    r"123456789012345",
    r"1-234-567-8901",
    r"(234) 567-8901",
    r"+1234567890123456",
]

_INVALID_TWITTER_STRINGS_ = [
    r"abc34567890123456",
    r"abc_123_cde_456_XX",
    r"abc-123",
    r"abc.cde",
    r"abc@123",
]


@pytest.fixture()
def valid_entity():
    """Return info to generate a valid `Entity` object."""
    return {
        "name": "Test Name",
        "email": "test@example.com",
        "phone": "+12125550000",
        "slack": "testslack12345",
        "twitter": "testtwitter2345",
    }


@pytest.fixture()
def mixed_entity_three_valid_one_dupe():
    """Return mixed `Entity` list."""
    return _MIXED_ENTITY_LIST_WITH_THREE_VALID_ONE_DUPE_


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_create_entity_happy_path(valid_entity):
    """Test creating new `Entity` object with valid info."""
    data = valid_entity
    ent = entity.Entity(**data)
    assert ent.name == data["name"]
    assert ent.email == data["email"]
    assert ent.phone == data["phone"]
    assert ent.slack == data["slack"]
    assert ent.twitter == data["twitter"]
    assert ent.to_dict() == data


def test_create_entity_all_empty_items():
    """Test creating new `Entity` object with missing info."""
    ent = entity.Entity(
        name="",
        email="",
        phone="",
        slack="",
        twitter="",
    )
    assert ent.name == ""
    assert ent.email == ""
    assert ent.phone == ""
    assert ent.slack == ""
    assert ent.twitter == ""


def test_create_invalid_name():
    """Test creating new `Entity` object with invalid name string."""
    tooLong = "x" * (entity._MAX_LEN_NAME_ + 10)

    with pytest.raises(ValueError) as e:
        entity.Entity(name=tooLong)
    assert e.type == ValueError
    assert str(entity._MAX_LEN_NAME_) in e.value.args[0]


@pytest.mark.parametrize("invalid", _INVALID_EMAIL_STRINGS_)
def test_create_invalid_email(invalid):
    """Test creating new `Entity` object with invalid email address."""
    with pytest.raises(ValueError) as e:
        entity.Entity(email=invalid)
    assert e.type == ValueError
    assert "Invalid email" in e.value.args[0]


@pytest.mark.parametrize("invalid", _INVALID_PHONE_STRINGS_)
def test_create_invalid_phone(invalid):
    """Test creating new `Entity` object with invalid phone number."""
    with pytest.raises(ValueError) as e:
        entity.Entity(phone=invalid)
    assert e.type == ValueError
    assert "Invalid phone" in e.value.args[0]


def test_create_invalid_slack():
    """Test creating new `Entity` object with invalid Slack name."""
    tooLong = "x" * (entity._MAX_LEN_SLACK_ + 1)
    with pytest.raises(ValueError) as e:
        entity.Entity(slack=tooLong)
    assert e.type == ValueError
    assert str(entity._MAX_LEN_SLACK_) in e.value.args[0]


@pytest.mark.parametrize("invalid", _INVALID_TWITTER_STRINGS_)
def test_create_invalid_twitter(invalid):
    """Test creating new `Entity` object with invalid Twitter name."""
    with pytest.raises(ValueError) as e:
        entity.Entity(twitter=invalid)
    assert e.type == ValueError
    assert "Invalid Twitter" in e.value.args[0]


def test_dedupe_by_attribute(mixed_entity_three_valid_one_dupe):
    """Test de-duping a list of objects by a given attribute."""
    for key, val in mixed_entity_three_valid_one_dupe.items():
        tmpSet = entity.dedupe_by_attribute(val, key)
        clean = [item for item in tmpSet if hasattr(item, key)]
        assert len(clean) == 3


# from inspect import currentframe, getframeinfo
# helpers.pp(capsys, data, currentframe())
# helpers.pp(capsys, Hdrs['sql'], currentframe())
# helpers.pp(capsys, Hdrs['raw'], currentframe())
# helpers.pp(capsys, dataFName, currentframe())
# helpers.pp(capsys, tblName, currentframe())
# helpers.pp(capsys, dataOut, currentframe())
# helpers.pp(capsys, dataIn, currentframe())
