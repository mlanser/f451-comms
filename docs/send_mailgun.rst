Send email via Mailgun
======================

The *f451 Communications* module allows you to send emails via the `Mailgun <https://mailgun.com>`__ service using a unified interface. In it's simplest form, you can send a plain text email to one or more recipients. But you can also send complex individualized HTML-emails with attachments and inline images.

In order to use this service, you'll need to `set up an account with Mailgun <https://signup.mailgun.com/new/signup>`__. Once that is done, you get your API key and other relevant account credentials.

.. note:: Please refer to the "`Configuration files <config_files.html>`__" section for more detailed information on configuration requirements for the `Mailgun <https://mailgun.com>`__ email service.


Core features
-------------

- **Send plain text and/or HTML emails** -- *An email can be either plain text only, or have both a plain text version of the message and an HTML version included as well.*
- **Supports file attachments and inline images** -- *Emails can include both file attachments and inline images. Please note that emails cannot exceed 25MB in size (incl. any attachments).*
- **Supports multiple 'to' addresses** -- *Every email can have up to max 1,000 recipients.*
- **Supports optional multiple 'cc' and 'bcc' addresses** -- *Emails support both 'cc' and 'bcc' recipients. But each recipient in either list counts towards to total max of 1,000 recipients.*


Examples
--------

.. note:: These examples use the ``send_message_via_email()`` method. But you can also use the generic ``send_message()`` method with the same arguments.

**Example -- send simple email**

.. code-block::
   :linenos:

    comms = Comms(secrets, config)              # Initialize ``Comms`` with credentials
                                                # and optional default settings
    msg = "Hello world!"
    attribs = {
        "channels": "f451_mailgun",
        "to_email": "batman@example.com",
        "subject": "Hello!",
    }

    comms.send_message_via_email(msg, attribs)  # Send email


**Example -- send email with attachments**

.. code-block::
   :linenos:

    comms = Comms(secrets, config)              # Initialize ``Comms`` with credentials
                                                # and optional default settings
    msg = "Hello world!"
    attribs = {
        "channels": "f451_mailgun",
        "to_email": "batman@example.com",
        "subject": "Hello!",
        "attachments": ["path/to/joker.txt", "path/to/riddler.txt"],
    }

    comms.send_message_via_email(msg, attribs)  # Send email


**Example -- send email with HTML and inline images**

.. code-block::
   :linenos:

    comms = Comms(secrets, config)              # Initialize ``Comms`` with credentials
                                                # and optional default settings
    msg = "Hello world!"
    attribs = {
        "channels": "f451_mailgun",
        "to_email": "batman@example.com",
        "subject": "Hello!",
        "html": "<html>Hello world! Look at this image <img src="cid:joker.jpg"></html>",
        "inline": "path/to/joker.jpg",
    }

    comms.send_message_via_email(msg, attribs)  # Send email


**Example -- send email using recipients data**

.. code-block::
   :linenos:

    comms = Comms(secrets, config)              # Initialize ``Comms`` with credentials
                                                # and optional default settings
    msg = "Hello world!"
    attribs = {
        "channels": "f451_mailgun",
        "to_email": ["batman@example.com", "robin@example.com"],
        "subject": "Hello %recipient.name%!",
        "html": "<html>Your lucky number is %recipient.lucky%</html>",
        "recipient_data": {
            "batman@example.com": {"name":"Batman", "lucky": 13},
            "robin@example.com": {"name":"Robin", "lucky": 29}
        }
    }

    comms.send_message_via_email(msg, attribs)  # Send email


Additional references
---------------------

- `Mailgun documentation <https://documentation.mailgun.com/en/latest/index.html>`__
