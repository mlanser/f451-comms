Installation
============

.. include:: ../README.rst
    :start-after: install-start
    :end-before: install-end

If you're using `Poetry <https://python-poetry.org/>`__ for dependency management, then you can add this module as follows to your project:

.. code:: console

   $ poetry add f451-comms

Once installed, you can import the main ``Comms`` module into your project as follows:

.. code-block::

    from f451_comms.comms import Comms

    comms = Comms(<secrets>)
    comms.send_message("Hello world!", "all")

And while importing the main module usually is the best option for most use cases, it is also possible to import any of the sub-modules. The following example illustrates how you can import a specific sub-module. In this case only the ``Mailgun`` provider module is imported.

.. code-block::

    from src.f451_comms.providers.mailgun import Mailgun

    client = Mailgun(
                apiKey="<_YOUR_API_KEY_>",
                from_name="<_EMAIL_SENDER_>",
                to_email="<_EMAIL_RECIPIENT_>",
                subject="<_EMAIL_SUBJECT_>",
            )
    response = client.send_message("Hello world!", **<_OTHER_MESSAGE_SETTINGS_>)
