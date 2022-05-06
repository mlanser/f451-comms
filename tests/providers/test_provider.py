"""Test cases for the generic 'provider' (base class) module."""
import pytest
import src.f451_comms.constants as const
import src.f451_comms.providers.provider as provider
from src.f451_comms.exceptions import CommunicationsError
from src.f451_comms.exceptions import InvalidAttributeError


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
@pytest.mark.slow
def test_verify_file(new_attachment_file):
    """Test ability to verify that a given file exists."""
    # Test happy path
    assert provider.verify_file(new_attachment_file, True)

    # Test sad paths ;-)
    with pytest.raises(InvalidAttributeError) as e:
        provider.verify_file("_INVALID_FILE_", True)
    assert e.type == InvalidAttributeError
    assert "_INVALID_FILE_" in e.value.args[0]

    with pytest.raises(InvalidAttributeError) as e:
        provider.verify_file("", True)
    assert e.type == InvalidAttributeError
    assert "blank" in e.value.args[0]

    assert provider.verify_file(new_attachment_file, False)
    assert not provider.verify_file("_INVALID_FILE_", False)
    assert not provider.verify_file("", False)


@pytest.mark.slow
def test_process_media_list(new_attachment_file):
    """Test ability to process a list of filenames."""
    # Test happy path
    processed = provider.process_media_list(
        inList=[new_attachment_file, new_attachment_file]
    )
    assert len(processed) == 2

    processed = provider.process_media_list(
        inList=f"{new_attachment_file}|{new_attachment_file}"
    )
    assert len(processed) == 2

    # Test max num media files
    processed = provider.process_media_list(
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
    processed = provider.process_media_list(
        inList=[new_attachment_file, "", new_attachment_file]
    )
    assert len(processed) == 2

    # Test skipping blank and invalid filenames
    processed = provider.process_media_list(
        inList=[new_attachment_file, "", "_INVALID_FILE_"]
    )
    assert len(processed) == 1

    processed = provider.process_media_list(inList=["", "", "_INVALID_FILE_"])
    assert processed == []


@pytest.mark.slow
def test_process_media_list_strict_mode(new_attachment_file):
    """Test ability to process a list of filenames in 'strict' mode."""
    # Test assertion if file does not exist
    with pytest.raises(InvalidAttributeError) as e:
        provider.process_media_list(inList=["_INVALID_FILE_"], strict=True)
    assert e.type == InvalidAttributeError
    assert "_INVALID_FILE_" in e.value.args[0]

    # Test exception if empty filename
    with pytest.raises(InvalidAttributeError) as e:
        provider.process_media_list(inList=[""], strict=True)
    assert e.type == InvalidAttributeError
    assert "blank" in e.value.args[0]


@pytest.mark.slow
def test_create_Media_object(new_attachment_file):
    """Test ability to create a 'Media' object."""
    # Test happy path
    fileList = [
        new_attachment_file,
        new_attachment_file,
        new_attachment_file,
        new_attachment_file,
    ]

    totNum = len(fileList)
    maxNum = totNum + 1
    obj = provider.Media(inList=fileList, maxNum=maxNum)
    assert obj.keyword == const.KWD_MEDIA
    assert not obj.isRequired
    assert obj.isValid
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == totNum
    assert len(obj.raw) == totNum
    assert len(obj.clean) == totNum

    # Test 'maxNum'
    maxNum = len(fileList) - 1
    obj = provider.Media(inList=fileList, maxNum=maxNum)
    assert obj.minNum == 0
    assert obj.maxNum == maxNum
    assert obj.totNum == maxNum
    assert len(obj.raw) == maxNum
    assert len(obj.clean) == maxNum

    # Test assertion that 'media' can be empty
    obj = provider.Media(inList=[""], maxNum=10)
    assert obj.isValid
    assert obj.raw == []
    assert obj.clean == []


def test_create_Response_object():
    """Test ability to create a 'Response' object."""
    resp = provider.Response(
        status="OK",
        provider="TEST",
        data="TEST DATA",
    )
    assert resp.isOK


def test_create_Response_object_with_errors():
    """Test ability to create a 'Response' object with errors."""
    resp = provider.Response(
        status="OK", provider="TEST", data="TEST DATA", errors=["ERROR 1"]
    )
    assert not resp.isOK
    with pytest.raises(CommunicationsError) as e:
        resp.raise_on_errors()
    assert e.type == CommunicationsError
    assert "ERROR 1" in e.value.args[0]


def test_pretty_print_response_records(capsys):
    """Test ability to create a 'Response' object with errors."""
    valStatus = "OK"
    valProvider = "TEST PROVIDER"

    resp = provider.Response(
        status=valStatus,
        provider=valProvider,
        data="TEST DATA",
    )

    provider.pretty_print_response_records(resp)
    captured = capsys.readouterr()
    result = captured.out
    assert valStatus in result.upper()
    assert valProvider in result.upper()


# from inspect import currentframe, getframeinfo
# helpers.pp(capsys, data, currentframe())
