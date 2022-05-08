"""Twitter class for f451 Communications module.

This module adds an abstraction layer to the Tweepy Twitter API package and the main
purpose is to provide a standard interface for some core methods for sending Twitter
status updates and DMs to specific recipients.

Note:
    This module assumes that we have an active Twitter developer account.

Note:
    We use Twitter API v1.1 for all Tweets as the new Twitter API v2 does not yet
    support media uploads.
"""
import logging
import pprint
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import tweepy

import f451_comms.constants as const
import f451_comms.providers.provider as provider
import f451_comms.utils as utils
from f451_comms.entity import dedupe_by_attribute
from f451_comms.entity import Entity
from f451_comms.entity import process_entity_list_by_key
from f451_comms.exceptions import CommunicationsError
from f451_comms.exceptions import MissingAttributeError
from f451_comms.processor import AttributeProcessor

# =========================================================
#          G L O B A L S   A N D   H E L P E R S
# =========================================================
SRV_CONFIG_SCTN: str = "f451_twitter"
SRV_PROVIDER: str = "Twitter"

_VALID_IMG_FMTS_: List[str] = ["jpeg", "png", "gif", "webp"]

_MAX_RECIPIENTS_: int = 100  # Max number of DM recipients
_MAX_TWEET_LEN_: int = 280  # Max char len for Tweets
_MAX_DM_LEN_: int = 10000  # Max char len for DMs

_MAX_IMG_SIZE_: int = 5  # Max image size in MB
_MAX_VID_SIZE_: int = 15  # Max video/anim GIF size in MB

_MAX_NUM_IMG_: int = 4  # Max 4 images allowed ...
_MAX_NUM_VID_: int = 1  # ... max 1 video or anim GIF

_MAX_NUM_DM_MEDIA_: int = 1  # Max 1 image/video allowed for DMs

log = logging.getLogger()
pp = pprint.PrettyPrinter(indent=4)


# =========================================================
#       T W I T T E R   U T I L I T Y    C L A S S E S
# =========================================================
class ToTwitter(AttributeProcessor):
    """Processor class for recipient ('to') Twitter name lists.

    This class is only used for DM recipients. For normal status updates,
    'to'-lists are simply converted to '@'-lists.

    Attributes:
        inList:
            Single Twitter name (string) or list with one or more Twitter names
        maxNum:
            Max number of Twitter names in list
        strict:
            If 'True' then exception is raised if Twitter names list is empty

    Raises:
        MissingAttributeError: 'strict' mode and list of Twitter names is empty
    """

    def __init__(self, inList: Any, maxNum: int, strict: bool = True) -> None:
        super().__init__(
            keyword=const.KWD_TO_TWITTER,
            required=const.ATTR_REQUIRED,
        )
        self._data: List[Entity] = []
        self._strict = strict
        self._minNum = 1  # we require min 1 Twitter DM recipient
        self.maxNum = maxNum
        self.data = inList

    @property
    def data(self) -> List[Entity]:
        """Return 'data' property."""
        return self._data

    @data.setter
    def data(self, inList: Any) -> None:
        """Set 'data' property."""
        tmpList = process_recipient_list(inList, self._maxNum)

        if len(tmpList) < self._minNum:
            log.error("Blank DM recipient.")
            self._data = []
            self._valid = False
            if self._strict:
                raise MissingAttributeError("DM recipient cannot be blank.")
        else:
            self._data = tmpList
            self._valid = True

    @property
    def minNum(self) -> int:
        """Return 'minNum' property."""
        return self._minNum

    @property
    def maxNum(self) -> int:
        """Return 'maxNum' property."""
        return self._maxNum

    @maxNum.setter
    def maxNum(self, val: int) -> None:
        """Set 'maxNum' property."""
        # 'max' num cannot be smaller than 'min'
        self._maxNum = max(self._minNum, val)

    @property
    def totNum(self) -> int:
        """Return 'totNum' property."""
        return len(self._data)

    @property
    def raw(self) -> List[Entity]:
        """Return 'raw' list of 'Entity' objects."""
        return self._data

    @property
    def clean(self) -> List[str]:
        """Return 'clean' list of Twitter name strings."""
        return [item.twitter for item in self._data]


