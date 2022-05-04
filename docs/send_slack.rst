Post message to Slack workspace
===============================

The *f451 Communications* module allows you to post messages to so-called `Slack channels <https://slack.com>`__ using a unified interface. In it's simplest for form, you can post a plain text message to a given channel. But you can also post complex messages using so-called `Slack blocks <https://api.slack.com/block-kit>`__ with styling, images, and more.

In order to use this service, you'll need to `set up an account with Slack <https://slack.com/get-started#/createnew>`__. Once that is done, you get your API key and other relevant account credentials.

.. note:: Please refer to the "`Configuration files <config_files.html>`__" section for more detailed information on configuration requirements for `Slack <https://slack.com>`__.

.. todo::
    - Create test using ``debug`` attribute
    - Create test using Slack block content attribute and ``debug`` flag


Core features
-------------

- **Post plain text messages to a Slack channel** -- *Allows you to post simple messages to Slack channels.*
- **Post formatted messages using Slack blocks** -- *Allows to post complex multi-block messages.*


Sending email using the ``slack.Slack`` object
----------------------------------------------

You can send SMS using the ``send_message()`` method of the ``Slack`` object in the ``comms_slack`` sub-module as follows:

1. Initialize the ``Slack`` object:

.. code-block::

    client = Slack(
                authToken,          # your Slack auth token
                fromName,           # your Slack username
                signingSecret,      # your Slack signing secret
                appToken,           # your Slack app token
                defaults            # optional default values
            )

2. Call the ``send_message()`` method:

.. code-block::

    client.send_message(
                "Hello world!",     # plain text message
                attribs             # misc. attributes required to send message
            )

ALTERNATIVE: call ``send_message_with_blocks()`` method

.. code-block::

    client.send_message_with_blocks(
                blocks,             # message in form of list of Slack blocks
                attribs             # misc. attributes required to send message
            )

Slack ``blocks`` are a list of one or more ``dict`` structure. The following is a simple example:

.. code-block::

    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Hello world!"
        }
    }


.. note:: Please refer to `Slack blocks documentation <https://api.slack.com/block-kit/building>`__ for more information of creating and styling message blocks.

.. note:: Please to section "`Configuration files <config_files.html>`__" for more details on defining ``secrets`` and ``config`` data.

.. note:: Please see below for a detailed description of options for ``attribs`` and note that some items are required in order to send messages via Slack. Also note that some values can be stored as default values when initializing the main ``Slack       `` object and the do not need to be included in the ``attribs`` argument.


Keywords and values for ``attribs`` argument
--------------------------------------------

.. include:: attribs.rst


Examples
--------

Example -- attributes for simple Slack message:

.. code-block::

    attribs = {
        "to_channel": "#general",
    }

Example -- attributes for Slack message using Slack blocks:

.. code-block::

    attribs = {
        "to_channel": "#general",
        "attachments": ["path/to/joker.jpg", "path/to/riddler.jpg"],
    }


Additional references
---------------------

- `Slack documentation <https://api.slack.com/apis>`__
