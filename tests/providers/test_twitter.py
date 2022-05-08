"""Test cases for the Twitter module."""
import uuid

import pytest
import tweepy

import f451_comms.constants as const
import f451_comms.providers.provider as provider
import f451_comms.providers.twitter as twitter
from f451_comms.entity import Entity
from f451_comms.exceptions import CommunicationsError
from f451_comms.exceptions import MissingAttributeError

# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_TEST_MSG_ = "Hello World!"
_TEST_USER_ = "@twitter"
_TEST_USER_ID_ = "123456789"
_TEST_RESP_ = "_TEST_RESPONSE_"

_VALID_NAME_STRING_ = "one|two|three"
_VALID_NAME_LIST_ = ["one", "two", "three"]
_VALID_ENTITY_LIST_ = [
    Entity(twitter="one"),
    Entity(twitter="two"),
    Entity(twitter="three"),
]


@pytest.fixture
def fake_filesystem(fs):  # pylint:disable=invalid-name
    """Initialize fake file system.

    Note: Variable name 'fs' causes a pylint warning. Provide a longer name
    acceptable to pylint for use in tests.
    """
    yield fs


@pytest.fixture()
def mixed_name_list():
    """Return valid name list."""
    return _VALID_NAME_LIST_


@pytest.fixture()
def mixed_entity_list():
    """Return 'Entity' list."""
    return [Entity(twitter=item) for item in _VALID_NAME_LIST_]


class MockTwitter(provider.Provider):
    """Mock Twitter client object."""

    def __init__(self, validCreds):
        super().__init__(
            const.SRV_TYPE_FORUMS, twitter.SRV_PROVIDER, twitter.SRV_CONFIG_SCTN
        )
        self._isValidCreds = validCreds
        self._api = None

    def _default_test_response(self):
        """Mock function."""
        return self._make_response(
            data={"test_resp": _TEST_RESP_},
            response=None,
            errors=None,
        )

    def get_user_id(self, usr, strict):
        """Mock function."""
        if not self._isValidCreds:
            raise CommunicationsError(
                errors=["000"], message="Invalid Twitter credentials!"
            )
        return _TEST_USER_ID_

    def send_status_update(self, msg, **kwargs):
        """Mock function."""
        if not self._isValidCreds:
            raise CommunicationsError(
                errors=["000"], message="Invalid Twitter credentials!"
            )
        return [self._default_test_response()]

    def send_dm(self, msg, **kwargs):
        """Mock function."""
        if not self._isValidCreds:
            raise CommunicationsError(
                errors=["000"], message="Invalid Twitter credentials!"
            )
        return [self._default_test_response()]

    def send_message(self, msg, **kwargs):
        """Mock function."""
        if not self._isValidCreds:
            raise CommunicationsError(
                errors=["000"], message="Invalid Twitter credentials!"
            )
        return [self._default_test_response()]


class MockMedia:
    """Mock media object."""

    def __init__(self, mediaID=None):
        self.media_id = str(mediaID) if mediaID is not None else uuid.uuid4().hex


class MockUser:
    """Mock user object."""

    def __init__(self, userID=None):
        self.id_str = str(userID) if userID is not None else uuid.uuid4().hex


@pytest.fixture()
def invalidCredsTwitterClient():
    """Set up 'broken' mock Twitter client."""
    return MockTwitter(False)


@pytest.fixture()
def twitterClient(valid_settings, mocker):
    """Set up mock Twitter client."""
    # Disable API calls to verify Twitter 'creds', etc.
    mocker.patch.object(
        tweepy.API, "verify_credentials", autospec=True, return_value=True
    )
    mocker.patch.object(
        tweepy.API, "media_upload", autospec=True, return_value=MockMedia()
    )
    mocker.patch.object(tweepy.API, "get_user", autospec=True, return_value=MockUser())

    return twitter.Twitter(
        usrKey=valid_settings.get(
            const.CHANNEL_TWITTER, const.KWD_USER_KEY, fallback=""
        ),
        usrSecret=valid_settings.get(
            const.CHANNEL_TWITTER, const.KWD_USER_SECRET, fallback=""
        ),
        authToken=valid_settings.get(
            const.CHANNEL_TWITTER, const.KWD_AUTH_TOKEN, fallback=""
        ),
        authSecret=valid_settings.get(
            const.CHANNEL_TWITTER, const.KWD_AUTH_SECRET, fallback=""
        ),
    )


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
@pytest.mark.parametrize(
    "testData", [_VALID_NAME_STRING_, _VALID_NAME_LIST_, _VALID_ENTITY_LIST_]
)
def test_process_at_list(twitterClient, testData):
    """Verify ability to process '@' lists."""
    result = twitterClient._process_at_list(testData)
    assert "@one" in result
    assert "@two" in result
    assert "@three" in result


