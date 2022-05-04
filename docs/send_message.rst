Send messages to multiple channels
==================================

The *f451 Communications* module allows you to send messages to several channels at the same time via the unified ``send_message()`` method in the ``Comms`` object. You indicate which channels to use, as well as other message attributes, using the ``attribs`` argument. For example, you can send the same message via Twitter, Slack, and SMS with a single method call.

In order to use this command, you'll need to set up an accounts with all services that you want to use. Once that is done, you get your API keys and other relevant account credentials which you'll need in order to send messages.

.. note:: Please refer to the "`Configuration files <config_files.html>`__" section for more detailed information on configuration requirements for all services.

.. todo::
    - Create test using ``debug`` attribute


Core features
-------------

- **Send messages to several services** -- *the* ``send_message()`` *method routes the request to all services listed in the ``channels`` attribute in ``attribs``.*
- **Send messages using specific services using** ``send_message_via_xxxx()`` **methods** -- *the* ``Comms`` *object also has wrapper methods for the individual services.*


Send message to one or more channels
------------------------------------

You can send messages using the unified ``send_message()`` method as follows:

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

.. note:: Please refer to section "`Configuration files <config_files.html>`__" for more details on defining ``secrets`` and ``config`` data.

.. note:: Please see below for a detailed description of options for ``attribs`` and note that different items are required depending on which channels are used. Also note that some values can be stored as default values when initializing the main ``Comms`` object and then do not need to be included in the ``attribs`` argument when calling methods to send emails.


Send email using ``send_message_via_email()``
---------------------------------------------

You can send emails using the ``send_message_via_email()`` method as follows:

STEP 1: initialize ``Comms`` object

.. code-block::

    comms = Comms(
                secrets,            # credentials required for services
                config              # optional settings
            )

STEP 2: call ``send_message_via_email()`` method:

.. code-block::

    comms.send_message_via_email(
                "Hello world!",     # plain text message
                attribs             # misc. attributes required to send message
            )

.. note:: Please refer to section "`Configuration files <config_files.html>`__" for more details on defining ``secrets`` and ``config`` data.

.. note:: Please refer to section "`Mailgun email <send_mailgun.html>`__" for additional details and examples for sending emails.

.. note:: Please see below for a detailed description of options for ``attribs`` and note that some items are required in order to send emails. Also note that some values can be stored as default values when initializing the ``Comms`` object and then do not need to be included in the ``attribs`` argument when calling this method.

.. note:: If ``send_message_via_email()`` is used, then ``channels`` attribute is not required in the ``attribs`` argument.


Send SMS using ``send_message_via_sms()``
-----------------------------------------

You can send messages via SMS using the ``send_message_via_sms()`` method as follows:

STEP 1: initialize ``Comms`` object

.. code-block::

    comms = Comms(
                secrets,            # credentials required for services
                config              # optional settings
            )

STEP 2: call ``send_message_via_sms()`` method:

.. code-block::

    comms.send_message(
                "Hello world!",     # plain text message
                attribs             # misc. attributes required to send message
            )

.. note:: Please refer to section "`Configuration files <config_files.html>`__" for more details on defining ``secrets`` and ``config`` data.

.. note:: Please refer to section "`Twilio SMS <send_twilio.html>`__" for additional details and examples for sending SMS.

.. note:: Please see below for a detailed description of options for ``attribs`` and note that some items are required in order to send messages via SMS. Also note that some values can be stored as default values when initializing the ``Comms`` object and then do not need to be included in the ``attribs`` argument when calling this method.

.. note:: If ``send_message_via_sms()`` is used, then ``channels`` attribute is not required in the ``attribs`` argument.


Post Twitter status update using ``send_message_via_twitter()``
---------------------------------------------------------------

You can post Twitter status updates using the ``send_message_via_twitter()`` method as follows:

STEP 1: initialize ``Comms`` object

.. code-block::

    comms = Comms(
                secrets,            # credentials required for services
                config              # optional settings
            )

STEP 2: call ``send_message_via_twitter()`` method:

.. code-block::

    comms.send_message_via_twitter(
                "Hello world!",     # plain text message
                attribs             # misc. attributes required to send message
            )

.. note:: Please refer to section "`Configuration files <config_files.html>`__" for more details on defining ``secrets`` and ``config`` data.

.. note:: Please refer to section "`Twitter update & DM <send_twitter.html>`__" for more details around posting Twitter status updates and sending DMs using the ``twitter.Twitter`` object and its methods.

.. note:: Please see below for a detailed description of options for ``attribs`` and note that some items are required in order to post Twitter status updates. Also note that some values can be stored as default values when initializing the ``Comms`` object and then do not need to be included in the ``attribs`` argument when calling this method.

.. note:: If ``send_message_via_twitter()`` is used, then ``channels`` attribute is not required in the ``attribs`` argument.


Post Slack status update using ``send_message_via_slack()``
-----------------------------------------------------------

You can post Slack status updates using the ``send_message_via_slack()`` method as follows:

STEP 1: initialize ``Comms`` object

.. code-block::

    comms = Comms(
                secrets,            # credentials required for services
                config              # optional settings
            )

STEP 2: call ``send_message_via_slack()`` method:

.. code-block::

    comms.send_message_via_slack(
                "Hello world!",     # plain text message
                attribs             # misc. attributes required to send message
            )

.. note:: Please refer to section "`Configuration files <config_files.html>`__" for more details on defining ``secrets`` and ``config`` data.

.. note:: Please refer to section "`Slack message <send_slack.html>`__" for more details around posting Slack status updates using the ``slack.Slack`` object and its methods.

.. note:: Please see below for a detailed description of options for ``attribs`` and note that some items are required in order to post Slack status updates. Also note that some values can be stored as default values when initializing the ``Comms`` object and then do not need to be included in the ``attribs`` argument when calling this method.

.. note:: If ``send_message_via_slack()`` is used, then ``channels`` attribute is not required in the ``attribs`` argument.


Keywords and values for ``attribs`` argument
--------------------------------------------

.. include:: attribs.rst


Examples
--------

**Example -- send simple message via multiple channels**

.. code-block::
   :linenos:

    comms = Comms(secrets, config)              # Initialize ``Comms`` with credentials
                                                # and optional default settings
    msg = "Hello world!"
    attribs = {
        "channels": ["f451_mailgun", "f451_twilio", "f451_twitter", "f451_slack"],
        "to_phone": "+12125550000",
        "to_channel": "#GothamCrime",
        "to_email": "batman@example.com",
        "subject": "Hello!",
    }

    comms.send_message(msg, attribs)            # Send message via multiple channels
