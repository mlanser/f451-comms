"""Utility functions for f451 Communications module.

This module includes several functions that are used throughout the
f451 Communications module to handle common tasks like processing lists,
parsing strings, and more.
"""
import re
from collections import ChainMap
from configparser import ConfigParser
from configparser import ExtendedInterpolation
from typing import Any
from typing import Dict
from typing import List

__all__ = [
    "is_valid_email",
    "is_valid_phone",
    "is_valid_twitter",
    "is_valid_twitter",
    "convert_attrib_str_to_list",
    "process_string_list",
    "parse_attribs",
    "convert_config_str_to_dict",
    "process_config",
    "parse_defaults",
]


def is_valid_email(inStr: str) -> bool:
    """Validate string has valid email address format."""
    return bool(
        re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", inStr)
    )


def is_valid_phone(inStr: str) -> bool:
    """Validate string has valid phone number format."""
    return bool(re.fullmatch(r"^\+[1-9]\d{1,14}$", inStr))


def is_valid_twitter(inStr: str) -> bool:
    """Validate string has valid Twitter name format."""
    return bool(re.fullmatch(r"^[A-Za-z0-9_]{1,15}$", inStr))


def process_key_value_map(
    inList: Any, keyDelim: str = ":", itemDelim: str = "|"
) -> Dict[str, Any]:
    """Process list of key-value mappings.

    The purpose of this method is to process a list with one or more key-value
    mappings and placing them into a lookup table (dict).

    Example:
        >>> myMap = process_key_value_map('key1:value1|key2:value2')
        >>> assert myMap == {'key1': 'value1', 'key2': 'value2'}

    Args:
        inList:
            Single string or list with one or more strings
        keyDelim:
            delimiter between key and value
        itemDelim:
            delimiter between key-value pairs

    Returns:
        'dict' with zero or more key-value pairs
    """
    stripChars = f"{keyDelim} "

    tmpList = (
        inList
        if isinstance(inList, list)
        else convert_attrib_str_to_list(inList, itemDelim)
    )
    outList = [
        {key.strip(): val.strip()}
        for key, val in [
            tuple(item.split(keyDelim)[:2])
            for item in tmpList
            if item.strip(stripChars) and len(item.split(keyDelim)) > 1
        ]
        if key.strip() and val.strip()
    ]
    return dict(ChainMap(*outList)) if len(outList) else {}


def convert_attrib_str_to_list(
    inStr: Any, itemDelim: str = "|", itemFmt: Any = str
) -> List[Any]:
    """Convert a given attribute string to list format.

    This method is used throughout the f451 Communications module and its purpose
    is to convert multi-value attribute strings to list format. By default, the
    output will be a list of strings. But the 'itemFmt' function can convert the
    output to a list of any type.

    Example:
        >>> myList = convert_attrib_str_to_list("item")
        >>> assert myList == ["item"]

        >>> myList = convert_attrib_str_to_list("item1|item2|item3")
        >>> assert myList == ["item1", "item2", "item3"]

        >>> myList = convert_attrib_str_to_list("item")
        >>> assert myList == ["item"]

        >>> myList = convert_attrib_str_to_list("5")
        >>> assert myList == ["5"]

        >>> myList = convert_attrib_str_to_list("5")
        >>> assert myList == ["5"]

        >>> myList = convert_attrib_str_to_list(5)
        >>> assert myList == ["5"]

        >>> myList = convert_attrib_str_to_list("1|2|3|4|5")
        >>> assert myList == ["1", "2", "3", "4", "5"]

        >>> myList = convert_attrib_str_to_list("5", "|", int)
        >>> assert myList == [5]

        >>> myList = convert_attrib_str_to_list(5, "|", int)
        >>> assert myList == [5]

        >>> myList = convert_attrib_str_to_list("1|2|3|4|5", "|", int)
        >>> assert myList == [1, 2, 3, 4, 5]

    Args:
        inStr:
            configuration string to be converted.
        itemDelim:
            item delimiter
        itemFmt:
            item (data) formatter

    Returns:
        List with zero or more attribute values
    """
    tmpList = str(inStr).split(itemDelim)
    return [itemFmt(item.strip()) for item in tmpList if item.strip()]


def convert_str_to_bool(inVal: Any) -> bool:
    """Convert string value to boolean.

    Example:
        >>> myBool = convert_str_to_bool("TRUE")
        >>> assert myBool

        >>> myBool = convert_str_to_bool("yes")
        >>> assert myBool

        >>> myBool = convert_str_to_bool("1")
        >>> assert myBool

        >>> myBool = convert_str_to_bool("F")
        >>> assert not myBool

        >>> myBool = convert_str_to_bool("no")
        >>> assert not myBool

    Args:
        inVal:
            Value to be converted.

    Returns:
        Boolean 'True' or 'False' based on input.
    """
    return (
        inVal
        if type(inVal) == bool
        else str(inVal).lower() in {"true", "1", "t", "y", "yes"}
    )


