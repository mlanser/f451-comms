"""Test cases for 'Mailgun' provider module."""
import pytest
import src.f451_comms.constants as const
import src.f451_comms.providers.mailgun as mailgun
from src.f451_comms.exceptions import MissingAttributeError


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_DEFAULT_MSG_ = "Hello World!"
_DEFAULT_TAG_ = "safe"
_DEFAULT_TEST_STRING_ = "_TEST_STRING_"
_DEFAULT_TEST_NAME_ = "Batman"
_DEFAULT_TEST_EMAIL_ = "batman@example.com"
_DEFAULT_TEST_SUBJECT_ = "_TEST_SUBJECT_"


@pytest.fixture()
def mixed_tag_list():
    """Return mixed tag strings."""
    return [_DEFAULT_TAG_, "äpple", "nötter", "blåbär", "three", "four"]


@pytest.fixture()
def mixed_attribs():
    """Return mixed attributes."""
    return {
        const.KWD_FROM_NAME: _DEFAULT_TEST_NAME_,
        const.KWD_TO_EMAIL: _DEFAULT_TEST_EMAIL_,
        const.KWD_SUBJECT: _DEFAULT_TEST_SUBJECT_,
        const.KWD_TAGS: _DEFAULT_TEST_STRING_,
        const.KWD_TRACKING: True,
        const.KWD_TESTMODE: True,
    }


@pytest.fixture()
def mailgunClient(valid_settings, mixed_attribs):
    """Return Nailgun client."""
    return mailgun.Mailgun(
        apiKey=valid_settings.get(
            const.CHANNEL_MAILGUN, const.KWD_PRIV_KEY, fallback=""
        ),
        fromDomain=valid_settings.get(
            const.CHANNEL_MAILGUN, const.KWD_FROM_DOMAIN, fallback=""
        ),
        **mixed_attribs,
    )


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_static_process_tag_list(mixed_tag_list):
    """Verify ability to process tag list."""
    # Test happy path
    totNum = len(mixed_tag_list)
    maxNum = totNum + 1
    processed = mailgun.process_tag_list(
        inList=mixed_tag_list,
        maxNum=maxNum,
        minTagLen=mailgun._MIN_TAG_LEN_,
        maxTagLen=mailgun._MAX_TAG_LEN_,
    )
    assert len(processed) == len(mixed_tag_list)

    # Test blank items
    processed = mailgun.process_tag_list(
        inList=["one", "", "", "three"],
        maxNum=10,
        minTagLen=mailgun._MIN_TAG_LEN_,
        maxTagLen=mailgun._MAX_TAG_LEN_,
    )
    assert len(processed) == 2

    # Test max items
    processed = mailgun.process_tag_list(
        inList=["one", "two", "three", "four"],
        maxNum=3,
        minTagLen=mailgun._MIN_TAG_LEN_,
        maxTagLen=mailgun._MAX_TAG_LEN_,
    )
    assert len(processed) == 3

    # Test min/max chars
    processed = mailgun.process_tag_list(
        inList="abc123",
        maxNum=10,
        minTagLen=1,
        maxTagLen=3,
    )
    assert len(processed[0]) == 3
    processed = mailgun.process_tag_list(
        inList=["abc123", "a", "ab"],
        maxNum=10,
        minTagLen=3,
        maxTagLen=10,
    )
    assert len(processed[0]) == 6

    # Test 'ascii' conversion
    processed = mailgun.process_tag_list(
        inList="äpple", maxNum=10, minTagLen=3, maxTagLen=10
    )
    assert processed[0] == "?pple"


def test_create_Tags_object(mixed_tag_list):
    """Verify ability to creata a 'Tag' object."""
    # Test happy path
    totNum = len(mixed_tag_list)
    maxNum = totNum + 1
    obj = mailgun.Tags(
        inList=mixed_tag_list,
        maxNum=maxNum,
        minLen=mailgun._MIN_TAG_LEN_,
        maxLen=mailgun._MAX_TAG_LEN_,
    )
    assert obj.keyword == const.KWD_TAGS
    assert not obj.isRequired
    assert obj.isValid
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum
    assert len(obj.raw) == totNum
    assert isinstance(obj.clean, list)

    # Test 'maxNum'
    maxNum = len(mixed_tag_list) - 1
    obj = mailgun.Tags(
        inList=mixed_tag_list,
        maxNum=maxNum,
        minLen=mailgun._MIN_TAG_LEN_,
        maxLen=mailgun._MAX_TAG_LEN_,
    )
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == maxNum
    assert len(obj.raw) == maxNum
    assert len(obj.clean) == maxNum

    # Test assertion that 'tags' can be empty
    obj = mailgun.Tags(
        inList=[""],
        maxNum=10,
        minLen=mailgun._MIN_TAG_LEN_,
        maxLen=mailgun._MAX_TAG_LEN_,
    )
    assert obj.isValid
    assert obj.raw == []
    assert obj.clean == []