@pytest.mark.parametrize(
    "testData",
    [
        "",
        "|",
        "||",
        [],
        ["", ""],
        Entity(name="one"),
        [Entity(name="one"), Entity(slack="two")],
    ],
)
def test_process_at_list_return_empty(twitterClient, testData):
    """Verify ability to handle invalid/empty '@' lists."""
    result = twitterClient._process_at_list(testData)
    assert not result


@pytest.mark.parametrize(
    "testData", ["one", _VALID_NAME_STRING_, _VALID_NAME_LIST_, _VALID_ENTITY_LIST_]
)
def test_process_recipient_list(twitterClient, testData):
    """Verify ability to process recipient lists."""
    result = twitter.process_recipient_list(testData, 10)
    assert len(result) >= 1
    assert isinstance(result[0], Entity)
    assert result[0].twitter in _VALID_NAME_LIST_


@pytest.mark.parametrize(
    "testData",
    [
        "",
        "|",
        "||",
        [],
        ["", ""],
        Entity(name="one"),
        [Entity(name="one"), Entity(slack="two")],
    ],
)
def test_process_recipient_list_return_empty(twitterClient, testData):
    """Verify ability to handle empty/invalid recipient lists."""
    result = twitter.process_recipient_list(testData, 10)
    assert not result


@pytest.mark.slow
def test_upload_media(twitterClient):
    """Test ability to upload media."""
    client = twitterClient

    val = client._upload_media(["tests/test_media/test-image-small.gif"], 1)
    assert len(val) == 1

    val = client._upload_media(
        [
            "tests/test_media/test-image-small.gif",
            "tests/test_media/test-image-small.jpg",
            "tests/test_media/test-image-small.png",
            "tests/test_media/test-image-small.tiff",
        ],
        4,
    )
    assert len(val) == 4

    val = client._upload_media(
        [
            "tests/test_media/test-image-small.gif",
            "tests/test_media/test-image-small.jpg",
            "tests/test_media/test-image-small.png",
            "",
        ],
        4,
    )
    assert len(val) == 3

    val = client._upload_media(
        [
            "tests/test_media/test-image-small.gif",
            "tests/test_media/test-image-small.jpg",
            "tests/test_media/test-image-small.png",
        ],
        2,
    )
    assert len(val) == 2


def test_upload_media_fails_or_return_empty(twitterClient):
    """Verify failing to upload media."""
    client = twitterClient

    with pytest.raises(FileNotFoundError) as e:
        client._upload_media(["_INVALID_FILE_"], 1, True)
    assert e.type == FileNotFoundError

    with pytest.raises(FileNotFoundError) as e:
        client._upload_media([""], 1, True)
    assert e.type == FileNotFoundError

    val = client._upload_media(["_INVALID_FILE_"], 1, False)
    assert val == []

    val = client._upload_media([""], 1, False)
    assert val == []

    val = client._upload_media([], 1, False)
    assert val == []

    val = client._upload_media(["tests/test_media/test-image-small.gif"], 0, False)
    assert val == []

    val = client._upload_media([" "], 1, False)
    assert val == []


def test_make_msg_content(twitterClient, invalidCredsTwitterClient):
    """Test ability to create Twitter message."""
    client = twitterClient

    val = client._make_msg_content(_TEST_MSG_, ["batman", "robin"], ["apple", "banana"])
    assert val == "@batman @robin Hello World! #apple #banana"

    val = client._make_msg_content(_TEST_MSG_, "batman|robin", "apple|banana")
    assert val == "@batman @robin Hello World! #apple #banana"

    val = client._make_msg_content(_TEST_MSG_, "@batman|robin", "apple|#banana")
    assert val == "@batman @robin Hello World! #apple #banana"

    val = client._make_msg_content(_TEST_MSG_, "batman")
    assert val == "@batman Hello World!"

    val = client._make_msg_content(_TEST_MSG_, "", "apple")
    assert val == "Hello World! #apple"


def test_get_user_id(mocker, twitterClient, invalidCredsTwitterClient: MockTwitter):
    """Test ability to get Twitter user IDs."""
    # We have disabled API calls for Twitter 'creds' check, and we therefore need
    # to set the object '_isValidCreds' attribute to 'False' to verify that 'send_message'
    # always does a 'creds' check first
    with pytest.raises(CommunicationsError) as e:
        invalidCredsTwitterClient.get_user_id(_TEST_USER_, True)
    assert e.type == CommunicationsError
    assert "000" in e.value.args[0]

    mocker.patch.object(twitterClient, "get_user_id", autospec=True)
    twitterClient.get_user_id(_TEST_USER_, True)
    twitterClient.get_user_id.assert_called_once_with(_TEST_USER_, True)


