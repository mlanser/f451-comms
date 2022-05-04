The following keywords and values are primarily used to pass additional arguments via the ``**kwargs`` parameter to the various ``send_message_<xxxx>`` functions. Please note that some keywords can also be used for defining API credentials and various default values for use in config files (e.g. ``config.ini``).

- ``account_sid``
    - Required for:
        - SMS (`Twilio <send_twilio.html>`__) -- Twilio account SID as ``str``
    - Example .ini entry:
        - ``acct_sid = XX0x00x0x0xxxxx000x0x0x0x000xxx00x``

    .. warning:: Do NOT store this value in source code!

- ``app_token``
    - Required for:
        - Slack (`Slack <send_slack.html>`__) -- Slack app token as ``str``
    - Example .ini entry:
        - ``app_token = xapp-0-X00000000-000000000-00000000xxxxx00000000xxxxx00000000``

    .. warning:: Do NOT store this value in source code!

- ``attachments``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- one or more file names as ``str`` or ``list`` of ``str``
        - Slack (`Slack <send_slack.html>`__) -- one or more file names as ``str`` or ``list`` of ``str``
    - Examples:
        - Single attachment: ``{"attachments": path/to/file1.txt"}``
        - Multiple attachments: ``{"attachments": ["path/to/file1.txt", "path/to/file2.txt"]}``

- ``auth_secret``
    - Required for:
        - Twitter (`Twitter <send_twitter.html>`__) -- Twitter auth secret as ``str``
    - Example .ini entry:
        - ``auth_secret = xx0000000000xx000000x0000000x0xx00000xxx00000``

    .. warning:: Do NOT store this value in source code!

- ``auth_token``
    - Required for:
        - Slack (`Slack <send_slack.html>`__) -- Slack auth token as ``str``
        - SMS (`Twilio <send_twilio.html>`__) -- Twilio auth token as ``str``
        - Twitter (`Twitter <send_twitter.html>`__) -- Twitter auth token as ``str``
    - Example .ini entry:
        - ``auth_token = 000000000000000000000000000000000000000000000``

    .. warning:: Do NOT store this value in source code!

- ``bcc_email``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- see ``to_email`` attribute

- ``cc_email``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- see ``to_email`` attribute

- ``channels``
    - Required for:
        - ``Comms.send_message()`` method -- one or more tags as ``str`` or ``list`` of ``str``
    - Examples:
        - Send message to all available channels: ``{"channels": "all"}``
        - Send message to Twitter and Slack: ``{"channels": ["f451_twitter", "f451_slack"]}`` or ``{"channels": "f451_twitter|f451_slack"}``
    - Valid options:
        - ``all`` -- all channels
        - ``f451_mailgun`` -- email via `Mailgun <send_mailgun.html>`__ service
        - ``f451_slack`` -- `Slack <send_slack.html>`__ message
        - ``f451_twilio`` -- SMS via `Twilio <send_twilio.html>`__ service
        - ``f451_twitter`` -- `Twitter <send_twitter.html>`__ status updates and DMs

    .. note:: Use ``channel_map`` attribute to map custom keywords against channel names.

- ``channel_map``
    - **Optional for:** ``main`` section
    - Examples:
        - Map *email* and *sms* keywords: ``channel_map = email:f451_mailgun|sms:f451_twilio``

- ``debug``
    - **Reserved** for future use

- ``file_title``
    - Optional for:
        - Slack (`Slack <send_slack.html>`__) -- file title as ``str``
    - Examples:
        - Simple title: ``{"file_title": "List of Gotham City crime bosses"}``

- ``from_domain``
    - Required for:
        - Email (`Mailgun <send_mailgun.html>`__) -- Mailgun domain as ``str``
    - Example .ini entry:
        - ``from_domain = xxxxxxx00000000000000000000.mailgun.org``

    .. warning:: Do NOT store this value in source code!

- ``from_email``
    - *Reserved for future use*

- ``from_name``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- sender name ``str``

- ``from_phone``
    - Required for:
        - SMS (`Twilio <send_twilio.html>`__) -- Twilio sender phone number as ``str``
    - Example .ini entry:
        - ``from_phone = +12125150000``

    .. warning:: Do NOT store this value in source code!

- ``from_slack``
    - Optional for:
        - `Slack <send_slack.html>`__ -- sender name ``str``

- ``from_twitter``
    - Required for:
        - `Twitter <send_twitter.html>`__ DMs -- sender name ``str``

- ``html``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- HTML version of email message as ``str``
    - Example:
        - Simple: ``{"html": "<html>Hello world!</html>"}``

- ``icon_emoji``
    - Optional for:
        - `Slack <send_slack.html>`__ -- a ``str`` that represents the emoji short code.
    - Examples:
        - Use *See No Evil* emoji: ``{"icon_emoji": ":see_no_evil:"}``

- ``inline``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- one or more file names as ``str`` or ``list`` of ``str``
    - **Valid formats:** .png, .jpg, .gif
    - Examples:
        - Single inline image: ``{"inline": path/to/image1.jpg"}``
        - Multiple inline images: ``{"inline": ["path/to/image1.jpg", "path/to/image2.jpg"]}``

- ``log_level``
    - Optional for:
        - all channels -- ``int`` or ``str``
    - **Default:** ``logging.INFO``
    - Valid options:
        - ``-1`` or ``OFF`` -- no logging
        - ``int`` from ``0`` to ``100`` -- log level is set to this value.
        - standard log levels defined in `Python 'logging' package <https://docs.python.org/3.9/howto/logging.html#logging-levels>`__ package as ``logging.<CONST>`` or equivalent string name
    - Examples:
        - Enable logging: ``{"log_level": logging.INFO}`` or {"log_level": "INFO"}
        - Disable logging: ``{"log_level": -1}`` or ``{"log_level": "OFF"}``

- ``media``
    - Optional for:
        - SMS (`Twilio <send_twilio.html>`__) -- one or more file names as ``str`` or ``list`` of ``str``
        - Twitter (`Twitter <send_twitter.html>`__) -- one or more file names as ``str`` or ``list`` of ``str``
    - **Valid formats:** .png, .jpg, .gif
    - Examples:
        - Single attachment: ``{"attachments": path/to/file1.txt"}``
        - Multiple attachments: ``{"attachments": ["path/to/file1.txt", "path/to/file2.txt"]}``

- ``method_update``
    - *Reserved for future use*

- ``method_dm``
    - Optional for:
        - `Twitter <send_twitter.html>`__ -- boolean flag. If ``True`` message is sent as DM. This also requires at least one name listed in ``to_twitter`` attribute.
    - **Default:** ``False``
    - Examples:
        - Send message as DM: ``{"method_dm": True}``

- ``priv_api_key``
    - Required for:
        - Email (`Mailgun <send_mailgun.html>`__) -- Mailgun private API key as ``str``
    - Example .ini entry:
        - ``priv_api_key = key-00000000000000000000000000000000``

    .. warning:: Do NOT store this value in source code!

- ``publ_val_key``
    - Required for:
        - Email (`Mailgun <send_mailgun.html>`__) -- Mailgun public API key as ``str``
    - Example .ini entry:
        - ``publ_val_key = pubkey-00000000000000000000000000000000``

    .. warning:: Do NOT store this value in source code!

- ``recipient``
    - *Reserved for future use*

- ``recipient_data``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- list of additional recipient info for batch emails as ``struct``
    - Example:
        - Email address used as key: ``{"recipient_data": {"batman@example.com": {"name":"Batman", "lucky": 13}, ...}}``

- ``signing_secret``
    - Required for:
        - Slack (`Slack <send_slack.html>`__) -- signing secret as ``str``
    - Example .ini entry:
        - ``signing_secret = xxxxx0000000000xxx000000000xxxx00000``

    .. warning:: Do NOT store this value in source code!

- ``subject``
    - Required for:
        - Email (`Mailgun <send_mailgun.html>`__) -- email subject line as ``str``
    - Examples:
        - Simple: ``{"subject": "Hello world!"}``
        - Personalized using ``recipients`` info: ``{"subject": "Hello %recipients.name%"}``

- ``suppress_errors``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- boolean flag. If ``True`` Mailgun exceptions are suppressed.
        - SMS (`Twilio <send_twilio.html>`__) -- boolean flag. If ``True`` Twilio exceptions are suppressed.
        - `Twitter DM <send_twitter.html>`__ -- boolean flag. If ``True`` Twitter exceptions are suppressed.
    - **Default:** ``False``
    - Examples:
        - Suppress errors: ``{"suppress_error": True}``

- ``tags``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- one or more (max 3) tags as ``str`` or ``list`` of ``str``
    - Examples:
        - Single tag: ``{"tags": "greeting"}``
        - Multiple tags: ``{"tags": ["greeting", "salutation"]}`` or ``{"tags": "greeting|salutation"}``

- ``testmode``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- boolean flag. If ``True`` *test mode* is enabled.
    - **Default:** ``False``
    - Examples:
        - Enable *test mode*: ``{"testmode": True}``

- ``to_channel``
    - Required for:
        - `Slack <send_slack.html>`__ -- one or more Slack channels as ``str`` or ``list`` of ``str``
    - Examples:
        - Single channel: ``{"to_channel": "#GothamCrime"}``
        - Multiple recipients: ``{"to_channel": ["#GothamCrime", "#NewVillains"]}`` or ``{"to_channel": "GothamCrime|NewVillains"}``

- ``to_email``
    - Required for:
        - Email (`Mailgun <send_mailgun.html>`__) -- one or more email addresses as ``str`` or ``list`` of ``str``
    - Examples:
        - Single recipient: ``{"to_email": "batman@example.com"}``
        - Multiple recipients: ``{"to_email": ["batman@example.com", "robin@example.com"]}`` or ``{"to_email": "batman@example.com|robin@example.com"}``

    .. note:: If you send an email to multiple recipients, then also use the ``recipient_data`` attribute for additional recipient info.

- ``to_phone``
    - Required for:
        - SMS (`Twilio <send_twilio.html>`__) -- one or more phone numbers as ``str`` or ``list`` of ``str``
    - Examples:
        - Single recipient: ``{"to_phone": "+12125550000"}``
        - Multiple recipients: ``{"to_phone": ["+12125550000", "+12125551111"]}`` or ``{"to_phone": "+12125550000|+12125551111"}``

- ``to_slack``
    - Optional for:
        - `Slack <send_slack.html>`__ -- one or more Slack user Names as ``str`` or ``list`` of ``str``.  Names listed here will be included with '@' symbol in the beginning of the Slack message.
    - Examples:
        - Single name: ``{"to_slack": "batman"}``
        - Multiple names: ``{"to_slack": ["batman", "robin"]}`` or ``{"to_slack": "batman|robin"}``

- ``to_twitter``
    - Optional for:
        - `Twitter <send_twitter.html>`__ -- one or more Twitter user names as ``str`` or ``list`` of ``str``. If ``method_dm`` is ``False``, then names listed here will be included with '@' symbol in the beginning of the Twitter status update message.
    - Examples:
        - Single name: ``{"to_twitter": "batman"}``
        - Multiple names: ``{"to_twitter": ["batman", "robin"]}`` or ``{"to_twitter": "batman|robin"}``

- ``tracking``
    - Optional for:
        - Email (`Mailgun <send_mailgun.html>`__) -- boolean flag. If ``True`` tracking is enabled.
    - **Default:** ``False``
    - Examples:
        - Enable tracking: ``{"tracking": True}``

- ``user_key``
    - Required for:
        - Twitter (`Twitter <send_twitter.html>`__) -- Twitter user key as ``str``
    - Example .ini entry:
        - ``user_key = xxxxx0000000000xxx000000000xxxx00000``

    .. warning:: Do NOT store this value in source code!

- ``user_secret``
    - Required for:
        - Twitter (`Twitter <send_twitter.html>`__) -- Twitter user secret as ``str``
    - Example .ini entry:
        - ``user_secret = xxxxx0000000000xxx000000000xxxx00000xxxxx00000xxxxx0000``

    .. warning:: Do NOT store this value in source code!

- ``webhook_sign_key``
    - Required for:
        - Email (`Mailgun <send_mailgun.html>`__) -- Mailgun webhook sign key as ``str``
    - Example .ini entry:
        - ``webhook_sign_key = key-xxxxx0000000000xxx000000000``

    .. warning:: Do NOT store this value in source code!

.. note:: Attributes that support ``str`` and ``list`` of ``str`` can process the lists either as a string using pipe character (``|``) as delimiter between values, or as a true ``lst`` of ``str``:

    - list of values as simple ``str``: ``"apple|banana|orange"``
    - list of values as ``lst`` of ``str``:  ``["apple", "banana", "orange"]``
