(Un-)conventions
================

OK, let's get this out of the way: I'm coming to `Python <https://www.python.org/>`__ late in my career and I'm coming over to this side after years of programming in languages like `JavaScript <https://developer.mozilla.org/en-US/docs/Web/JavaScript>`__, `PHP <https://www.php.net/>`__, `C <https://en.wikipedia.org/wiki/C_(programming_language)>`__ & `C++ <https://en.wikipedia.org/wiki/C%2B%2B>`__, `Java <https://en.wikipedia.org/wiki/Java_(programming_language)>`__, `Modula-2 <https://en.wikipedia.org/wiki/Modula-2>`__, `Pascal <https://en.wikipedia.org/wiki/Pascal_(programming_language)>`__, `Forth <https://en.wikipedia.org/wiki/Forth_(programming_language)>`__, and `Assembly <https://en.wikipedia.org/wiki/Assembly_language>`__. And yes, I may have some quirks and habits that have built up some crud over the years.

Where am I going with this? Well, let's just say that my coding style may not always be `Pythonic <https://docs.python.org/3/glossary.html>`__. But, in my defense, I try very hard to be consistent both within and across my projects 🤓


Naming conventions
------------------

- **Class names** -- `Camel case <https://en.wikipedia.org/wiki/Camel_case>`__ with first letter always capitalized -- example: ``Email``, ``Twitter``, etc. The only exception are classes where a common acronym works best as a class name (e.g. ``SMS``) and then I use all caps.
- **Function and method names** -- `Snake case <https://en.wikipedia.org/wiki/Snake_case>`__ -- example: ``send_message()``. Private class methods are always prefixed with an underscore (_).
- **Variable names** -- `Camel case <https://en.wikipedia.org/wiki/Camel_case>`__ with occasional pseudo `hungarian notation <https://en.wikipedia.org/wiki/Hungarian_notation>`__. I know ... this is so not `Pythonic <https://docs.python.org/3/glossary.html>`__! But I can't help it. Most of my variables have names like ``authToken`` and ``fromName`` and names of private class attributes are, again, prefixed with an underscore (_). But yes, sometimes you may see a few names like ``listStr`` to indicate that this is a ``list`` of ``str``. Usually I only use names like that inside helper functions where, like in this example, the strings can contain anything (e.g. names of dogs, auth tokens, tags, etc.). At least I have stopped calling them "arrays" 🤓
- **Constants** -- always all caps -- 'nuff said! 😉


Files and folders
-----------------

- **Root folder** -- holds misc config files, etc. for `git <https://git-scm.com/>`__, `Poetry <https://python-poetry.org/>`__, and other tools.
- ``docs`` **folder** -- holds most documentation in ``.rst`` files. The exceptions are files like ``README.rst``, ``LICENSE.rst`` and other more generic project documentation.
- ``src`` **folder** -- holds all source code files.
- ``tests`` **folder** -- holds all test files.


Other notes
===========

Again, I try to be very consistent and my code should (hopefully) be easy to follow. I also try to document a lot of stuff, both with in-code comments and actual project documentation. Why? Because I have the memory of a goldfish [1]_ and I forget after week or so why I did whatever I did.

Please note, though, that I am a one-man-band and there are bound to be mistakes, and, quite likely, a bug or two (or more) in my code and documentation. I am `dog-fooding <https://en.wikipedia.org/wiki/Eating_your_own_dog_food>`__ my packages and libraries as I use them in my various projects. And, of course, I try to fix bugs and correct mistakes as I find them.

Now, if you find a problem, please feel free to log an issue. Or, better yet, maybe you can help fix the issue and submit a PR 🤓

.. [1] Turns out goldfish may have better memory than me: `Do goldfish really have a 3-second memory? <https://www.livescience.com/goldfish-memory.html>`__
