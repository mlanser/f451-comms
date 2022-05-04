Configuration files
===================

As the *f451 Communications* module is merely an abstraction layer for a several different of communication services, it relies on the calling application to provide all necessary API keys and other secrets and settings to properly authenticate with those services.

These keys and and secrets can be submitted ad hoc (via properly formatted ``dict`` structures) when the communications object is initialized. However, it is recommended to instead store these keys and secrets in so-called configuration files and then submit the filename and path to these files to the initialization method.

Furthermore, the *f451 Communications* module allows you to keep keys and secrets and default applications settings in separate files. For example, keys and secrets can be stored in a file called ``secrets.ini`` and miscellaneous settings and  default values can be stored in ``config.ini``.

.. note:: Any configuration file must use a format that the `Python ConfigParser library <https://docs.python.org/3.9/library/configparser.html#module-configparser>`_ can process.

.. note:: It's not necessary to have a separate ``secrets.ini`` file for the just the *f451 Communications* module. As long as there is no conflict between section names, values required by *f451 Communications* can be co-located with values required by other modules and systems.


Sample ``secrets.ini`` file
---------------------------

The ``secrets.ini`` file should contain all keys and secrets required to authenticate against the services that you want to use with the *f451 Communications* module.

.. literalinclude:: ../src/f451_comms/secrets.ini.example
   :language: ini


Sample `config.ini` file
------------------------

The ``config.ini`` file can hold any optional settings and default values for the *f451 Communications* module.

.. literalinclude:: ../src/f451_comms/config.ini.example
   :language: ini


Using ``dict`` structure during testing
---------------------------------------

It is recommended that permanent keys and secrets are stored in config files. However, some use cases may call for using temporary values (e.g. for testing) and to support that, the *f451 Communications* module also allows you to supply keys, secrets, and other configurations values via properly formatted ``dict`` structures.

.. code-block::

    data = {
        'section1_label': {
            'item1_key': 'value1',
            'item2_key': 'value2',
             ...
            'itemN_key': 'valueN',
        }
    }

Such a ``dict`` structure is then converted internally to a ``ConfigParser`` object.


Keywords for managing secret keys and values
--------------------------------------------

The *f451 Communications* module looks for specific section and item labels to be used as credentials for the supporting communication services.

**Section** ``f451_mailgun``

- **Description:** used for values related to Mailgun email service
- **Required:** yes, if email channel is used
- **Items:**

  - ``priv_api_key`` -- *your private Mailgun API key string*
  - ``publ_val_key`` -- *your public Mailgun API key string*
  - ``webhook_sign_key`` -- *your Mailgun webhook signing key*
  - ``from_domain`` -- *your Mailgun domain name*

- **Reference:** `Mailgun <https://mailgun.com>`_


**Section** ``f451_slack``

- **Description:** used for values related to Slack service
- **Required:** yes, if Slack channel is used
- **Items:**

  - ``auth_token`` -- *your Slack auth token*
  - ``app_token`` -- *your Slack app token*
  - ``signing_secret`` -- *your Slack signing secret*

- **Reference:** `Slack <https://slack.com>`_


**Section** ``f451_twilio``

- **Description:** used for values related to Slack service
- **Required:** yes, if Slack channel is used
- **Items:**

  - ``acct_sid`` -- *your Twilio account SID*
  - ``auth_token`` -- *your Twilio auth token*
  - ``from_phone`` -- *your 'from' phone number*

- **Reference:** `Twilio <https://twilio.com>`_


**Section** ``f451_twitter``

- **Description:** used for values related to Twitter service
- **Required:** yes, if Twitter channel is used
- **Items:**

  - ``user_key`` -- *your Twitter user key*
  - ``user_secret`` -- *your Twitter secret key*
  - ``auth_token`` -- *your Twitter auth token*
  - ``auth_secret`` -- *your Twitter auth secret*

- **Reference:** `Twitter <https://twitter.com>`_, `Tweepy <https://tweepy.org>`_


Keywords for managing optional settings and values
--------------------------------------------------

The *f451 Communications* module looks for specific section and item labels to be used as optional setting or default values for the supporting communication services.

**Section** ``f451_main``

- **Description:** used for optional settings related to ???
- **Items:**

  - ``channels`` -- *list of default channels separated by '\|' character (e.g. 'twitter\|slack')*


**Section** ``f451_mailgun``

- **Description:** used for optional settings related to email
- **Items:**

  - ``subject`` -- *default email subject (e.g. 'Status update ...')*
  - ``to_email`` -- *default recipient email address*
  - ``from_name`` -- *optional default '*from*' name*


**Section** ``f451_slack``

- **Description:** used for optional settings related to Slack
- **Items:**

  - ``to_channel`` -- *default Slack channel (e.g. '#general')*
  - ``icon_emoji`` -- *default app/user icon emoji (e.g. ':see_no_evil:')*
  - ``from_name`` -- *default app/user name*


**Section** ``f451_twilio``

- **Description:** used for values related to Slack service
- **Required:** yes, if Slack channel is used
- **Items:**

  - ``to_phone`` -- *optional default 'to' phone number*

**Section** ``f451_twitter``

- **Description:** used for optional settings related to Twitter
- **Items:**

  - ``to_name`` -- *Twitter user name of default DM recipient*
