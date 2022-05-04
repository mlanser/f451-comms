"""Test cases for the generic SMS provider module."""
import re

import pytest
import src.f451_comms.constants as const
import src.f451_comms.providers.sms as sms
from src.f451_comms.entity import Entity
from src.f451_comms.exceptions import MissingAttributeError


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_MIXED_STRING_LISTS_ONE_VALID_ = [
    "+12125552222|123",
    "123|+12125552222|456",
    "123|+12125552222",
    "123|456|+12125552222",
    "+12125552222|abc",
    ["+12125552222", "456"],
    ["123", "+12125552222", "456"],
    ["123", "+12125552222"],
    ["123", "bar", "+12125552222"],
    ["123", "", "+12125552222"],
    ["", "+12125552222", ""],
    ["123", "+12125552222", ""],
    ["+12125552222", "abc"],
]

_MIXED_PHONE_LIST_ = [
    "+1-212-555-0000",
    "+1.212.555.1111",
    "+12125552222",
]

_MIXED_STRINGS_LIST_WITH_THREE_VALID_ONE_DUPE_ = [
    ["+1-212-555-0001", "+1-212-555-0002", "+1-212-555-0001", "+1-212-555-0003"],
    "+1-212-555-0001|+1-212-555-0002|+1-212-555-0001|+1-212-555-0003",
]

_MIXED_ENTITY_LIST_WITH_THREE_VALID_ONE_DUPE_ = [
    [
        Entity(name="Foo", phone="+12125550001"),
        Entity(name="Bar", phone="+12125550001"),
        Entity(name="Fizz", phone="+12125550003"),
        Entity(name="Bang", phone="+12125550004"),
    ],
    [
        Entity(name="Foo", email="foo@example.com", phone="+12125550001"),
        Entity(name="Bar", email="bar@example.com", phone="+12125550001"),
        Entity(name="Fizz", email="fizz@example.com", phone="+12125550003"),
        Entity(name="Bang", email="bang@example.com", phone="+12125550004"),
    ],
    [
        Entity(
            name="Foo", email="foo@example.com", phone="+12125550001", twitter="foo"
        ),
        Entity(
            name="Bar", email="bar@example.com", phone="+12125550001", twitter="bar"
        ),
        Entity(
            name="Fizz", email="fizz@example.com", phone="+12125550003", twitter="fizz"
        ),
        Entity(
            name="Bang", email="bang@example.com", phone="+12125550004", twitter="bang"
        ),
    ],
    [
        Entity(
            name="Foo",
            email="foo@example.com",
            phone="+12125550001",
            twitter="foo",
            slack="foo",
        ),
        Entity(
            name="Bar",
            email="bar@example.com",
            phone="+12125550001",
            twitter="bar",
            slack="bar",
        ),
        Entity(
            name="Fizz",
            email="fizz@example.com",
            phone="+12125550003",
            twitter="fizz",
            slack="fizz",
        ),
        Entity(
            name="Bang",
            email="bang@example.com",
            phone="+12125550004",
            twitter="bang",
            slack="bango",
        ),
    ],
    [
        Entity(
            name="Foo",
            email="foo@example.com",
            phone="+12125550001",
            twitter="foo",
            slack="foo",
        ),
        Entity(
            name="Bar",
            email="bar@example.com",
            phone="+12125550001",
            twitter="bar",
            slack="bar",
        ),
        Entity(
            name="Fizz",
            email="fizz@example.com",
            phone="+12125550003",
            twitter="fizz",
            slack="fizz",
        ),
        Entity(
            name="Bang",
            email="bang@example.com",
            phone="+12125550004",
            twitter="bang",
            slack="bang",
        ),
    ],
]


@pytest.fixture()
def mixed_phone_list():
    """Return mixed phone number list."""
    return _MIXED_PHONE_LIST_


@pytest.fixture()
def clean_phone_list():
    """Return clean phone number list."""
    return [re.sub("[^0-9+]", "", item) for item in _MIXED_PHONE_LIST_]


@pytest.fixture()
def mixed_entity_list():
    """Return mixed 'Entity' list."""
    return [Entity(phone=item) for item in _MIXED_PHONE_LIST_]


@pytest.fixture()
def mixed_string_list_one_valid():
    """Return mixed string list."""
    return _MIXED_STRING_LISTS_ONE_VALID_


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_process_recipient_list_with_valid_phone_strings():
    """Test ability to process recipient list with valid phone numbers."""
    data = sms.process_recipient_list("+1-212-555-0001", 2)
    assert len(data) == 1

    data = sms.process_recipient_list("+1-212-555-0001|+1-212-555-0002", 2)
    assert len(data) == 2

    data = sms.process_recipient_list(["+1-212-555-0001", "+1-212-555-0002"], 2)
    assert len(data) == 2

    data = sms.process_recipient_list(
        "+1-212-555-0001|+1-212-555-0002|+1-212-555-0003", 2
    )
    assert len(data) == 2

    data = sms.process_recipient_list(
        ["+1-212-555-0001", "+1-212-555-0002", "+1-212-555-0003"], 2
    )
    assert len(data) == 2


