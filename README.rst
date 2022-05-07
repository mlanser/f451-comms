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


.. warning:: This module is in early alpha stage. And while the code works (and passes all the tests), **use at your own risk 🤓**


TL;DR
-----
.. tldr-start

This module provides a universal interface for various communications systems and services (e.g. email, Slack, SMS, etc.) and makes it possible to send the same message to several services with a single method call. The same call structure is used regardless of which services are enabled.

.. tldr-end


Installation
------------

.. install-start

You can install the *f451 Communications* module via `pip <https://pip.pypa.io/en/stable/#>`__ from `PyPi <https://pypi.org/>`__:

.. code:: console

   $ pip install f451-comms

.. install-end


Quickstart
----------

.. qs-start

A common use case for the *f451 Communications* module is in applications that send (usually programmatically generated) messages via one or more channels. The module assumes that you provide all necessary keys and secrets required to verify your credentials with the services linked to the channels that you want to use.

It is recommended that you store these keys and secrets in a separate file (e.g. ``secrets.ini``). However, it is also possible to submit them -- for example during testing -- in the form of a so-called ``dict`` structure. Please review the section ":doc:`Configuration files<config_files>`" for more information.

.. code-block::

    from configparser import ConfigParser, ExtendedInterpolation
    from f451_comms.comms import Comms

    secrets = ConfigParser(interpolation=ExtendedInterpolation())
    secrets.read("_PATH_TO_YOUR_SECRETS_FILE_")

    comms = Comms(secrets)
    comms.send_message("Hello world!", "all")

The basic sequence is to first initialize the ``Comms`` object with the keys and secrets required to authenticate with the services that you want to use. After that you can send messages to one or more channels with a single method call to the ``Comms`` object.

The ``send_message()`` method also has a 3rd argument that allows you to include additional attributes using a ``dict`` structure. These attributes can contain a wide variety of items. For example, you can include the HTML version of an email, or Slack blocks for more complex Slack messages. You can also include references to images to be included with the message, or files to be attached to emails, and so on.

.. qs-end


Background
----------

.. bkgrnd-start

This module was originally created to "scratch an itch" -- or, as we say in marketing parlance: to solve a particular use case. 😉 -- I had several single-purpose applications running on different devices (e.g. `Raspberry Pi <https://www.raspberrypi.org/>`_) configured to support specific hardware configurations (i.e. sensors and displays, etc.), services, or functions. And all applications were designed to notify me via different channels that certain events had occurred and so on.

Using a standardized communications library made it easy to have the main application on each device communicate results to the same channels without writing duplicate code for each application for a given device. Instead, I can now import this library, and most/all per-application customization can be handled by updating config files on each device.

For example, I have several devices that continuously collect data from sensors and perform various processing tasks on that data. Then, at regular intervals, when specific tasks are completed or certain events are triggered, I get notified via SMS, some fancy Slack message, or even get a nice HTML-based email with a status update, etc. And in some cases, the devices also notify the world via Twitter that whatever status was updated.

But most importantly, I'm able to call a simple ``send_message()`` method, which works the same way regardless of which services are enabled for a given device. And if I add a new communications channel, I can enable it quickly on my devices without updating the core applications. Simply adding the new channel to a configuration file is enough 😎

**Current support:**

- `Email via Mailgun <https://mailgun.com>`__ -- plain text and HTML, with attachments and inline images
- `Slack <https://slack.com>`__ -- plain text and Slack blocks
- `SMS via Twilio <https://twilio.com/sms/>`__ -- SMS with images
- `Twitter <https://twitter.com>`__ -- status updates and DMs

**Future support:**

- Other - *I know, this is really specific ... but there will be more* 😜

.. bkgrnd-end


Run a demo of this module
-------------------------

.. demo-start

This module comes with a demo that allows you to experiment with sending messages to the various channels. Of course, you must first ensure that you have accounts with the services that you want to experiment with. You must also provide the appropriate credentials when starting the demo or it will simply fail to authenticate with the services you're trying to use.

Please see the section "`Run demo`_" for more information.

.. demo-end

.. misc-start

Contributing
------------

Contributions are very welcome. To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_, the *f451 Communications* module is free and open source software.


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
