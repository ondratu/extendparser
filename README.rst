extendparser
============

Extend parser is set of ``ConfigParser`` extensions. All extensions are added
to one final class ``ExtendParser``. For more details see source code, or use
help.


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
Include class can append content of other configuration to calling. Let's have
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
Get class have two smart methods ``get_option`` and ``get_section`` to get
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

Installation
------------

.. code:: sh

  ~$ pip install extendparser
