"""Global constants for f451 Communications module.

This module holds all global constants used within various components of
the f451 Communications module. Most constants are used as keyword equivalents
for attributes in .ini files.
"""
# =========================================================
#              M I S C .   C O N S T A N T S
# =========================================================
DELIM_STD: str = "|"
DELIM_VAL: str = ":"

# =========================================================
#    K E Y W O R D S   F O R   C O N F I G   F I L E S
# =========================================================
CHANNEL_ALL: str = "all"
CHANNEL_MAIN: str = "f451_main"
CHANNEL_MAILGUN: str = "f451_mailgun"
CHANNEL_SLACK: str = "f451_slack"
CHANNEL_TWILIO: str = "f451_twilio"
CHANNEL_TWITTER: str = "f451_twitter"

KWD_ACCT_SID: str = "acct_sid"
KWD_APP_TOKEN: str = "app_token"
KWD_ATTACHMENTS: str = "attachments"  # Attachments for email and Slack
KWD_AUTH_SECRET: str = "auth_secret"
KWD_AUTH_TOKEN: str = "auth_token"
KWD_BCC_EMAIL: str = "bcc_email"
KWD_CC_EMAIL: str = "cc_email"
KWD_CHANNELS: str = "channels"
KWD_CHANNEL_MAP: str = "channel_map"
KWD_DEBUG: str = "debug"  # Reserved
KWD_EMAIL: str = "email"
KWD_FILE_TITLE: str = "file_title"  # Attachment/file title for Slack
KWD_FROM: str = "from"
KWD_FROM_DOMAIN: str = "from_domain"
KWD_FROM_EMAIL: str = "from_email"  # Reserved for future use
KWD_FROM_NAME: str = "from_name"
KWD_FROM_PHONE: str = "from_phone"
KWD_FROM_SLACK: str = "from_slack"
KWD_FROM_TWITTER: str = "from_twitter"
KWD_HTML: str = "html"  # HTML text for email
KWD_ICON_EMOJI: str = "icon_emoji"
KWD_INLINE: str = "inline"  # Inline images for email
KWD_LOG_LEVEL: str = "log_level"
KWD_MEDIA: str = "media"  # Media for Twilio, and Twitter
KWD_METHOD_UPDATE: str = "method_update"
KWD_METHOD_DM: str = "method_dm"
KWD_NAME: str = "name"
KWD_PHONE: str = "phone"
KWD_PRIV_KEY: str = "priv_api_key"
KWD_PUBL_KEY: str = "publ_val_key"
KWD_RECIPIENT: str = "recipient"  # Reserved for future use
KWD_RECIPIENT_DATA: str = "recipient_data"
KWD_SIGN_SECRET: str = "signing_secret"
KWD_SLACK: str = "slack"
KWD_SUBJECT: str = "subject"
KWD_SUPPRESS_ERROR: str = "suppress_errors"
KWD_TAGS: str = "tags"
KWD_TESTMODE: str = "testmode"
KWD_TO: str = "to"
KWD_TO_CHANNEL: str = "to_channel"
KWD_TO_NAME: str = "to_name"
KWD_TO_EMAIL: str = "to_email"
KWD_TO_PHONE: str = "to_phone"
KWD_TO_SLACK: str = "to_slack"
KWD_TO_TWITTER: str = "to_twitter"
KWD_TRACKING: str = "tracking"
KWD_TWITTER: str = "twitter"
KWD_USER_KEY: str = "user_key"
KWD_USER_SECRET: str = "user_secret"
KWD_WEB_HOOK_KEY: str = "webhook_sign_key"

LOG_CRITICAL: str = "CRITICAL"
LOG_DEBUG: str = "DEBUG"
LOG_ERROR: str = "ERROR"
LOG_INFO: str = "INFO"
LOG_NOTSET: str = "NOTSET"
LOG_OFF: str = "OFF"
LOG_WARNING: str = "WARNING"

LOG_LVL_OFF: int = -1
LOG_LVL_MIN: int = -1
LOG_LVL_MAX: int = 100

ATTR_REQUIRED: bool = True
ATTR_OPTIONAL: bool = False

SRV_TYPE_MAIN: str = "main"
SRV_TYPE_EMAIL: str = "email"
SRV_TYPE_SMS: str = "sms"
SRV_TYPE_FORUMS: str = "forums"
SRV_TYPE_TWITTER: str = "twitter"
SRV_TYPE_SLACK: str = "slack"

STATUS_SUCCESS: str = "success"
STATUS_FAILURE: str = "failure"
