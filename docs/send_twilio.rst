Send SMS via Twilio
===================

The *f451 Communications* module allows you to send SMS via the `Twilio SMS <https://www.twilio.com/sms>`__ service using a unified interface. In it's simplest for form, you can send a plain text message to a given recipient. But you can also send a more complex message with attached images.

In order to use this service, you'll need to `set up an account with Twilio <https://www.twilio.com/try-twilio>`__. Once that is done, you get your API key and other relevant account credentials.

.. note:: Please refer to the "`Configuration files <config_files.html>`__" section for more detailed information on configuration requirements for the `Twilio <https://twilio.com>`__ messaging service.


Core features
-------------

- **Send SMS** -- *Messages can be text-only as well as include images.*
- **Supports multiple 'to' phone numbers** -- *Allows you to send text messages to multiple recipients*


Examples
--------

.. note:: These examples use the ``send_message_via_sms()`` method. But you can also use the generic ``send_message()`` method with the same arguments.

**Example -- send simple SMS**

.. code-block::
   :linenos:

    comms = Comms(secrets, config)              # Initialize ``Comms`` with credentials
                                                # and optional default settings
    msg = "Hello world!"
    attribs = {
        "channels": "f451_twilio",
        "to_phone": "+12125550000",
    }

    comms.send_message_via_sms(msg, attribs)    # Send SMS


**Example -- send SMS with attachments**

.. code-block::
   :linenos:

    comms = Comms(secrets, config)              # Initialize ``Comms`` with credentials
                                                # and optional default settings
    msg = "Hello world!"
    attribs = {
        "channels": "f451_twilio",
        "to_phone": "+12125550000",
        "attachments": ["path/to/joker.jpg", "path/to/riddler.jpg"],
    }

    comms.send_message_via_sms(msg, attribs)    # Send SMS


**Example -- send SMS to multiple recipients**

.. code-block::
   :linenos:

    comms = Comms(secrets, config)              # Initialize ``Comms`` with credentials
                                                # and optional default settings
    msg = "Hello world!"
    attribs = {
        "channels": "f451_twilio",
        "to_phone": ["+12125550000", "+12125551111"],
    }

    comms.send_message_via_sms(msg, attribs)    # Send SMS


Additional references
---------------------

- `Twilio SMS documentation <https://www.twilio.com/docs/sms/quickstart/python>`__
