"""Test cases for the generic email provider module."""
import pytest
import src.f451_comms.constants as const
import src.f451_comms.providers.email as email
from src.f451_comms.entity import Entity
from src.f451_comms.exceptions import InvalidAttributeError
from src.f451_comms.exceptions import MissingAttributeError


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_MIXED_STRING_LISTS_ONE_VALID_ = [
    "one@example.com|foo",
    "foo|two@example.com|bar",
    "foo|threee@example.com",
    "foo|bar|four@example.com",
    ["one@example.com", "foo"],
    ["foo", "two@example.com", "bar"],
    ["foo", "threee@example.com"],
    ["foo", "bar", "four@example.com"],
    ["foo", "", "four@example.com"],
    ["", "two@example.com", ""],
    ["foo", "two@example.com", ""],
]

_MIXED_ADDRESS_LIST_ = [
    "one@example.com",
    "two@example.com",
    "threee@example.com",
]

_MIXED_STRINGS_LIST_WITH_THREE_VALID_ONE_DUPE_ = [
    ["foo@example.com", "foo@example.com", "fizz@example.com", "bang@example.com"],
    "foo@example.com|foo@example.com|fizz@example.com|bang@example.com",
]

_MIXED_ENTITY_LIST_WITH_THREE_VALID_ONE_DUPE_ = [
    [
        Entity(name="Foo", email="foo@example.com"),
        Entity(name="Bar", email="foo@example.com"),
        Entity(name="Fizz", email="fizz@example.com"),
        Entity(name="Bang", email="bang@example.com"),
    ],
    [
        Entity(name="Foo", email="foo@example.com", phone="+12125550001"),
        Entity(name="Bar", email="foo@example.com", phone="+12125550002"),
        Entity(name="Fizz", email="fizz@example.com", phone="+12125550003"),
        Entity(name="Bang", email="bang@example.com", phone="+12125550004"),
    ],
    [
        Entity(
            name="Foo", email="foo@example.com", phone="+12125550001", twitter="foo"
        ),
        Entity(
            name="Bar", email="foo@example.com", phone="+12125550002", twitter="bar"
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
            email="foo@example.com",
            phone="+12125550002",
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
            email="foo@example.com",
            phone="+12125550002",
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
def mixed_address_list():
    """Return mixed address list."""
    return _MIXED_ADDRESS_LIST_


@pytest.fixture()
def mixed_entity_list():
    """Return mixed 'Entity' objecgts."""
    return [Entity(email=item) for item in _MIXED_ADDRESS_LIST_]


@pytest.fixture()
def mixed_string_list_one_valid():
    """Return mixed strings."""
    return _MIXED_STRING_LISTS_ONE_VALID_


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_process_recipient_list_with_valid_email_strings():
    """Test ability to process recipient lists with valid emails."""
    data = email.process_recipient_list("batman@example.com", 2)
    assert len(data) == 1

    data = email.process_recipient_list("batman@example.com|robin@example.com", 2)
    assert len(data) == 2

    data = email.process_recipient_list(["batman@example.com", "robin@example.com"], 2)
    assert len(data) == 2

    data = email.process_recipient_list(
        "batman@example.com|robin@example.com|alfred@example.com", 2
    )
    assert len(data) == 2

    data = email.process_recipient_list(
        ["batman@example.com", "robin@example.com", "alfred@example.com"], 2
    )
    assert len(data) == 2


@pytest.mark.parametrize("testData", ["foo", ["foo", "bar"]])
def test_process_recipient_list_with_invalid_email_strings(testData):
    """Test ability to process recipient lists with invalid emails."""
    data = email.process_recipient_list(testData, 5)
    assert data == []


@pytest.mark.parametrize("testData", _MIXED_STRING_LISTS_ONE_VALID_)
def test_process_recipient_list_with_mixed_email_strings(testData):
    """Test ability to process recipient lists with mixed emails."""
    data = email.process_recipient_list(testData, 5)
    assert len(data) == 1


@pytest.mark.parametrize("testData", _MIXED_STRINGS_LIST_WITH_THREE_VALID_ONE_DUPE_)
def test_process_recipient_list_with_duplicate_email_strings(testData):
    """Test ability to process recipient lists with duplicate emails."""
    data = email.process_recipient_list(testData, 10)
    assert len(data) == 3


def test_process_recipient_list_with_entities():
    """Test ability to process recipient lists with 'Entity' objects."""
    batman = Entity(name="Batman", email="batman@example.com")
    robin = Entity(name="Robin", email="robin@example.com")
    alfred = Entity(name="Alfred", email="alfred@example.com")

    data = email.process_recipient_list(batman, 2)
    assert len(data) == 1

    data = email.process_recipient_list([batman, robin], 2)
    assert len(data) == 2

    data = email.process_recipient_list([batman, robin, alfred], 2)
    assert len(data) == 2

    noMail = Entity(name="No Mail")
    data = email.process_recipient_list([batman, robin, alfred, noMail], 10)
    assert len(data) == 3


@pytest.mark.parametrize("testData", _MIXED_ENTITY_LIST_WITH_THREE_VALID_ONE_DUPE_)
def test_process_recipient_list_with_duplicate_entities(testData):
    """Test ability to process recipient lists with duplicates."""
    data = email.process_recipient_list(testData, 10)
    assert len(data) == 3


@pytest.mark.slow
def test_process_attachment_list(new_attachment_file):
    """Test ability to process attachments."""
    # Test happy path
    processed = email.process_attachment_list(
        inList=[new_attachment_file, new_attachment_file]
    )
    assert len(processed) == 2

    processed = email.process_attachment_list(
        inList=f"{new_attachment_file}|{new_attachment_file}"
    )
    assert len(processed) == 2

    # Test max num attachments
    processed = email.process_attachment_list(
        inList=[
            new_attachment_file,
            new_attachment_file,
            new_attachment_file,
            new_attachment_file,
        ],
        maxNum=3,
    )
    assert len(processed) == 3

    # Test skipping blank filenames
    processed = email.process_attachment_list(
        inList=[new_attachment_file, "", new_attachment_file]
    )
    assert len(processed) == 2

    # Test skipping blank and invalid filenames
    processed = email.process_attachment_list(
        inList=[new_attachment_file, "", "_INVALID_FILE_"]
    )
    assert len(processed) == 1

    processed = email.process_attachment_list(inList=["", "", "_INVALID_FILE_"])
    assert processed == []

    with pytest.raises(InvalidAttributeError) as e:
        email.process_attachment_list(
            inList=[new_attachment_file, new_attachment_file], inType="_INVALID_TYPE_"
        )
    assert e.type == InvalidAttributeError
    assert const.KWD_ATTACHMENTS in e.value.args[0]


@pytest.mark.slow
def test_process_attachment_list_strict_mode(new_attachment_file):
    """Test ability to process attachments in 'strict' mode."""
    # Test assertion if file does not exist
    with pytest.raises(InvalidAttributeError) as e:
        email.process_attachment_list(
            inList=["_INVALID_FILE_"],
            strict=True,
        )
    assert e.type == InvalidAttributeError
    assert "_INVALID_FILE_" in e.value.args[0]

    # Test assertion if file does not exist
    with pytest.raises(InvalidAttributeError) as e:
        email.process_attachment_list(
            inList=[""],
            strict=True,
        )
    assert e.type == InvalidAttributeError
    assert "blank" in e.value.args[0]


def test_create_ToEmail_object_with_entities(mixed_address_list, mixed_entity_list):
    """Test ability to create 'CcEmail' object using 'Entity' objects."""
    # Test happy path
    totNum = len(mixed_entity_list)
    maxNum = totNum + 1
    obj = email.ToEmail(inList=mixed_entity_list, maxNum=maxNum)
    assert obj.keyword == const.KWD_TO_EMAIL
    assert obj.isRequired
    assert obj.isValid
    assert obj.minNum == 1
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum

    assert len(obj.raw) == len(mixed_entity_list)
    assert len(obj.clean) == len(mixed_entity_list)
    verifyRaw = [item in mixed_entity_list for item in obj.raw]
    verifyClean = [item in mixed_address_list for item in obj.clean]
    assert all(verifyRaw)
    assert all(verifyClean)


def test_create_ToEmail_object_with_strings(mixed_address_list, mixed_entity_list):
    """Test ability to create 'ToEmail' object using string values."""
    # Test happy path
    totNum = len(mixed_address_list)
    maxNum = totNum + 1
    obj = email.ToEmail(inList=mixed_address_list, maxNum=maxNum)
    assert obj.keyword == const.KWD_TO_EMAIL
    assert obj.isRequired
    assert obj.isValid
    assert obj.minNum == 1
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum

    assert len(obj.raw) == len(mixed_entity_list)
    assert len(obj.clean) == len(mixed_entity_list)
    verifyRaw = [item in mixed_entity_list for item in obj.raw]
    verifyClean = [item in mixed_address_list for item in obj.clean]
    assert all(verifyRaw)
    assert all(verifyClean)

    # Test 'maxNum'
    maxNum = len(mixed_address_list) - 1
    obj = email.ToEmail(inList=mixed_address_list, maxNum=maxNum)
    assert obj.minNum == 1
    assert obj.maxNum == maxNum
    assert obj.totNum == maxNum
    assert len(obj.raw) == maxNum
    assert len(obj.clean) == maxNum

    # Test 'maxNum' cannot be smaller than 'minNum'
    obj = email.ToEmail(inList=mixed_address_list, maxNum=0)
    assert obj.minNum == 1
    assert obj.maxNum == 1
    assert obj.totNum == 1

    # Test assertion that 'to' cannot be empty
    with pytest.raises(MissingAttributeError) as e:
        email.ToEmail(inList=[""], maxNum=10)
    assert e.type == MissingAttributeError
    assert "to" in e.value.args[0]

    # Test that 'to' should not be empty when not in strict mode
    obj = email.ToEmail(inList=[""], maxNum=10, strict=False)
    assert not obj.isValid  # 'valid' flag is set to 'False'
    assert obj.raw == []  # 'data' is empty list
    assert obj.clean == []


def test_create_CcEmail_object_with_entities(mixed_entity_list):
    """Test ability to create 'CcEmail' object using 'Entity' objects."""
    # Test happy path
    totNum = len(mixed_entity_list)
    maxNum = totNum + 1
    obj = email.CcEmail(inList=mixed_entity_list, maxNum=maxNum)
    assert obj.keyword == const.KWD_CC_EMAIL
    assert not obj.isRequired
    assert obj.isValid
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum
    assert len(obj.raw) == totNum
    assert len(obj.clean) == totNum


def test_create_CcEmail_object_with_strings(mixed_address_list):
    """Test ability to create 'CcEmail' object using string values."""
    # Test happy path
    totNum = len(mixed_address_list)
    maxNum = totNum + 1
    obj = email.CcEmail(inList=mixed_address_list, maxNum=maxNum)
    assert obj.keyword == const.KWD_CC_EMAIL
    assert not obj.isRequired
    assert obj.isValid
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum
    assert len(obj.raw) == totNum
    assert len(obj.clean) == totNum

    totNum = len(mixed_address_list)
    maxNum = totNum + 1
    obj = email.CcEmail(
        inList=mixed_address_list, maxNum=maxNum, keyword=const.KWD_BCC_EMAIL
    )
    assert obj.keyword == const.KWD_BCC_EMAIL
    assert not obj.isRequired
    assert obj.isValid
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum
    assert len(obj.raw) == totNum
    assert len(obj.clean) == totNum

    # Test 'maxNum'
    maxNum = len(mixed_address_list) - 1
    obj = email.CcEmail(inList=mixed_address_list, maxNum=maxNum)
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == maxNum
    assert len(obj.raw) == maxNum
    assert len(obj.clean) == maxNum

    # Test assertion that 'cc' can be empty
    obj = email.CcEmail(inList=[""], maxNum=10)
    assert obj.isValid
    assert obj.raw == []
    assert obj.clean == []


@pytest.mark.slow
def test_create_Attachments_object(new_attachment_file):
    """Test ability to create 'Attachment' object."""
    # Test happy path
    fileList = [
        new_attachment_file,
        new_attachment_file,
        new_attachment_file,
        new_attachment_file,
    ]

    totNum = len(fileList)
    maxNum = totNum + 1
    obj = email.Attachments(
        inList=fileList, inType=const.KWD_ATTACHMENTS, maxNum=maxNum
    )
    assert obj.keyword == const.KWD_ATTACHMENTS
    assert not obj.isRequired
    assert obj.isValid
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum
    assert len(obj.raw) == totNum
    assert len(obj.clean) == totNum

    obj = email.Attachments(inList=fileList, inType=const.KWD_INLINE, maxNum=maxNum)
    assert obj.keyword == const.KWD_INLINE

    # Test 'maxNum'
    maxNum = len(fileList) - 1
    obj = email.Attachments(
        inList=fileList, inType=const.KWD_ATTACHMENTS, maxNum=maxNum
    )
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == maxNum
    assert len(obj.raw) == maxNum
    assert len(obj.clean) == maxNum

    # Test assertion that 'attachments' can be empty
    obj = email.Attachments(inList=[""], inType=const.KWD_ATTACHMENTS, maxNum=10)
    assert obj.isValid
    assert obj.raw == []
    assert obj.clean == []


# from inspect import currentframe, getframeinfo
# helpers.pp(capsys, data, currentframe())
# helpers.pp(capsys, Hdrs['sql'], currentframe())
# helpers.pp(capsys, Hdrs['raw'], currentframe())
# helpers.pp(capsys, dataFName, currentframe())
# helpers.pp(capsys, tblName, currentframe())
# helpers.pp(capsys, dataOut, currentframe())
# helpers.pp(capsys, dataIn, currentframe())
