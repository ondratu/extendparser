"""ConfigParser with include support.

.. code:: ini

    # test.ini
    [main]
    key = value

    .include include.ini

.. code:: ini

    # include.ini
    [main]
    foo = bar

example code:

    >>> from iconfigparser import IConfigParser
    >>> from sys import stdout
    >>> cp = IConfigParser()
    >>> cp.read("test.ini")
    >>> cp.write(stdout)
"""

from sys import version_info
from os.path import exists

if version_info.major == 2:
    from ConfigParser import ConfigParser
    from io import BytesIO as BufferIO
else:
    from configparser import ConfigParser
    from io import StringIO as BufferIO


class IConfigParser(ConfigParser):
    def readfp(self, fp, source=None):
        """Alias for read_file like in Python 3.x"""
        self.read_file(fp, source)

    def read_file(self, fp, source=None):
        config_string = BufferIO()
        includes = set()

        for line in fp:
            if line.startswith('.include'):
                includes.add(line[8:].strip())
            else:
                config_string.write(line)

        config_string.seek(0)

        if version_info.major == 2:
            ConfigParser.readfp(self, config_string, source)
        else:
            # readfp in python3 call self(SmartConfig).read_file
            ConfigParser.read_file(self, config_string, source)

        for inc in includes:
            if inc:
                self.read(inc)

    def read(self, inc):
        if exists(inc):
            with open(inc, 'r') as fp:
                self.read_file(fp, inc)


if __name__ == "__main__":
    from sys import stdout

    cp = IConfigParser()
    cp.read("test.ini")

    cp.write(stdout)
