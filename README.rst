extendparser
============

Extend parser is set of ``ConfigParser`` extensions. ``Get`` and ``Include``
extensions are added to one class ``ExtendParser``. For more details see source
code, or use help.


:copyright: 2018, see AUTHORS for more details
:license: BSD, see LICENSE for more details

Library
-------

ExtendParser
~~~~~~~~~~~~

.. code:: python

    >>> from extendparser import ExtendParser
    >>> cp = ExtendParser()

Include
~~~~~~~
Include class can append content from other configuration files. Let's have
these configuration files:

.. code:: ini

  # test.ini
  [main]
  string = value
  .include numbers.ini

.. code:: ini

  # numbers.ini
  integer = 42
  .include const.ini

.. code:: ini

  # const.ini
  pi = 3.14


Here is the string buffer which ConfiguratinParser will read:

.. code:: ini

  # test.ini
  [main]
  string = value
  # numbers.ini
  integer = 42
  # const.ini
  pi = 3.14

Get
~~~
Get class has two smart methods ``get_option`` and ``get_section`` to get
value(s) in any type you want.

.. code:: python

    >>> from extendparser.get import Get
    >>> cp = Get()
    >>> print(cp.get_option("test", "number", target=int, fallback=1))
    1
    >>> print(cp.get_option("test", "list", target=list, fallback=["a"],
    ...                      delimiter=','))
    ['a']
    >>> cp.add_section("test")
    >>> cp.set("test", "tuple", "a:b:c")
    >>> print(cp.get_option("test", "tuple", target=tuple, delimiter=':'))
    ('a', 'b', 'c')
    >>> print(cp.get_section("test", (("tuple", tuple, tuple(), ':'),
    ...                               ("string", str, "value"))))
    {'tuple': ('a', 'b', 'c'), 'string': 'value'}

Environment
~~~~~~~~~~~
Environ module has two classes, which extend ``ConfigParser`` to read
environment variables. There is ``EnvironFirst`` class, which read environment
variables first, and then use original get method.


.. code:: python

    >>> from os import environ
    >>> from configparser import ConfigParser
    >>> from extendparser.environ import EnvironFirst
    >>> cp = EnvironFirst()
    >>> cp.add_section("test")
    >>> cp.getint("test", "number", fallback=1)
    1
    >>> cp.set("test", "number", "7")
    >>> cp.getint("test", "number")
    7
    >>> environ["TEST_NUMBER"] = "42"
    >>> cp.getint("test", "number")
    42

Next ``EnvironLast`` class use environment variable as fallback for original get
method.

.. code:: python

    >>> from os import environ
    >>> from configparser import ConfigParser
    >>> from extendparser.environ import EnvironLast
    >>> cp = EnvironLast()
    >>> cp.add_section("test")
    >>> cp.getfloat("test", "float", fallback=1.0)
    1.0
    >>> environ["TEST_FLOAT"] = "42"
    >>> cp.getfloat("test", "float", fallback=1)
    42.0
    >>> cp.set("test", "float", "3.14")
    >>> cp.getfloat("test", "float")
    3.14

Installation
------------

.. code:: sh

  ~$ pip install extendparser