def test_create_RecipientData_object(valid_attribs_dict):
    """Verify ability to creata a 'RecipientData' object."""
    # Test happy path
    totNum = len(valid_attribs_dict.items())
    maxNum = totNum + 1
    obj = mailgun.RecipientData(inData=valid_attribs_dict, maxNum=maxNum)
    assert obj.keyword == const.KWD_RECIPIENT_DATA
    assert not obj.isRequired
    assert obj.isValid
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum
    assert len(obj.raw.items()) == totNum
    assert isinstance(obj.clean, str)
    assert len(obj.clean) > 1

    # Test 'maxNum'
    maxNum = len(valid_attribs_dict.items()) - 1
    obj = mailgun.RecipientData(inData=valid_attribs_dict, maxNum=maxNum)
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == maxNum
    assert len(obj.raw.items()) == maxNum

    # Test assertion that 'recipient_data' can be empty
    obj = mailgun.RecipientData(inData={}, maxNum=10)
    assert obj.isValid
    assert obj.raw == {}
    assert obj.clean == "{}"


def test_create_Mailgun_object(mailgunClient, valid_settings, mixed_attribs):
    """Verify ability to creata a 'Mailgun' object."""
    client = mailgunClient
    assert client.serviceType == const.SRV_TYPE_EMAIL
    assert client.serviceName == mailgun._SRV_PROVIDER_
    assert client.configSection == mailgun._SRV_CONFIG_SCTN_

    client = mailgun.Mailgun(
        valid_settings.get(const.CHANNEL_MAILGUN, const.KWD_PRIV_KEY, fallback=""),
        valid_settings.get(const.CHANNEL_MAILGUN, const.KWD_FROM_DOMAIN, fallback=""),
        **mixed_attribs,
    )
    assert len(client.defaultTo) == 1
    assert client.defaultTo[0].email == _DEFAULT_TEST_EMAIL_
    assert client.defaultSubject == _DEFAULT_TEST_SUBJECT_
    assert client.defaultTags == [_DEFAULT_TEST_STRING_]
    assert client._tracking
    assert client._testmode


def test_send_message(mocker, mailgunClient):
    """Verify ability to send message."""
    with pytest.raises(MissingAttributeError) as e:
        mailgunClient.send_message("")
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    attribs = {
        const.KWD_SUBJECT: "",
        const.KWD_TO_EMAIL: "one@example.com",
    }
    with pytest.raises(MissingAttributeError) as e:
        mailgunClient.send_message(_DEFAULT_MSG_, **attribs)
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    attribs = {
        const.KWD_SUBJECT: _DEFAULT_MSG_,
        const.KWD_TO_EMAIL: "",
    }
    with pytest.raises(MissingAttributeError) as e:
        mailgunClient.send_message(_DEFAULT_MSG_, **attribs)
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    attribs = {
        const.KWD_SUBJECT: _DEFAULT_MSG_,
        const.KWD_TO_EMAIL: "one@example.com",
        const.KWD_HTML: f"<html>{_DEFAULT_MSG_}</html>",
        const.KWD_RECIPIENT_DATA: {
            "one@example.com": {"first": "First", "last": "Person", "uuid": "12345567"}
        },
        const.KWD_TESTMODE: False,
    }

    mocker.patch.object(mailgunClient, "send_message", autospec=True)
    mailgunClient.send_message(_DEFAULT_MSG_, **attribs)
    mailgunClient.send_message.assert_called_once()


@pytest.mark.slow
def test_send_message_extensive(mocker, mailgunClient, new_attachment_file):
    """Verify ability to send message with more data."""
    attribs = {
        const.KWD_SUBJECT: _DEFAULT_MSG_,
        const.KWD_TO_EMAIL: ["one@example.com", "two@example.com"],
        const.KWD_CC_EMAIL: "cc@example.com",
        const.KWD_BCC_EMAIL: ["bcc@example.com", "", "bcc2@example.com"],
        const.KWD_TAGS: ["äpple", "nötter", "", "blåbär", "three", "four"],
        const.KWD_HTML: f"<html>{_DEFAULT_MSG_}</html>",
        const.KWD_ATTACHMENTS: new_attachment_file,
        const.KWD_INLINE: new_attachment_file,
        const.KWD_RECIPIENT_DATA: {
            "one@example.com": {"first": "First", "last": "Person", "uuid": "12345567"},
            "two@example.com": {"first": "Second", "last": "Human", "uuid": "98765443"},
        },
        const.KWD_TESTMODE: False,
    }

    mockMailgunClient = mailgunClient
    mocker.patch.object(mockMailgunClient, "send_message", autospec=True)
    mailgunClient.send_message(_DEFAULT_MSG_, **attribs)
    mailgunClient.send_message.assert_called_once()


# from inspect import currentframe, getframeinfo
# helpers.pp(capsys, data, currentframe())