def test_send_status_update(
    mocker, twitterClient, invalidCredsTwitterClient: MockTwitter
):
    """Test ability to send Twitter updates."""
    # We have disabled API calls for Twitter 'creds' check, and we therefore need
    # to set the object '_isValidCreds' attribute to 'False' to verify that 'send_message'
    # always does a 'creds' check first
    with pytest.raises(CommunicationsError) as e:
        invalidCredsTwitterClient.send_message("")
    assert e.type == CommunicationsError
    assert "000" in e.value.args[0]

    # Verify 'empty msg' check, etc.
    with pytest.raises(MissingAttributeError) as e:
        twitterClient.send_message("")
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    mocker.patch.object(twitterClient, "send_status_update", autospec=True)
    twitterClient.send_message(_TEST_MSG_, **{const.KWD_METHOD_DM: False})
    twitterClient.send_status_update.assert_called_once_with(
        _TEST_MSG_, **{const.KWD_METHOD_DM: False}
    )


def test_send_dm(mocker, twitterClient, invalidCredsTwitterClient: MockTwitter):
    """Test ability to send Twitter DMs."""
    # We have disabled API calls for Twitter 'creds' check, and we therefore need
    # to set the object '_isValidCreds' attribute to 'False' to verify that 'send_message'
    # always does a 'creds' check first
    with pytest.raises(CommunicationsError) as e:
        invalidCredsTwitterClient.send_message("")
    assert e.type == CommunicationsError
    assert "000" in e.value.args[0]

    # Verify 'empty msg' check, etc.
    with pytest.raises(MissingAttributeError) as e:
        twitterClient.send_message("")
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    mocker.patch.object(twitterClient, "send_dm", autospec=True)
    twitterClient.send_message(_TEST_MSG_, **{const.KWD_METHOD_DM: True})
    twitterClient.send_dm.assert_called_once_with(
        _TEST_MSG_, **{const.KWD_METHOD_DM: True}
    )


def test_send_message(mocker, twitterClient):
    """Test ability to send a message."""
    # Verify 'empty msg' check, etc.
    with pytest.raises(MissingAttributeError) as e:
        twitterClient.send_message("")
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    # Verify 'method' attribute switch
    mocker.patch.object(twitterClient, "send_status_update", autospec=True)
    mocker.patch.object(twitterClient, "send_dm", autospec=True)

    twitterClient.send_message(_TEST_MSG_, **{const.KWD_METHOD_DM: False})
    twitterClient.send_status_update.assert_called_once_with(
        _TEST_MSG_, **{const.KWD_METHOD_DM: False}
    )

    twitterClient.send_message(_TEST_MSG_, **{const.KWD_METHOD_DM: True})
    twitterClient.send_dm.assert_called_once_with(
        _TEST_MSG_, **{const.KWD_METHOD_DM: True}
    )


def test_create_ToTwitter_object(mixed_name_list, mixed_entity_list):
    """Test ability to create a 'ToTwitter' object."""
    # Test happy path
    totNum = len(mixed_name_list)
    maxNum = totNum + 1
    obj = twitter.ToTwitter(inList=mixed_name_list, maxNum=maxNum)
    assert obj.keyword == const.KWD_TO_TWITTER
    assert obj.isRequired
    assert obj.isValid
    assert obj.minNum == 1
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum
    verifyRaw = [item in mixed_entity_list for item in obj.raw]
    verifyClean = [item in mixed_name_list for item in obj.clean]
    assert all(verifyRaw)
    assert all(verifyClean)

    # Test 'maxNum'
    maxNum = len(mixed_name_list) - 1
    obj = twitter.ToTwitter(inList=mixed_name_list, maxNum=maxNum)
    assert obj.minNum == 1
    assert obj.maxNum == maxNum
    assert obj.totNum == maxNum
    assert len(obj.raw) == maxNum
    assert len(obj.clean) == maxNum

    # Test 'maxNum' cannot be smaller than 'minNum'
    obj = twitter.ToTwitter(inList=mixed_name_list, maxNum=0)
    assert obj.minNum == 1
    assert obj.maxNum == 1
    assert obj.totNum == 1

    # Test assertion that 'to' cannot be empty
    with pytest.raises(MissingAttributeError) as e:
        twitter.ToTwitter(inList=[""], maxNum=10)
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    # Test that 'to' should not be empty when not in strict mode
    obj = twitter.ToTwitter(inList=[""], maxNum=10, strict=False)
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
