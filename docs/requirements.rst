Requirements and dependencies
=============================

The *f451 Communications* module is an abstraction layer for a set of communications packages. But in order for it to work, you need to first install the underlying packages and set up accounts with the associated services.

Please note, that you do not have to use all services. In the end, config files (e.g. ``secrets.ini`` and ``config.ini``) define which services are enabled. Conversely, if you enable a service where you do not have the proper API keys, etc., then the module will raise exceptions when authentication fails due to missing and/or invalid credentials.

- **email** -- account at `Mailgun <https://mailgun.com>`__
- **Slack** -- account at `Slack <https://slack.com>`__
- **SMS** -- account at `Twilio <https://twilio.com>`__
- **Twitter** -- account at `Twitter <https://slack.com>`__

This module also relies on a few specialized communications libraries which are installed automatically as dependencies:

- **email** -- `requests <https://docs.python-requests.org/en/latest/>`__
- **Slack** -- `Python Slack SDK <https://github.com/SlackAPI/python-slack-sdk>`__
- **Twilio** (SMS) -- `Twilio Python <https://github.com/twilio/twilio-python>`__
- **Twitter** -- `Tweepy <https://docs.tweepy.org/en/stable/index.html>`__

.. note:: Please review the documentation for each sub-module for additional information.