# =========================================================
#        M A I N   C L A S S   D E F I N I T I O N
# =========================================================
class Twitter(provider.Provider):
    """Twitter class for f451 Communications module.

    Use this support class to send messages via Twilio.

    Attributes:
        usrKey:
            Twitter user/consumer key
        usrSecret:
            Twitter user/consumer secret
        authToken:
            Twitter auth/access token
        authSecret:
            Twitter auth/access token secret
    """

    def __init__(
        self,
        usrKey: str,
        usrSecret: str,
        authToken: str,
        authSecret: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(const.SRV_TYPE_FORUMS, SRV_PROVIDER, SRV_CONFIG_SCTN)
        self._isValidCreds: bool = False
        self._client: Any = None
        self.client = (usrKey, usrSecret, authToken, authSecret)
        self.defaultTags = kwargs.get(const.KWD_TAGS, "")
        self.defaultTo = kwargs.get(const.KWD_TO, kwargs.get(const.KWD_TO_TWITTER, ""))

    @property
    def client(self) -> Any:
        """Return 'totNum' property."""
        return self._client

    @client.setter
    def client(self, inAuth: Tuple[str, str, str, str]) -> None:
        usrKey, usrSecret, authToken, authSecret = inAuth

        try:
            log.debug("Verifying Twitter credentials")
            auth = tweepy.OAuth1UserHandler(usrKey, usrSecret)
            auth.set_access_token(authToken, authSecret)
            api = tweepy.API(auth, wait_on_rate_limit=True)

            api.verify_credentials()
            self._isValidCreds = True
            self._client = api

        except tweepy.errors.TweepyException as e:
            log.error("Invalid Twitter credentials")
            raise CommunicationsError("Invalid Twitter credentials") from e

    @property
    def defaultTo(self) -> List[Entity]:
        """Return 'defaultTo' property."""
        return self._defaultTo

    @defaultTo.setter
    def defaultTo(self, val: Any) -> None:
        """Set 'defaultTo' property."""
        if isinstance(val, Entity):
            self._defaultTo = [val]
        elif const.DELIM_VAL in val and const.DELIM_STD in val:
            self._defaultTo = [Entity(**utils.process_key_value_map(val))]
        else:
            self._defaultTo = process_recipient_list(val, _MAX_RECIPIENTS_)

    @property
    def defaultTags(self) -> List[str]:
        """Return 'defaultTags' property."""
        return self._defaultTags

    @defaultTags.setter
    def defaultTags(self, val: Any) -> None:
        """Set 'defaultTags' property."""
        self._defaultTags = utils.convert_attrib_str_to_list(val)

    @property
    def timeline(self) -> Any:
        """Return 'timeline' property."""
        return self._client.home_timeline() if self._client else None

    @property
    def isValidCreds(self) -> bool:
        """Return 'isValidCreds' property."""
        return self._isValidCreds

    @staticmethod
    def _process_at_list(inList: Any) -> str:
        """Create string with list of '@' usernames.

        This method can take a single name string, single Entity, or list of
        either and create a string with one or more '@' names.

        Args:
            inList:
                Single name string, list of names, entity, or list of entities

        Returns:
            String with zero or more '@' names
        """
        if isinstance(inList, Entity) or (
            isinstance(inList, list)
            and all(isinstance(item, Entity) for item in inList)
        ):
            return process_entity_list_by_key(inList, const.KWD_TWITTER, "@", " ")
        else:
            return utils.process_string_list(inList, "@", " ")

    def _process_dm_list(self, inList: List[str]) -> List[Tuple[str, str]]:
        """Get Twitter IDs for a set of given Twitter names.

        We always want to create a list of recipients even if there is only 1 DM recipient. This
        allows us to easily send DMs to one more recipients with a simple loop.

        Args:
            inList:
                List of Twitter name strings

        Returns:
            List of tuples with recipient Twitter names and IDs.
        """
        return [
            (dmName, self.get_user_id(dmName, True))
            for dmName in inList
            if dmName.strip()
        ]

    def _make_msg_content(
        self, msg: str, atList: Any = None, tagList: Any = None
    ) -> str:
        """Assemble Twitter message/post.

        This method will process any name in 'toList' and any tags in 'tagList'
        and sandwich the post message in between so the final message string
        looks as follows:

            '@name Hello world! #someTag'

        Args:
            msg:
                Message string
            atList:
                Single name string, list of names, entity, or list of entities
            tagList:
                Single tag string or list of tags

        Returns:
            Final message string
        """
        # Do we need to '@' somebody and/or do we have hashtags?
        atList = self._process_at_list(atList)
        tagList = utils.process_string_list(tagList, "#", " ")

        # Do some 'assemble magic' and cut off at max len
        return (
            (" ".join([atList.strip(), msg.strip(), tagList.strip()])).strip()[
                :_MAX_TWEET_LEN_
            ]
        ).strip()

    def _make_comm_error(
        self, msg: str, data: Any = None, erc: Any = None
    ) -> Dict[str, Any]:
        return {
            "provider": self._srvName,
            "data": data,
            "errors": [str(erc)] if erc else None,
            "response": None,
            "message": msg,
        }

    def _upload_media(
        self,
        inList: List[str],
        maxMedia: int = _MAX_NUM_IMG_,
        strict: bool = False,
    ) -> List[str]:
        """Upload media item to Twitter.

        This method will verify that an image files have valid types and then upload
        them to Twitter. The resulting media ID is then used in the status update
        message or DM.

        Args:
            inList:
                list of file names
            maxMedia:
                max number of media file to upload
            strict:
                If 'True' then exception is raised when file does not exist,
                otherwise empty list is returned

        Returns:
            List of media IDs

        Raises:
            CommunicationsError: Twitter/Tweepy API returns an error
            FileNotFoundError: Media file cannot be found
        """
        if not self._client or not inList or maxMedia < 1:
            return []

        outList: List[str] = []
        try:
            mediaList = [
                self._client.media_upload(item)
                for item in inList[:maxMedia]
                if provider.verify_media_file(item, _VALID_IMG_FMTS_, strict)
            ]
            outList = [item.media_id for item in mediaList]

        except FileNotFoundError as e:
            if strict:
                log.error(f"FileNotFoundError: {e}")
                raise FileNotFoundError from e

        except tweepy.HTTPException as e:
            if strict:
                log.error(f"HTTP error: {e}")
                raise CommunicationsError(errors=[f"HTTPException {e}"]) from e

        return outList

    def get_user_id(self, dmUserName: str, strict: bool = False) -> str:
        """Get Twitter user ID.

        This method provides a standard interface for retrieving the user ID
        for a given Twitter username.

        Args:
            dmUserName:
                simple/plain text version of message to be sent
            strict:
                If 'True' then exception is raised when user does not exist,
                otherwise empty string is returned

        Returns:
            Twitter user ID for a given username

        Raises:
            MissingAttributeError: Twitter DM username is blank
            CommunicationsError: Twitter/Tweepy API returns an error or Twitter creds are invalid
        """
        if not self._client:
            log.error("Invalid Twitter credentials")
            raise CommunicationsError(
                **self._make_comm_error(
                    "Invalid Twitter credentials!", dmUserName, "001"
                )
            )

        cleanDMUserName = dmUserName.strip("@ ")
        if not cleanDMUserName:
            log.error("Blank Twitter user name")
            raise MissingAttributeError(
                "Twitter username message text cannot be empty."
            )

        try:
            log.debug(f"Get Twitter user ID for '{dmUserName}'")
            user = self._client.get_user(screen_name=cleanDMUserName)
            log.info(f"Twitter user ID: {user.id_str}")

        except tweepy.HTTPException as e:
            if strict:
                log.error(f"HTTP error: {e}")
                raise CommunicationsError(
                    **self._make_comm_error(f"HTTPException {e}", dmUserName, "002")
                ) from e
            else:
                return ""

        return str(user.id_str)

    def send_status_update(self, msg: str, **kwargs: Any) -> List[provider.Response]:
        """Post Twitter status update.

        This method provides a standard interface for posting Twitter
        status update messages.

        Args:
            msg:
                simple/plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            'list' of 'Response' objects from Tweepy API call. We always return a list
            even though we'll only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            MissingAttributeError: Twitter message is blank
            CommunicationsError: Twitter/Tweepy API returns an error or Twitter creds are invalid
        """
        if not self._client:
            log.error("Invalid Twitter credentials")
            raise CommunicationsError(errors=["Invalid Twitter credentials!"])

        if not msg.strip():
            log.error("Blank Tweet message")
            raise MissingAttributeError("Tweet message cannot be blank.")

        # Combine message text with '@' list and any hashtags
        statusMsg = self._make_msg_content(
            msg=msg,
            atList=kwargs.get(const.KWD_TO_TWITTER, ""),
            tagList=kwargs.get(const.KWD_TAGS, self._defaultTags),
        )

        # Do we have media?
        mediaIDList = self._upload_media(
            inList=provider.process_media_list(kwargs.get(const.KWD_MEDIA, "")),
            maxMedia=1,
        )

        try:
            log.debug("Sending Twitter status update")
            clientResponse = self._client.update_status(
                status=statusMsg, media_ids=mediaIDList
            )
            log.info(f"Twitter response code: {clientResponse}")
            response = self._make_response(
                data={"status": statusMsg, "media_ids": mediaIDList},
                response=None,
                errors=None,
            )

        except tweepy.HTTPException as e:
            log.error(f"HTTP error: {e}")
            raise CommunicationsError(errors=[f"HTTPException {e}"]) from e

        except tweepy.errors.TweepyException as e:
            log.error(f"Tweepy API error: {e}")
            raise CommunicationsError(errors=[f"TweepyException {e}"]) from e

        return [response]

    def send_dm(self, msg: str, **kwargs: Any) -> List[provider.Response]:
        """Send Twitter DM.

        This method provides a standard interface for sending Twitter
        DMs to a specific recipient/username. The recipient name must
        be listed using the 'to_twitter' key.

        Note:
            No need to validate Twitter credentials here as this is done
            when retrieving Twitter ID for recipient.

        Args:
            msg:
                Simple/plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            'list' of 'Response' objects from Tweepy API call. We always return a list
            even though we'll only have a single item. This allows us to be consistent
            across all 'send_message()' functions.

        Raises:
            MissingAttributeError: Twitter message is blank
            CommunicationsError: Twitter/Tweepy API returns an error or Twitter creds are invalid
        """
        if not self._client:
            log.error("Invalid Twitter credentials")
            raise CommunicationsError(errors=["Invalid Twitter credentials!"])

        if not msg.strip():
            log.error("Blank Tweet message")
            raise MissingAttributeError("Tweet message cannot be blank.")

        # We need one or more recipients!
        toList = ToTwitter(
            inList=kwargs.get(const.KWD_TO_TWITTER, self._defaultTo),
            maxNum=_MAX_RECIPIENTS_,
        )
        recipientList = self._process_dm_list(toList.clean)
        if not recipientList:
            log.error("Unknown/invalid DM recipient(s)")
            raise CommunicationsError(errors=["Unknown/invalid DM recipient(s)."])

        # Combine message text with any hashtags
        dmMsg = self._make_msg_content(
            msg=msg, tagList=kwargs.get(const.KWD_TAGS, self._defaultTags)
        )

        # Do we have media?
        mediaIDList = self._upload_media(
            inList=provider.process_media_list(kwargs.get(const.KWD_MEDIA, "")),
            maxMedia=1,
        )
        mediaID = (
            mediaIDList[0] if mediaIDList else ""
        )  # Only 1 media item allowed in DMs
        suppress = kwargs.get(const.KWD_SUPPRESS_ERROR, False)

        return [
            self._send_single_dm_message(dmName, dmID, dmMsg, mediaID, suppress)
            for (dmName, dmID) in recipientList
        ]

    def _send_single_dm_message(
        self, dmName: str, dmID: str, msg: str, mediaID: str, suppress: bool = False
    ) -> provider.Response:
        """Send single Twitter DM.

        This helper method sends a single Twitter DM.

        Args:
            dmName:
                Recipient Twitter name
            dmID:
                Recipient Twitter ID
            msg:
                Message to be sent
            mediaID:
                ID of media attachment -- DMs only allow single attachment
            suppress:
                If 'False' then exception will be raised if request response returns errors

        Returns:
            Response from Twitter service API call

        Raises:
            CommunicationsError: 'suppress' is 'False' and response has errors
        """
        msgData = {"recipient_id": dmID, "text": msg, "attachment_media_id": mediaID}

        twitterResponse = None
        twitterErrors = []

        if not self._client:
            log.error("Invalid Twitter credentials")
            raise CommunicationsError(errors=["Invalid Twitter credentials!"])

        try:
            log.debug(f"Sending Twitter DM message to '{dmName}' [ID:{dmID}]")
            twitterResponse = self._client.send_direct_message(**msgData)

        except tweepy.HTTPException as e:
            log.error(f"HTTPException {e}")
            twitterErrors.append(f"HTTPException {e}")

        except tweepy.errors.TweepyException as e:
            log.error(f"TweepyException {e}")
            twitterErrors.append(f"TweepyException {e}")

        response = self._make_response(msgData, twitterResponse, twitterErrors)
        log.info(f"Twitter response code: {twitterResponse}")

        if not suppress:
            response.raise_on_errors()

        return response

    def send_message(self, msg: str, **kwargs: Any) -> List[provider.Response]:
        """Post Twitter status update or send DM.

        This method provides a standard interface for posting a Twitter status
        update or send a Twitter DM to a specific user. The 'method_dm' key is
        used to indicate how the message will be sent.

        Note:
            We determine whether to send a DM or a regular status update (i.e. tweet)
            based on the 'method_<xxxx>' attribute. The strategy is to check for
            explicit 'DM' first. We'll go with status update if 'method_dm' is set
            to 'False' or is missing, unless 'method_update' is set to 'False'.

            1. 'method_dm' is 'True' --> send DM
            2. 'method_dm' is 'False' --> send status update
            3. 'method_dm' is missing --> check 'method_update'

            4. 'method_dm' is missing and 'method_update' is 'True' --> send status update
            5. 'method_dm' is missing and 'method_update' is 'False' --> send DM
            6. 'method_dm' is missing and 'method_update' is missing --> send status update

            7. 'method_dm' is 'True' and 'method_update' is 'True' --> send DM as 'method_dm' has priority

        Args:
            msg:
                Simple/plain text version of message to be sent
            kwargs:
                Additional optional arguments

        Returns:
            'list' of 'Response' objects from Tweepy API call. We always return a list
            even though we'll only have a single item. This allows us to be consistent
            across all 'send_message()' functions.
        """
        useDM = kwargs.get(
            const.KWD_METHOD_DM, kwargs.get(const.KWD_METHOD_UPDATE, True)
        )

        return (
            self.send_dm(msg, **kwargs)
            if useDM
            else self.send_status_update(msg, **kwargs)
        )


# =========================================================
#              U T I L I T Y   F U N C T I O N S
# =========================================================
def process_recipient_list(inList: Any, maxNum: int) -> List[Entity]:
    """Process list of recipients and return list of 'Entity' objects.

    Args:
        inList:
             Single Twitter name (string) or 'Entity' object, or list of
             one or more names or 'Entity' objects.
        maxNum:
            Max number of Twitter names

    Returns:
        List of 'Entity' objects
    """
    # Ensure we have proper lists of either Twitter name strings or 'Entity' objects
    if isinstance(inList, str):
        inList = utils.convert_attrib_str_to_list(inList)
    elif isinstance(inList, Entity):
        inList = [inList]

    if not isinstance(inList, list):
        return []

    # Ensure we work with unique records by converting 'list' to 'set' and
    # then convert list of Twitter name strings to list of 'Entity' objects
    tmpSet = set(inList)
    if all(isinstance(item, str) for item in tmpSet):
        outList = [
            item.strip("@ ")
            for item in tmpSet
            if utils.is_valid_twitter(item.strip("@ "))
        ]
        return [Entity(twitter=item) for item in set(outList)][:maxNum]

    # Ensure that all items in list of 'Entity' objects have a phone number
    elif all(isinstance(item, Entity) for item in inList):
        tmpList = dedupe_by_attribute(inList, "twitter")
        return [item for item in tmpList if item.twitter][:maxNum]

    return []
