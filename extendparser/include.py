"""ConfigParser with include support.

    .. code:: ini

        # tests/data/test.ini
        [main]
        key = value

        .include tests/data/include.ini

    .. code:: ini

        # tests/data/include.ini
        [main]
        foo = bar

    example code:

        >>> from extendparser.include import Include
        >>> from sys import stdout
        >>> cp = Include()
        >>> cp.read("tests/data/test.ini")
        >>> print(cp.get("main", "key"))
        value
        >>> print(cp.get("main", "foo"))
        bar
"""

from sys import version_info
from os.path import exists

from extendparser.to3 import ConfigParser, BufferIO

__all__ = ["ConfigParser"]


class Include(ConfigParser):
    """ConfigParser which supports includes.

    Includes are provide by `.include` keyword on empty line. Including is like
    templating, so each included file expression is replaced in read config
    string.
    """
    def readfp(self, fp, source=None):
        """Alias for read_file like in Python 3.x"""
        self.read_file(fp, source)

    def read_file(self, fp, source=None):
        """Overriding method which support .include expression."""
        config_string = BufferIO()

        for line in fp:
            if line.startswith('.include'):
                self.read_buffer(config_string, source)

                self.read(line[8:].strip())     # read includeded ini
                config_string = BufferIO()      # reset config_string
            else:
                config_string.write(line)

        self.read_buffer(config_string, source)

    def read_buffer(self, buff, source=None):
        """This method read call original methods.

        Use readfp in python2 or read_file in python3."""
        buff.seek(0)

        if version_info.major == 2:
            ConfigParser.readfp(self, buff, source)
        else:
            # readfp in python3 call self(SmartConfig).read_file
            ConfigParser.read_file(self, buff, source)

    def read(self, inc):
        """Overriding method to call instance read_file from actual path."""
        if exists(inc):
            with open(inc, 'r') as fp:
                self.read_file(fp, inc)
