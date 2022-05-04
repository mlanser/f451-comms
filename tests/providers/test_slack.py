"""Test cases for Slack module."""
from pathlib import PurePath

import pytest
import src.f451_comms.constants as const
import src.f451_comms.providers.slack as slack
from slack_sdk import WebClient
from src.f451_comms.exceptions import InvalidAttributeError
from src.f451_comms.exceptions import MissingAttributeError

# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_TEST_MSG_ = "Hello World!"
_TEST_TO_NAME_ = "Batman"
_TEST_CHANNEL_ = "#general"
_TEST_EMOJI_ = "simple_smile"  # No need to include ':' as we add them anyway
_TEST_TITLE_ = "_TEST_TITLE_"


@pytest.fixture()
def valid_block():
    """Return valid Slack message block."""
    return {"type": "header", "text": {"type": "plain_text", "text": _TEST_MSG_}}


@pytest.fixture()
def mixed_attribs():
    """Return mixed attributes."""
    return {
        const.KWD_TO_SLACK: _TEST_TO_NAME_,
        const.KWD_TO_CHANNEL: _TEST_CHANNEL_,
        const.KWD_ICON_EMOJI: _TEST_EMOJI_,
    }


@pytest.fixture()
def slackClient(valid_settings, mocker):
    """Return mock Slack client."""
    # Disable API calls to various Slack functions
    mocker.patch.object(
        WebClient, "chat_postMessage", autospec=True, return_value={"ok": True}
    )
    mocker.patch.object(
        WebClient, "files_upload", autospec=True, return_value={"ok": True}
    )

    return slack.Slack(
        authToken=valid_settings.get(
            const.CHANNEL_SLACK, const.KWD_AUTH_TOKEN, fallback=""
        ),
        fromName=valid_settings.get(
            const.CHANNEL_SLACK, const.KWD_FROM_NAME, fallback=""
        ),
        signingSecret=valid_settings.get(
            const.CHANNEL_SLACK, const.KWD_SIGN_SECRET, fallback=""
        ),
        appToken=valid_settings.get(
            const.CHANNEL_SLACK, const.KWD_APP_TOKEN, fallback=""
        ),
    )


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
@pytest.mark.slow
def test_process_file_attachment(new_attachment_file):
    """Test ability to process file attachments."""
    # Test happy path
    fName, fContent, fTitle = slack.process_file_attachment(
        inFile=new_attachment_file,
        inTitle=_TEST_TITLE_,
    )
    assert fName == PurePath(new_attachment_file).name
    assert fTitle == _TEST_TITLE_

    fName, fContent, fTitle = slack.process_file_attachment(
        inFile=[new_attachment_file, new_attachment_file],
        inTitle=_TEST_TITLE_,
    )
    assert fName == PurePath(new_attachment_file).name
    assert fTitle == _TEST_TITLE_

    fName, fContent, fTitle = slack.process_file_attachment(
        inFile=f"{new_attachment_file}|{new_attachment_file}",
        inTitle=_TEST_TITLE_,
    )
    assert fName == PurePath(new_attachment_file).name
    assert fTitle == _TEST_TITLE_

    # Test skipping blank filenames
    fName, fContent, fTitle = slack.process_file_attachment(
        inFile=["", "", new_attachment_file],
        inTitle=_TEST_TITLE_,
    )
    assert fName == PurePath(new_attachment_file).name
    assert fTitle == _TEST_TITLE_

    # Test skipping blank and invalid filenames
    fName, fContent, fTitle = slack.process_file_attachment(
        inFile=["", "_INVALID_FILE_", "", new_attachment_file],
        inTitle=_TEST_TITLE_,
    )
    assert fName == PurePath(new_attachment_file).name
    assert fTitle == _TEST_TITLE_

    processed = slack.process_file_attachment(inFile=["", "", "_INVALID_FILE_"])
    assert processed == ("", b"", "")


@pytest.mark.slow
def test_process_media_list_strict_mode(new_attachment_file):
    """Test ability to process media files in 'strict' mode."""
    # Test assertion if file does not exist
    with pytest.raises(InvalidAttributeError) as e:
        slack.process_file_attachment(inFile=["_INVALID_FILE_"], strict=True)
    assert e.type == InvalidAttributeError
    assert "_INVALID_FILE_" in e.value.args[0]

    # Test exception if empty filename
    with pytest.raises(InvalidAttributeError) as e:
        slack.process_file_attachment(inFile=[""], strict=True)
    assert e.type == InvalidAttributeError
    assert "blank" in e.value.args[0]


def test_send_message(mocker, slackClient):
    """Test ability to send a message."""
    with pytest.raises(MissingAttributeError) as e:
        slackClient.send_message("")
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    mocker.patch.object(slack.Slack, "send_message", autospec=True)
    slackClient.send_message(_TEST_MSG_)
    slackClient.send_message.assert_called_once_with(slackClient, _TEST_MSG_)


def test_send_message_with_blocks(mocker, slackClient, valid_block):
    """Test ability to send a message with Slack message blocks."""
    with pytest.raises(MissingAttributeError) as e:
        slackClient.send_message_with_blocks([])
    assert e.type == MissingAttributeError
    assert "blank" in e.value.args[0]

    mocker.patch.object(slack.Slack, "send_message_with_blocks", autospec=True)
    slackClient.send_message_with_blocks([valid_block])
    slackClient.send_message_with_blocks.assert_called_once_with(
        slackClient, [valid_block]
    )


def test_send_message_with_file(mocker, slackClient):
    """Test ability to send a message with file attachments."""
    # with pytest.raises(ValueError) as e:
    #     slackClient.send_message('')
    # assert e.type == ValueError
    # assert 'empty' in e.value.args[0]
    #
    # with pytest.raises(CommsSlackException) as e:
    #     slackClient.send_message(_MSG_)
    # assert e.type == CommsSlackException
    #
    # mocker.patch.object(Slack, 'send_message', autospec=True)
    # slackClient.send_message(_MSG_)
    # slackClient.send_message.assert_called_once_with(slackClient, _MSG_)
    pass


# from inspect import currentframe, getframeinfo
# helpers.pp(capsys, data, currentframe())
# helpers.pp(capsys, dataHdrs['sql'], currentframe())
# helpers.pp(capsys, dataHdrs['raw'], currentframe())
# helpers.pp(capsys, dataFName, currentframe())
# helpers.pp(capsys, tblName, currentframe())
# helpers.pp(capsys, dataOut, currentframe())
# helpers.pp(capsys, dataIn, currentframe())
