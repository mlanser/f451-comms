Demo of communications functions
================================

You can see all communications functions in action by running:
::

   $ python -m f451-comms --msg "Hello world! :-)" --secrets _PATH_TO_SECRETS_

This will send a "*Hello world!*" message to all channels listed in the ``secrets.ini`` or similar configuration file. And yes, in order for this to work, you'll need to first set up accounts with all services (e.g. email, Slack, SMS, etc.) that you want to use.

You need to set up accounts with the services that you want to use. The *f451 Communications* module currently supports the following services:

- **email:** `Mailgun <https://mailgun.com>`__
- **Slack:** `Slack <https://slack.com>`__ (also requires `Python Slack SDK <https://github.com/SlackAPI/python-slack-sdk>`__)
- **SMS:** `Twilio <https://twilio.com>`__ (also requires `Twilio Python <https://github.com/twilio/twilio-python>`__)
- **Twitter:** `Twitter <https://slack.com>`__ (also requires `Tweepy <https://docs.tweepy.org/en/stable/index.html>`__)

.. note:: Please review the documentation for each sub-module for additional information.

.. warning:: If API keys and other secrets are not properly defined in your configuration files, then the methods in the *f451 Communications* module will raise exception.


Sample `secrets.ini` file
-------------------------

It is recommended that you store API keys and other secrets in a separate configuration file. Also ensure that this file is **excluded** from any files uploaded to source code repositories.

.. literalinclude:: ../src/f451_comms/secrets.ini.example
   :language: ini

See section "`Configuration files <config_files.html>`__" for more information.


Running from CLI
----------------

.. sphinx_argparse_cli::
   :module: f451_comms.__main__
   :func: init_cli_parser
   :prog: f451-comms