def process_string_list(
    inList: Any, prefix: str = "", suffix: str = "", spacer: str = ""
) -> str:
    """Process list of strings convert them to single string.

    This method is used throughout the f451 Communications module and its purpose
    is to process a list with one or more strings by adding prefix and suffix, and
    combining them into a single string with spaces between them.

    Args:
        inList:
            single string or list with one or more strings
        prefix:
            optional prefix for each item in the list
        suffix:
            optional suffix for each item in the list
        spacer:
            spacer to place between string items

    Returns:
        String with zero or more hashtags
    """
    if not inList:
        return ""

    stripChars = f"{prefix}{suffix}{spacer}"
    tmpList = inList if isinstance(inList, list) else convert_attrib_str_to_list(inList)
    strList = [item.strip(stripChars) for item in tmpList if item.strip(stripChars)]

    joiner = f"{suffix}{spacer}{prefix}"
    return f"{prefix}{joiner.join(strList)}{suffix}" if strList else ""


def parse_attribs(attribs: Any, key: str, default: Any = None) -> Any:
    """Retrieve value from attributes.

    This method is used throughout the f451 Communications module and its purpose
    is to retrieve a value from the 'attribs' dict which acts as a (temp) key-value
    store mechanism to supply various methods with any number of additional optional
    values. If the key cannot be found, then the method can return a default value.

    Example:
        >>> myVal = parse_attribs({"key1": "val1", "key2": "val2"}, "key1", "NOT FOUND")
        >>> assert myVal == "val1"

        >>> myVal = parse_attribs({"key1": "val1", "key2": "val2"}, "xyz", "NOT FOUND")
        >>> assert myVal == "NOT FOUND"

    Note:
        This method will only search for top-level keys. However, each key can be associated with any
        type of value including dict and list types.

    Args:
        attribs:
            dict with set of key-value pairs
        key:
            key string to find in 'attribs'
        default:
            default value to be returned if key is not found

    Returns:
        Value from 'attribs' if key is found, else 'default value
    """
    return attribs.get(key, default) if isinstance(attribs, dict) else default


def convert_config_str_to_dict(
    inStr: str, sectnDelim: str = "|", itemDelim: str = ",", keyDelim: str = ":"
) -> Dict[str, Any]:
    """Convert 'config' string to dict format.

    This method is used throughout the f451 Communications module and its purpose
    is to convert configuration strings to dict format which then can be read by ConfigParser.

    Note:
        This technique should only be used to represent a single section.

    Example:
        >>> myDict = convert_config_str_to_dict("section1|key1:val1,key2:val2")
        >>> assert myDict == {"section1": {"key1": "val1", "key2": "val2"}}

    Args:
        inStr:
            configuration string to be converted
        sectnDelim:
            section delimiter
        itemDelim:
            item delimiter
        keyDelim:
            key delimiter

    Returns:
        Configuration values in dict format

    Raises:
        ValueError: String has more than 1 section, or section label is missing,
            or there are no section items
    """
    inStrParts = inStr.split(sectnDelim, 1)
    if len(inStrParts) < 2:
        raise ValueError(f"'{inStr}' is not a valid configuration string.")

    sectnLbl = str(inStrParts[0]).strip()
    if not sectnLbl:
        raise ValueError("Section label for configuration string cannot be empty.")

    sectnItems = str(inStrParts[1]).strip()
    if not sectnItems:
        raise ValueError("Section items for configuration string cannot be empty.")

    return {
        sectnLbl: {
            k.strip(): v.strip()
            for k, v in (
                str(item).split(keyDelim, 1)
                for item in str(sectnItems).split(itemDelim)
            )
        }
    }


def process_config(inConfig: Any, force: bool = True) -> ConfigParser:
    """Process config files.

    Args:
        inConfig:
            configuration string to be converted
        force:
            section delimiter

    Returns:
        Config parser object

    Raises:
        ValueError: Invalid config data source
    """
    if isinstance(inConfig, str):
        outConfig = ConfigParser(interpolation=ExtendedInterpolation())
        outConfig.read_dict(convert_config_str_to_dict(inConfig))
    elif isinstance(inConfig, dict):
        outConfig = ConfigParser(interpolation=ExtendedInterpolation())
        outConfig.read_dict(inConfig)
    elif isinstance(inConfig, ConfigParser):
        outConfig = inConfig
    elif force:
        raise ValueError(
            f"'{type(inConfig)}' is not a valid type for configuration data sets."
        )
    else:
        outConfig = ConfigParser()

    return outConfig


def parse_defaults(inConfig: ConfigParser, sections: List[str]) -> Dict[str, Any]:
    """Parse default values.

    Args:
        inConfig:
            ConfigParser object with default data
        sections:
            list of one or more section names

    Returns:
        'dict' structure with default value(s)
    """
    outDict = {}

    for s in sections:
        if inConfig.has_section(s):
            outDict.update(dict(inConfig.items(s)))

    return outDict
