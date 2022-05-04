Post Twitter status updates and send DMs
========================================

The *f451 Communications* module allows you to post `Twitter status updates <https://twitter.com>`__ and send DMs to a given recipient using a unified interface. In it's simplest for form, you can post plain text message status update. But you can also send DMs to specific recipients.

In order to use this service, you'll need to `set up an account with Twitter <https://developer.twitter.com>`__. Once that is done, you get your API key and other relevant account credentials.

.. note:: Please refer to the "`Configuration files <config_files.html>`_" section for more detailed information on configuration requirements for `Twitter <https://twitter.com>`_ status updates and DMs.


Core features
-------------

- **Post status updates** -- *Status updates can be text-only as well as include images.*
- **Send DMs to multiple recipients** -- *Allows you to send Twitter DM messages to multiple recipients*


Post status updates using the main ``Comms`` object
---------------------------------------------------

You can send `Twitter status updates <https://twitter.com>`__ using the unified ``send_message()`` method of the ``Comms`` object as follows:

STEP 1: initialize ``Comms`` object

.. code-block::

    comms = Comms(
                secrets,            # credentials required for services
                config              # optional settings
            )

STEP 2: call ``send_message()`` method

.. code-block::

    comms.send_message(
                "Hello world!",     # plain text message
                attribs             # misc. attributes required to send message
            )

ALTERNATIVE: call ``send_message_via_twitter()`` method

.. code-block::

    comms.send_message_via_twitter(
                "Hello world!",     # plain text message
                attribs             # misc. attributes required to send message
            )

.. note:: Please to section "`Configuration files <config_files.html>`__" for more details on defining ``secrets`` and ``config`` data.

.. note:: Please see below for a detailed description of options for ``attribs`` and note that some items are required in order to send emails. Also note that some values can be stored as default values when initializing the main ``Comms`` object and the do not need to be included in the ``attribs`` argument.

.. note:: If alternative ``send_message_via_twitter()`` is used, then ``channels`` attribute is not required in the ``attribs`` argument.


Post status updates using the ``comms_twitter.Twitter`` object
--------------------------------------------------------------

You can send SMS using the ``send_message()`` method of the ``Twitter`` object in the ``comms_twitter`` sub-module as follows:

1. Initialize the ``Twitter`` object:

.. code-block::

    client = Twitter(
                usrKey,             # your Twitter user key
                usrSecret,          # your Twitter user secret
                authToken,          # your Twitter auth/access token
                authSecret,         # your Twitter auth/access token secret
                defaults            # optional default values
            )

2. Call the ``send_message()`` method:

.. code-block::

    client.send_message(
                "Hello world!",     # plain text message
                attribs             # misc. attributes required to send message
            )

.. note:: Please to section "`Configuration files <config_files.html>`__" for more details on defining ``secrets`` and ``config`` data.

.. note:: Please see below for a detailed description of options for ``attribs`` and note that some items are required in order to send Twitter status updates or DMs. Also note that some values can be stored as default values when initializing the main ``Comms`` object and the do not need to be included in the ``attribs`` argument.


Keywords and values for ``attribs`` argument
--------------------------------------------

.. include:: attribs.rst


Examples
--------

Example -- structure for simple Twitter status update:

.. code-block::

    attribs = {
        "channels": "f451_twitter",
    }

Example -- structure for simple Twitter DM:

.. code-block::

    attribs = {
        "channels": "f451_twitter",
        "to_twitter": "batman",
        "method_dm": True,
    }


Example -- structure for simple Twitter status update with '@' some Twitter users:

.. code-block::

    attribs = {
        "channels": "f451_twitter",
        "to_twitter": ["batman", "robin"],
        "method_dm": False,
    }


Additional references
---------------------

- `Tweepy documentation <https://docs.tweepy.org/en/stable/index.html>`__
- `Twitter documentation <https://developer.twitter.com/en/docs>`__