@pytest.mark.parametrize("testData", ["123", ["2125550000", "212555"]])
def test_process_recipient_list_with_invalid_phone_strings(testData):
    """Test ability to process recipient list with invalid phone numbers."""
    data = sms.process_recipient_list(testData, 5)
    assert data == []


@pytest.mark.parametrize("testData", _MIXED_STRING_LISTS_ONE_VALID_)
def test_process_recipient_list_with_mixed_phone_strings(testData):
    """Test ability to process recipient list with mixed phone number strings."""
    data = sms.process_recipient_list(testData, 5)
    assert len(data) == 1


@pytest.mark.parametrize("testData", _MIXED_STRINGS_LIST_WITH_THREE_VALID_ONE_DUPE_)
def test_process_recipient_list_with_duplicate_phone_strings(testData):
    """Test ability to process recipient list with duplicate phone number strings."""
    data = sms.process_recipient_list(testData, 10)
    assert len(data) == 3


def test_process_recipient_list_with_entities():
    """Test ability to process recipient list with 'Entity' objects."""
    batman = Entity(name="Batman", email="batman@example.com", phone="+1-212-555-0001")
    robin = Entity(name="Robin", email="robin@example.com", phone="+1-212-555-0002")
    alfred = Entity(name="Alfred", email="alfred@example.com", phone="+1-212-555-0003")

    data = sms.process_recipient_list(batman, 2)
    assert len(data) == 1

    data = sms.process_recipient_list([batman, robin], 2)
    assert len(data) == 2

    data = sms.process_recipient_list([batman, robin, alfred], 2)
    assert len(data) == 2

    noPhone = Entity(name="No Phone")
    data = sms.process_recipient_list([batman, robin, alfred, noPhone], 10)
    assert len(data) == 3


@pytest.mark.parametrize("testData", _MIXED_ENTITY_LIST_WITH_THREE_VALID_ONE_DUPE_)
def test_process_recipient_list_with_duplicate_entities(testData):
    """Test ability to process recipient list with duplicate 'Entity' objects."""
    data = sms.process_recipient_list(testData, 10)
    assert len(data) == 3


def test_create_ToPhone_object(mixed_phone_list, mixed_entity_list, clean_phone_list):
    """Test ability to create a 'ToPhone' object."""
    # Test happy path
    totNum = len(mixed_phone_list)
    maxNum = totNum + 1
    obj = sms.ToPhone(inList=mixed_phone_list, maxNum=maxNum)
    assert obj.keyword == const.KWD_TO_PHONE
    assert obj.isRequired
    assert obj.isValid
    assert obj.minNum == 1
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum
    verifyRaw = [item in mixed_entity_list for item in obj.raw]
    verifyClean = [item in clean_phone_list for item in obj.clean]
    assert all(verifyRaw)
    assert all(verifyClean)

    # Test 'maxNum'
    maxNum = len(mixed_phone_list) - 1
    obj = sms.ToPhone(inList=mixed_phone_list, maxNum=maxNum)
    assert obj.minNum == 1
    assert obj.maxNum == maxNum
    assert obj.totNum == maxNum
    assert len(obj.raw) == maxNum
    assert len(obj.clean) == maxNum

    # Test 'maxNum' cannot be smaller than 'minNum'
    obj = sms.ToPhone(inList=mixed_phone_list, maxNum=0)
    assert obj.minNum == 1
    assert obj.maxNum == 1
    assert obj.totNum == 1

    # Test assertion that 'to' cannot be empty
    with pytest.raises(MissingAttributeError) as e:
        sms.ToPhone(inList=[""], maxNum=10)
    assert e.type == MissingAttributeError
    assert "to" in e.value.args[0]

    # Test that 'to' should not be empty when not in strict mode
    obj = sms.ToPhone(inList=[""], maxNum=10, strict=False)
    assert not obj.isValid  # 'valid' flag is set to 'False'
    assert obj.raw == []  # 'data' is empty list
    assert obj.clean == []


# from inspect import currentframe, getframeinfo
# helpers.pp(capsys, data, currentframe())
# helpers.pp(capsys, Hdrs['sql'], currentframe())
# helpers.pp(capsys, Hdrs['raw'], currentframe())
# helpers.pp(capsys, dataFName, currentframe())
# helpers.pp(capsys, tblName, currentframe())
# helpers.pp(capsys, dataOut, currentframe())
# helpers.pp(capsys, dataIn, currentframe())
