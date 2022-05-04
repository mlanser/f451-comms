f451 Communications module
==========================

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/f451-comms.svg
   :target: https://pypi.org/project/f451-comms/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/f451-comms.svg
   :target: https://pypi.org/project/f451-comms/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/f451-comms
   :target: https://pypi.org/project/f451-comms
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/f451-comms
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/f451-comms/latest.svg?label=Read%20the%20Docs
   :target: https://f451-comms.readthedocs.io/
   :alt: Read the documentation at https://f451-comms.readthedocs.io/
.. |Tests| image:: https://github.com/mlanser/f451-comms/workflows/Tests/badge.svg
   :target: https://github.com/mlanser/f451-comms/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/mlanser/f451-comms/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/mlanser/f451-comms
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

.. warning:: This module is still pre-pre-pre-long-way-to-go-to-alpha! **Use at your own risk 🤓**

This module provides a universal interface for various communications systems and services (e.g. email, Slack, SMS, etc.). This means that we can send the same message to several channels/services with a single call. And we can also use that the same call structure regardless of which channels/services are enabled.

This module was created to "scratch an itch" -- or as we say in marketing parlance: to solve a particular use case 😉 -- where several applications run on different `Raspberry Pi <https://www.raspberrypi.org/>`_ devices that are all configured with different hardware, etc.

Using a standardized communications library makes it easier to have the main application on each device communicate results to the same channels without needing to create duplicate code in each application for a given device. Instead, most/all customization can be handled by simply updating config files on each device.

For example, I have several devices that continuously collect different types of data and/or perform various tasks. And, at regular intervals, when specific tasks are completed, or certain events are triggered, I want to be notified via SMS, get some fancy Slack message, or even get a nice HTML-bsed email with a status update, etc. I may even want to notify the world via Twitter that this or that happened, or that whatever status was updated.

But most of all, I want to be able to have a simple ``send_message()`` that works regardless of what services are enabled for a given device. And if I add a new communications channel, then I want to enable that quickly on my devices without having to update the core applications. Just adding the new channel to some configuration file should be enough 😎

**Current support:**

- `Email via Mailgun <https://mailgun.com>`__ -- plain text and HTML, with attachments and inline images
- `Slack <https://slack.com>`__ -- plain text and Slack blocks
- `SMS via Twilio <https://twilio.com/sms/>`__ -- SMS with images
- `Twitter <https://twitter.com>`__ -- status updates and DMs

**Future support:**

- Other - *I know, this is really specific* 😜


Requirements
------------

The *f451 Communications* module acts as an abstraction layer on top of existing communications packages, and in order for it to work, you need to first install the underlying packages and get accounts with the associated services.

Please note, that you do not have to use all services. In the end, the config files ``secrets.ini`` and ``config.ini`` define which services are enabled. Conversely, if you enable a service where you do not have the proper API keys, etc., then the module will raise exceptions when authentication fails due to missing and/or invalid credentials.

- **email** -- account at `Mailgun <https://mailgun.com>`__
- **Slack** -- account at `Slack <https://slack.com>`__ and `Python Slack SDK <https://github.com/SlackAPI/python-slack-sdk>`__
- **SMS** -- account at `Twilio <https://twilio.com>`__ and `Twilio Python <https://github.com/twilio/twilio-python>`__
- **Twitter** -- account at `Twitter <https://slack.com>`__ and `Tweepy <https://docs.tweepy.org/en/stable/index.html>`__ package

Please review documentation for each sub-module for additional information.


Installation
------------

You can install the *f451 Communications* module via pip_ from PyPI_:

.. code:: console

   $ pip install f451-comms


Quickstart
----------

The most common use case for the *f451 Communications* module is to use it in some application that needs to communicate (auto-)generated messages via one or more channels. The module assumes that you provide all necessary keys and secrets required to verify your credentials for services associated with the channels that you want to use.

It is recommended that you store these keys and secrets in a separate file (e.g. ``secrets.ini``). However, it is also possible to submit them -- for example during testing -- in the form of a so-called ``dict`` structure. Please review the section "`Configuration files`_" for more information.

.. code-block::

    from configparser import ConfigParser, ExtendedInterpolation
    from f451_comms.comms import Comms

    secrets = ConfigParser(interpolation=ExtendedInterpolation())
    secrets.read("_PATH_TO_YOUR_SECRETS_FILE_")

    comms = Comms(secrets)
    comms.send_message("Some clever message", "all")

The basic sequence is to first initialize the ``Comms`` object with the keys and secrets required to authenticate with the services that we want to use. After that we're ready to send messages to one or more channels with a single method call to the ``Comms`` object.

The ``send_message()`` method also has a 3rd argument that allows you to include additional attributes in a ``dict`` structure. These attributes can contain a wide variety of items. For example, you can include the HTML version of an email, or Slack blocks for more complex Slack messages. You can also include references to images to be included with the message, or files to be attached to emails, and so on.


Run a demo of this module
-------------------------

This module come with a demo that allows you to experiment with sending messages to the various channels. Of course, you must first ensure that you have accounts with the services that you want to experiment with and you must provide the appropriate credentials when starting the demo or it will simply fail to authenticate with the services you're trying to use.

Please see the section "`Run demo`_" for more information.


Contributing
------------

Contributions are very welcome. To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_, *f451 Communications* module is free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/mlanser/f451-comms/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://f451-comms.readthedocs.io/en/latest/usage.html
.. _Configuration files: https://f451-comms.readthedocs.io/en/latest/config_files.html
.. _Run demo: https://f451-comms.readthedocs.io/en/latest/demo.html
